#!/usr/bin/env python

# Make sure we can find all of our submodules
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'lib'
))

import pathlib
import argparse
import json
import typing
import logging
import math
from datetime import datetime
from dataclasses import dataclass
from contextlib import contextmanager, ExitStack
from collections import defaultdict, Counter
from sqlalchemy import create_engine, event, text, URL, Engine, TextClause
import pandas as pd
import numpy as np
import torch
import psutil
import shapely
from shapely import geometry
import tc_etl_lib as tc

# -------------------------------------
# Config management section
# -------------------------------------

def loadConfig(jsonPath: pathlib.Path):
    """Loads script configuration into environment from json file"""
    with jsonPath.open() as f:
        for k, v in json.load(f).items():
            os.environ[k] = str(v)

def dumpConfig() -> dict:
    """Dumps script configuration into a dict"""
    result = {}
    for k, v in os.environ.items():
        if k.startswith("ETL_VECTORIZE_"):
            #if "_PASS" in k:
            #    v = "***"
            result[k] = v
    return result

# -------------------------------------
# Connection management section
# -------------------------------------

@contextmanager
def psql_engine() -> typing.Iterator[Engine]:
    """Yields a postgres connection to the database"""
    url_object = URL.create(
        "postgresql+psycopg",
        username=os.getenv("ETL_VECTORIZE_PG_USER"),
        password=os.getenv("ETL_VECTORIZE_PG_PASSWORD"),
        host=os.getenv("ETL_VECTORIZE_PG_HOST"),
        port=int(os.getenv("ETL_VECTORIZE_PG_PORT", "5432")),
        database=os.getenv("ETL_VECTORIZE_PG_NAME")
    )
    pg_schema = os.getenv("ETL_VECTORIZE_PG_SCHEMA")
    engine = create_engine(url_object)
    try:
        # See https://docs.sqlalchemy.org/en/20/dialects/postgresql.html
        @event.listens_for(engine, "connect", insert=True)
        def set_search_path(dbapi_connection, connection_record):
            existing_autocommit = dbapi_connection.autocommit
            dbapi_connection.autocommit = True
            cursor = dbapi_connection.cursor()
            cursor.execute("SET SESSION search_path=%s,public" % pg_schema)
            cursor.close()
            dbapi_connection.autocommit = existing_autocommit
        yield engine
    finally:
        engine.dispose()

def geojson_to_shape(df: pd.DataFrame, colname: str) -> pd.DataFrame:
    """Convert a column containing geojson strings to shapes"""
    def convert(x, colname=colname):
        geojson = x[colname]
        if not geojson:
            return None
        geom = geometry.shape(json.loads(geojson))
        return geom
    df[colname] = df.apply(convert, axis=1)
    return df

@dataclass
class Broker:
    """
    Encapsulates the communication to the context broker
    """
    auth: typing.Optional[tc.authManager] = None
    cb: typing.Optional[tc.cbManager] = None

    @staticmethod
    def create() -> 'Broker':
        password = os.getenv('ETL_VECTORIZE_PASSWORD')
        if not password:
            logging.warn("No broker password provided, running in dettached mode")
            return Broker(auth=None, cb=None)
        auth = tc.auth.authManager(
            endpoint=os.getenv('ETL_VECTORIZE_ENDPOINT_KEYSTONE'),
            service=os.getenv('ETL_VECTORIZE_SERVICE'),
            subservice=os.getenv('ETL_VECTORIZE_SUBSERVICE'),
            user=os.getenv('ETL_VECTORIZE_USER'),
            password=password,
        )
        cb = tc.cb.cbManager(
            endpoint=os.getenv('ETL_VECTORIZE_ENDPOINT_CB'),
            sleep_send_batch=int(os.getenv('ETL_VECTORIZE_SLEEP_SEND_BATCH', '5')),
            timeout=int(os.getenv('ETL_VECTORIZE_TIMEOUT', '10')),
            post_retry_connect=float(os.getenv('ETL_VECTORIZE_POST_RETRY_CONNECT', '3')),
            post_retry_backoff_factor=float(os.getenv('ETL_VECTORIZE_POST_RETRY_BACKOFF_FACTOR', '2')),
            batch_size=int(os.getenv('ETL_VECTORIZE_BATCH_SIZE', '50')),
        )
        return Broker(auth=auth, cb=cb)

    def fetch(self, entitytype: str, entityid: typing.Optional[str]=None, q: typing.Optional[str]=None) -> typing.Sequence[typing.Any]:
        """Fetch general entity info"""
        if self.cb is None:
            return tuple()
        result = self.cb.get_entities(auth=self.auth, type=entitytype, id=entityid, q=q)
        if result:
            return result
        return tuple()

    def fetch_one(self, entitytype: str, entityid: typing.Optional[str]) -> typing.Any:
        """Fetch general entity info"""
        if self.cb is None:
            return None
        result = self.cb.get_entities_page(auth=self.auth, type=entitytype, id=entityid, limit=1)
        if result:
            return result[0]
        return None

    def push(self, entities=typing.Sequence[typing.Any]):
        """Send entities to CB"""
        if not self.cb:
            return
        self.cb.send_batch(auth=self.auth, entities=entities)

    def delete(self, entitytype: str, q: str):
        """Remove entities from CB"""
        if not self.cb:
            return
        self.cb.delete_entities(auth=self.auth, type=entitytype, q=q)

@contextmanager
def orion_engine() -> typing.Iterator[Broker]:
    """Yields a connection to the context broker"""
    yield Broker.create()

# -------------------------------------
# Data bearing types
# -------------------------------------

@dataclass
class DatasetProperties:
    """
    Contains the properties for a particular scene,
    trend and daytype.
    """
    timeinstant: datetime
    trend: str
    daytype: str


@dataclass
class Dataset(DatasetProperties):
    """
    Contains data for a particular set of measures
    of all the entities of the given entitytype in the
    database.

    This data must be regularized, i.e. grouped at
    the particular time interval proper of the dataset
    (hour, or 10-minute interval). But it should not
    be scaled.

    The dataframe must have at least columns
    "sourceref", "hour" (if hasHour),
    "minute" (if hasMinute) (see class Metadata).
    Then it must also have a column per each of
    the metrics of the entityType.
    """
    entityType: str
    df: pd.DataFrame

@dataclass
class VectorProperties:
    """
    Holds the properties of a vectorized dataset for a given
    entity type. See type `TypedVector` for a description
    of a vectorized dataset.
    """
    entityType: str

@dataclass
class TypedVector(VectorProperties):
    """
    Holds the data of a vectorized dataset for a given entity type.
    This data is fixed length: There is a row per entity id,
    hour (if hasHour) and 10-minute interval (if hasMinute).

    - The entities included in the vector must always be the same
      for a given entityType: the entities the model has been
      trained on. This is given by the dimension table for the
      entityType. Entities are always sorted by id in the vector.
    - if hasHour, there is a row per hour from 00 to 23.
    - if hasMinute, there is a row per 10-minute interval from 00 to 50.

    The columns in the dataframe are at least "sourceref",
    "hour", "minute", and a column per metric. Note that
    "hour" and/or "minute" might be 0 if not hasHour or not
    hasMinute, respectively.

    Notice that the metrics in a row can be NaN if the source
    does not have data for the given combination of sourceref,
    hour and minute.
    """
    df: pd.DataFrame

# -------------------------------------
# Schema bearing types
# -------------------------------------

@dataclass
class Metric:
    """
    Describes properties of a metric
    """
    scale: int
    integer: bool

@dataclass
class Metadata:
    """
    Describes each of the datasets in the database
    """
    dimensions: typing.List[str]
    metrics: typing.Mapping[str, Metric]
    fixedProps: typing.Dict[str, Metric]
    calcs: typing.Dict[str, str]
    hasHour: bool
    hasMinute: bool
    multiZone: bool
    namespace: str
    entityType: str
    dataTableName: str
    dimsTableName: str

    @staticmethod
    def create(kw: typing.Dict[str, typing.Any]) -> 'Metadata':
        """Read Metadata from a json object"""
        for metric_cols in ("fixedProps", "metrics"):
            # Convert metrics to dict of `Metric` objects
            props = {k: Metric(**v) for k, v in kw.pop(metric_cols, {}).items()}
            # Sort metrics in a stable order, and lowercase them
            # to match database column names
            kw[metric_cols] = { k.lower(): props[k] for k in sorted(props.keys()) }
        return Metadata(**kw)

    def dim_query(self, sceneref: str) -> TextClause:
        """Build SQL query to determine all entity IDs in the model"""
        if self.multiZone:
            columns = ["sourceref", "zone", "zonelist", "ST_AsGeoJSON(location) AS location"]
        else:
            columns = ["sourceref", "zone", "Array[zone]::json[] as zonelist", "ST_AsGeoJSON(location) AS location"]
        # This is needed so integer rows with null values are
        # preserved as integer instead of objects.
        # See https://stackoverflow.com/questions/37796916/pandas-read-sql-integer-became-float
        columns.extend(c.lower() if not v.integer
            else f"COALESCE({c.lower()}, 0)::integer AS {c.lower()}"
            for c, v in self.fixedProps.items())
        return text(f"""
            SELECT {','.join(columns)}
            FROM {self.dimsTableName}
            WHERE sceneref=:sceneref
            ORDER BY sourceref ASC
            """)

    def get_dim_df(self, engine: Engine, sceneref: str) -> pd.DataFrame:
        """
        Builds a dataframe of all entity IDs in the model.
    
        The dataframe includes the entityid, entitytype, sourceref,
        location, zone, zonelist, and fixed properties of
        the entitytype (i.e. parking capacity).

        The location is converted to shapely geometry
        before returning.
        """
        query = self.dim_query(sceneref).bindparams(sceneref=sceneref)
        df = pd.read_sql(query, engine)
        df['entitytype'] = self.entityType
        # Make sure to sort by entity id. The order of columns
        # in the vector is important.
        df.sort_values(by=['sourceref'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        # Convert locations from string to shape
        df = geojson_to_shape(df, 'location')
        return df

    def scene_query(self) -> TextClause:
        """Build SQL query for a given sceneref and timeinstant"""
        metrics = {
            k: Metric(scale=0, integer=False)
            for k in self.dimensions
        }
        metrics.update(self.metrics)
        # This is needed so integer rows with null values are
        # preserved as integer instead of objects.
        # See https://stackoverflow.com/questions/37796916/pandas-read-sql-integer-became-float
        columns = ", ".join(c.lower() if not v.integer
            else f"COALESCE({c.lower()}, 0)::integer AS {c.lower()}"
            for c, v in metrics.items()
        )
        return text(f"""
        SELECT {columns}
        FROM {self.dataTableName}
        WHERE sceneref = :sceneref
        AND timeinstant = :timeinstant
        """)

    def get_scene_df(self, engine: Engine, sceneref: str, timeinstant: datetime) -> pd.DataFrame:
        """Retrieves a DataFrame with all data for the scene and timeinstant"""
        query = self.scene_query()
        df = pd.read_sql(query.bindparams(sceneref=sceneref, timeinstant=timeinstant), engine)
        return df

    def get_fixed_df(self, dims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a placeholder dataset with a fixed size. The generated
        dataset will have the columns:
        "sourceref", "hour" and "minute",
        and a fixed number of rows, depending on the regularization
        of this dataframe.
        
        - The sourcerefs are sorted in the same order as the dims_df
        - There is a row per sourceref and hour of the day (0 .. 23),
          if "hasHour".
        - There is a row per sourceref, hour and ten-minute interval
          of the day (0 .. 50), if "hasMinute"
        """
        # Now, make sure there is a metric for each
        # possible combination of dimensions, so the vector has
        # always a fixed size. Even if some of the
        # metrics are NaN (they will be considered "padding")
        fixed_df = dims_df[['sourceref']].copy()
        if self.hasHour:
            hours = tuple(range(24))
            hours_df = pd.DataFrame({'hour': hours}, index=hours)
            fixed_df = pd.merge(fixed_df, hours_df, how='cross')
        else:
            fixed_df['hour'] = 0
        if self.hasMinute:
            minutes = tuple(m*10 for m in range(6))
            minutes_df = pd.DataFrame({'minute': minutes}, index=minutes)
            fixed_df = pd.merge(fixed_df, minutes_df, how='cross')
        else:
            fixed_df['minute'] = 0
        fixed_df.reset_index(inplace=True)
        return fixed_df

    def normalize(self, fixed_df: pd.DataFrame, dataset: typing.Optional[pd.DataFrame]) -> TypedVector:
        """
        Turns a regularized dataset into a vectorized dataset, i.e.:

        - Sorts entries so that they match the order in fixed_df.
        - Makes sure the dataset has a column per dimension.
        - Fills in missing metrics for hours or minutes, with NaN.
        
        The input dataset must be regularized in time, i.e. there must
        be only one entry per "sourceref" and set of dimensions:

        - if "hasHour" is true, there must be only one entry per sourceref
          and hour
        - if "hasMinute" is true, there must be only one entry per sourceref,
          hour and ten-minute interval.

        Each dataset is regularized differently. See the documentation of
        datasets for more infor on regularization.
        """
        typed_vector = TypedVector(
            entityType=self.entityType,
            # Even if there there are no metrics, we still need
            # rows in the index to be able to add or remove entities
            # from the simulation.
            # So we clone the fixed_frame df as typed vector.
            df=fixed_df.copy(),
        )
        if self.metrics:
            # We will join the fixed_df and the dataset by
            # all the relevant dimensions, which are: sourceref,
            # hour (if hasHour), minute (if hasMinute).
            on_columns = ['sourceref']
            if self.hasHour:
                on_columns.append('hour')
            if self.hasMinute:
                on_columns.append('minute')
            # We also need to make sure the generated dataset
            # has a column per metric. If we were not given
            # any dataset, generate an empty one.
            if dataset is None:
                dataset = pd.DataFrame(columns=on_columns + list(self.metrics.keys()))
            # Finally, do the merge of the fixed_df to the metrics
            typed_vector.df = pd.merge(
                typed_vector.df,
                dataset,
                how='left',
                on=on_columns
            )
        return typed_vector

    def unpivot(self, typed_vector: TypedVector, requested_metrics: typing.Optional[typing.Sequence[str]]=None) -> pd.Series:
        """
        Unpivots a typed vector into a pd.Series that has a multi-index
        with the following values:
        (entitytype, metric, sourceref, hour, minute)

        By default, it will create rows for all the metrics supported
        by the entity type. If the parameter `metrics` is specified,
        it will ony output rows for those metrics.
        """
        vector_list = []
        # Add entityType to the dataframe. If the entity type has
        # no metrics, add a "fake" metric "_none_" with value np.NaN.
        typed_vector.df['entitytype'] = self.entityType
        metric_keys = list(self.metrics.keys())
        if not self.metrics:
            typed_vector.df['_none_'] = np.NaN
            metric_keys = ['_none_']
        elif requested_metrics:
            # Filter metric keys, but preserve order
            metric_keys = [
                m for m in metric_keys
                if m in requested_metrics
            ]
        # Turn the dataframe into a series with a
        # multilevel index. The index will have the following keys:
        # (entitytype, metric, sourceref, hour, minute)
        index_names = ['entitytype', 'metric', 'sourceref', 'hour', 'minute']
        for metric in metric_keys:
            slim_df = typed_vector.df[['entitytype', 'sourceref', 'hour', 'minute', metric]].copy()
            slim_df['metric'] = metric
            slim_df = slim_df.set_index(index_names)
            # squeeze() deprecated because it might turn a dataframe
            # into a scalar instead of a series
            # slim_series = slim_df.squeeze()
            slim_series = slim_df[metric]
            # Make sure we have squeezed correctly
            assert(isinstance(slim_series, pd.Series))
            assert(slim_series.index.names == index_names)
            assert(len(slim_df) == len(slim_series))
            vector_list.append(slim_series)
        series = pd.concat(vector_list, axis=0)
        return series

    def to_sql(self, engine: Engine, sceneref: str, dataset: Dataset, dims_df:typing.Optional[pd.DataFrame]=None, dryrun:bool=False):
        # if we get a dims_df, try to join the
        # resulting dataframe to the dim_df to pick
        # up the staticProps
        df = dataset.df
        df['entityid'] = df['sourceref']
        df['fiwareservicepath'] = '/digitaltwin'
        df['recvtime'] = dataset.timeinstant
        df['timeinstant'] = dataset.timeinstant
        df['sceneref'] = sceneref
        df['trend'] = dataset.trend
        df['daytype'] = dataset.daytype
        if dims_df is not None and self.fixedProps:
            df = pd.merge(
                df,
                dims_df[['sourceref']+list(self.fixedProps.keys())],
                how='left',
                on=['sourceref']
            )
        with engine.begin() as conn:
            kw = {
                "sceneref": sceneref,
                "timeinstant": dataset.timeinstant,
                "trend": dataset.trend,
                "daytype": dataset.daytype,
            }
            # Clear the simulation table to avoid pkey duplicates
            statement = text(
                f"""
                DELETE FROM {self.dataTableName}
                WHERE sceneref=:sceneref
                AND trend=:trend
                AND daytype=:daytype
                """).bindparams(**kw)
            with conn.execute(statement) as curr:
                curr.close()
            logging.info("saving %d rows to the database for entityType %s, dimensions %s", len(df), self.entityType, kw)
            df.to_sql(
                self.dataTableName,
                con=conn,
                if_exists='append',
                index=False,
                chunksize=1000
            )
            # Do the calculations, if needed
            expressions = []
            if self.calcs:
                for col, expr in self.calcs.items():
                    expressions.append(f"{col} = {expr}")
            if expressions:
                statement = text(f"""
                    UPDATE {self.dataTableName} SET {','.join(expressions)} 
                    WHERE sceneref=:sceneref
                    AND timeinstant=:timeinstant
                    AND trend=:trend
                    AND daytype=:daytype
                    """).bindparams(**kw)
                with conn.execute(statement) as curr:
                    curr.close()
            if dryrun:
                conn.rollback()

    def in_bbox(self, engine: Engine, sceneref: str, bbox: geometry.MultiPoint) -> typing.Sequence[str]:
        """
        Get sourceref for all entities enclosed in the given bounding box

        The bounding box object must be provided as a shapely MultiPoint.
        see https://terraformer-js.github.io/glossary/
        """
        bounds = bbox.bounds
        with engine.connect() as conn:
            bounds = bbox.bounds
            affected = text(f"""
                SELECT sourceref FROM {self.dimsTableName}
                WHERE sceneref = :sceneref AND
                location && ST_MakeEnvelope(
                    :bbox_0,
                    :bbox_1,
                    :bbox_2,
                    :bbox_3,
                    4326
                )
                """).bindparams(
                    sceneref=sceneref,
                    bbox_0=bounds[0],
                    bbox_1=bounds[1],
                    bbox_2=bounds[2],
                    bbox_3=bounds[3],
                )
            with conn.execute(affected) as cursor:
                affected_places = cursor.fetchall()
                return [place[0] for place in affected_places]

# Factor aproximado para convertir distancias en coordenadas
# a distancias en metros.
# See https://sciencing.com/convert-distances-degrees-meters-7858322.html
GEO_SCALE_FACTOR = 111139.0

@dataclass
class Reference:
    """
    Reference contains basic information about the layout
    of the city and the entities that belong to the simulation
    """

    # Metadata for all the entity types
    # that can be affected by the simulation
    metadata: typing.Mapping[str, Metadata]

    # Location of all the zones
    zones_df: pd.DataFrame

    # Distance between each pair of entities in the
    # simulation.
    distance_df: typing.Optional[pd.DataFrame] = None

    # Data for the dimensionse. Maps each entitytype
    # to all the information available for that entitytype
    # in the lastdata tables for the identity simulation
    #
    # The columns in the dataframe are those
    # returned by Metadata.dims_df
    dims_df_map: typing.Optional[typing.Dict[str, pd.DataFrame]] = None

    # Data for the scene. Maps each entitytype
    # to all the information available for that entitytype
    # in the identity simulation.
    #
    # The columns in the dataframe are those
    # returned by Metadata.scene_data
    data_df_map: typing.Optional[typing.Mapping[str, pd.DataFrame]] = None

    @staticmethod
    def create(meta_path: pathlib.Path, engine: Engine) -> 'Reference':
        """
        Create reference information for the city,
        from metadata path and database connection.

        - The metadata is read from the meta_path file.
        - The zones are loaded  the database and
          their locations converted to shapely geometries.
        """
        # Begin with metadata
        with meta_path.open(encoding='utf-8') as f:
            items = (Metadata.create(params) for params in json.load(f))
            meta = {item.entityType: item for item in items}
            meta = {k: meta[k] for k in sorted(meta.keys())}
        # zones next
        with engine.connect() as con:
            zones_df = pd.read_sql(text(f"""
                SELECT
                    entityid, zoneid, name, label,
                    ST_AsGeoJSON(ST_ConvexHull(location)) AS location
                FROM dtwin_zone_lastdata
                """),
                con=con
            )
            zones_df = geojson_to_shape(zones_df, 'location')
        return Reference(
            metadata=meta,
            zones_df=zones_df
        )

    def match_zone(self, point: geometry.Point, default: str) -> str:
        """Find the zone to which a point belongs"""
        for _, row in self.zones_df.iterrows():
            if row.location and row.location.contains(point):
                return row.zoneid
        return default

    @staticmethod
    def last_simulation(engine: Engine, sceneref: str) -> datetime:
        """Retrieve the date of the latest simulation for the given sceneref"""
        query = text(f"""
        SELECT timeinstant
        FROM dtwin_simulation_lastdata
        WHERE entityid = :sceneref
        ORDER BY timeinstant DESC
        LIMIT 1
        """)
        df = pd.read_sql(query.bindparams(sceneref=sceneref), engine)
        print(df)
        return df.iloc[0]['timeinstant']

    def calculate_distances(self, dims_df_map: typing.Mapping[str, pd.DataFrame]):
        """
        Calculate the distance between each pair of entities.

        The result is stored in the distance_df dataframe,
        that has a multiindex with 4 levels:
        (from_entitytype, from_sourceref, to_entitytype, to_sourceref)
        """
        def distance(s1, x, s2, y) -> float:
            if x is None or y is None:
                return np.NaN
            d = shapely.distance(x, y) * GEO_SCALE_FACTOR
            # Only allow 0 distance for objects with the
            # same entity id
            if d <= 0 and s1 != s2:
                return 1
            return d

        distances: typing.List[pd.DataFrame] = []
        for from_type, _ in self.metadata.items():
            from_df = dims_df_map[from_type]
            from_entities = from_df[["sourceref", "location"]].rename(columns={
                "entityid": "from_entityid",
                "sourceref": "from_sourceref",
                "location": "from_location"
            })
            from_entities['from_entitytype'] = from_type
            for to_type, _ in self.metadata.items():
                to_df = dims_df_map[to_type]
                to_entities = to_df[["sourceref", "location"]].rename(columns={
                    "entityid": "to_entityid",
                    "sourceref": "to_sourceref",
                    "location": "to_location"
                })
                to_entities['to_entitytype'] = to_type
                cross_distances = from_entities.merge(to_entities, how="cross")
                cross_distances['distance'] = cross_distances.apply(
                    lambda x: distance(x["from_sourceref"], x["from_location"], x["to_sourceref"], x["to_location"]),
                    axis=1,
                    result_type='reduce'
                )
                cross_distances = cross_distances.drop(columns=["from_location", "to_location"])
                distances.append(cross_distances)
        df = pd.concat(distances, axis=0)
        df = df.set_index(["from_entitytype", "from_sourceref", "to_entitytype", "to_sourceref"])
        self.distance_df = df

    def get_closest(self, from_type: str, from_sourceref: typing.Sequence[str], to_type: str, distance: float) -> typing.Sequence[str]:
        """Return sourceref of entities that are under distance meters close"""
        assert(self.distance_df is not None)
        distance_series = self.distance_df['distance'].dropna()
        closest: typing.Set[str] = set()
        for sourceref in from_sourceref:
            candidates = distance_series.loc[from_type, sourceref, to_type]
            candidates = candidates[candidates < distance]
            closest.update(candidates.index.get_level_values(0).values)
        return tuple(closest)

    def softmax_by_distance(self, from_type: str, from_sourceref: str, to_type: str) -> pd.Series:
        """
        Calculates the distance between the (from_type, from_sourceref)
        enity, and every other entity of type `to_type` (except itself,
        if the from_type and to_type are the same).

        Then uses softmax to generate a series with the
        normalized weights between each pair of entities.
        the returned series has a row for each `to_sourceref`
        of the given `to_type`, and is indexed by `to_sourceref`.

        This can be used to calculate a weighted average of
        some metric from other entitites, using the distance
        as the weight.
        """
        assert(self.distance_df is not None)
        distance_series = self.distance_df['distance']
        candidates = typing.cast(pd.Series, distance_series.loc[from_type, from_sourceref, to_type])
        candidates = candidates.dropna()
        assert(isinstance(candidates, pd.Series))
        if from_type == to_type:
            # remove the entity itself from the candidates
            candidates = candidates[typing.cast(pd.Series, candidates) > 0]
        max_distance = typing.cast(float, candidates.max())
        assert(isinstance(max_distance, float))
        # We want to give more weight to the closest entities,
        # so we invert the distance
        inverted_distance = torch.Tensor(candidates.apply(lambda x: max_distance / x).to_numpy())
        softmax = inverted_distance.softmax(dim=0)
        return pd.Series(softmax.numpy(), index=candidates.index)

# -------------------------------------
# Schemaless types
# -------------------------------------

@dataclass
class Vector:
    """
    Untyped Vector class.

    Contains both the complete series of metrics that make up
    the inpt of the encoder, as well as the properties of all
    TypedVectors that went into the series, particularly
    the scales and offsets.

    The index of the series is expected to be a tuple
    (entitytype, metric, sourceRef, hour, minute).
    """
    properties: typing.Mapping[str, VectorProperties]
    df: pd.Series

    @staticmethod
    def create(meta_map: typing.Mapping[str, Metadata], fixed_df_map: typing.Mapping[str, pd.DataFrame], data_map: typing.Mapping[str, Dataset]) -> 'Vector':
        """
        Created a Vector from the given set of metadata and data.
        All the maps are indexed by entity type.

        The fixed_frame for each entity type must be generated using the
        fixed_frame function.

        The data for each entity type must be generated using the
        """
        vector_list = []
        props = {}
        for entityType, meta in meta_map.items():
            entity_data = data_map.get(entityType, None)
            entity_df: typing.Optional[pd.DataFrame] = None
            if entity_data is not None:
                entity_df = entity_data.df
            typed_vector = meta.normalize(fixed_df=fixed_df_map[entityType], dataset=entity_df)
            # Copy the properties for de-escalation
            props[entityType] = VectorProperties(entityType=typed_vector.entityType)
            vector_list.append(meta.unpivot(typed_vector=typed_vector))
        vector = pd.concat(vector_list, axis=0)
        return Vector(properties=props, df=vector.astype(np.float64))

    def pivot(self, meta: Metadata, props: DatasetProperties, series: pd.Series) -> Dataset:
        """
        Pivots a pd.Series that has a multi-index with
        (entitytype, metric, sourceref, hour, minute)
        into a dataset for the given entitytupe.

        It will filter the rows for this particular entitytype, and
        then pivot the metrics so that each metric becomes a column.
        """
        typed_props = self.properties[meta.entityType]
        typed_series: pd.Series = series.loc[meta.entityType]
        metrics: typing.List[pd.Series] = []
        if meta.metrics:
            # Extract the rows corresponding to each metric
            for metric in meta.metrics.keys():
                # Get measures for the metric
                metric_series = typed_series.loc[metric]
                metric_series.name = metric
                metrics.append(metric_series)
        else:
            # If the entity type has no metrics, we still need
            # to identify the proper sourcerefs, because
            # the simulation might have added or removed
            # entities.
            # In order to do so, we remove the next level from
            # the multiindex, which in regular conditions would
            # be the metric name; and rename the columns
            # to just "_none_".
            metric_series = typed_series.loc['_none_']
            metric_series.name = '_none_'
            metrics.append(metric_series)
        # concatenate all metrics as columns
        df: pd.DataFrame = pd.concat(metrics, axis=1)
        # Drop NaN and 0, but make sure we return at least one row per
        # sourceref, otherwise the sourceref will not be present in
        # the simulation dashboard.
        groups = []
        for sourceref, group in df.groupby(level='sourceref'):
            # This filters out the rows where all values are 0
            group = group.fillna(0)
            group = group.loc[~(group == 0).all(axis=1)]
            if group.empty:
                original_group = typing.cast(pd.DataFrame, df.loc[typing.cast(str, sourceref)])
                group = original_group.head(1)
            # turn "hour" and "minute" into columns
            group = group.reset_index()
            # overwrite other columns
            group['entitytype'] = meta.entityType
            group['sourceref'] = sourceref
            groups.append(group)
        # concatenate all groups
        df = pd.concat(groups, axis=0).reset_index(drop=True)
        if '_none_' in df.columns:
            df.drop('_none_', axis=1, inplace=True)
        # Hour and minute only belong in the dataset if the
        # input has those dimensions
        if not meta.hasHour:
            df = df.drop('hour', axis=1)
        if not meta.hasMinute:
            df = df.drop('minute', axis=1)
        return Dataset(
            timeinstant=props.timeinstant,
            trend=props.trend,
            daytype=props.daytype,
            entityType=meta.entityType,
            df=df
        )

@dataclass
class HiddenLayer:
    """
    Represents the hidden layer of the autoencoder
    """
    private: torch.Tensor
    # This index describes the order in which the information is
    # layed out in the hidden layer.
    # Currently, it has the following levels:
    # (entitytype, metric, sourceref, hour, minute)
    index: pd.MultiIndex

@dataclass
class DecoderLayer:
    """
    Represents the decoder layer of the autoencoder
    """
    # This series contains the index for the output vector.
    # The series is indexed by (entityType, metric, sourceref, hour, minute)
    index: pd.MultiIndex
    # This is the decoding weights and biases
    weights: torch.Tensor
    biases: torch.Tensor
    # This is the activation function to be applied
    activation: typing.Callable[[torch.Tensor], torch.Tensor]

    def index_matching(self, entitytype: str, sourceref: str) -> pd.Series:
        """
        Find the numerical indexes in the vector_index that match the
        provided entitytype and sourceref
        """
        # Assign to each index the numerical position in the vector
        vector_offsets = pd.Series(range(0, len(self.index)), index=self.index, dtype=np.int32)
        # Filter out only those rows that match the filter
        matches = vector_offsets.loc[entitytype, :, sourceref, :, :]
        return vector_offsets[vector_offsets.isin(matches)]

    def index_except(self, entitytype: str, sourceref: str) -> pd.Series:
        """
        Find the numerical positions in the index that do not match the
        entitytype and sourceref given.
        """
        vector_offsets = pd.Series(range(0, len(self.index)), index=self.index, dtype=np.int32)
        matching = self.index_matching(entitytype=entitytype, sourceref=sourceref)
        return vector_offsets[vector_offsets.index.difference(matching.index)]

    def reductor_matrix(self, positions: pd.Series):
        """
        Generates a reductor tensor that when applied to the weights
        or biases tensors, returns a new tensor with only the rows
        that correspond to the provided positions.

        Specifically,

        - positions is a pd.Series of len M containing integer locations
          to select from the output vector, from 0 to N (N = len(vector))
        - The returned tensor is a M x N matrix
        - Multiplying the returned tensor (M x N) times the weights matrix
          (M x N) returns a new matrix (M x N) that contains only the
          selected rows of the original matrix.
        - Multiplying the returned tensor (M x N) times the biases vector
          (N x 1) returns a new vector (M x 1) that contains only the
          selected rows of the original vector.
        """
        reductor_pos = torch.tensor([range(len(positions)), positions.array])
        reductor_val = torch.ones(len(positions))
        return torch.sparse_coo_tensor(reductor_pos, reductor_val, (len(positions), len(self.index)))

    def drop_entity(self, entitytype: str, sourceref: str):
        """
        Updates the decoder so that it will disregard the results
        for the provided sourceref and entitytype
        """
        # Get the indexes that don't contain the removed entity
        preserved = self.index_except(entitytype, sourceref)
        reductor = self.reductor_matrix(preserved)
        # Build a new bias ensor with only these rows
        self.weights = torch.matmul(reductor, self.weights)
        self.biases = torch.matmul(reductor , self.biases)
        # Leave only non matching items in the index
        self.index = typing.cast(pd.MultiIndex, preserved.index)

    def decode(self, hidden: torch.Tensor) -> pd.Series:
        """
        Run the decoder over the given hidden state tensor, and return the corresponding vector
        """
        result = torch.matmul(self.weights, hidden)
        result = result + self.biases
        result = self.activation(result)
        return pd.Series(result.numpy(), index=self.index)

    @staticmethod
    def linear(x: torch.Tensor) -> torch.Tensor:
        """Default activation function, just pass-through"""
        return x

    @staticmethod
    def scaled_sigmoid(scale: int, threshold: float) -> typing.Callable[[torch.Tensor], torch.Tensor]:
        """
        Creates a scaled version of the sigmoid function that return 0 when
        the input is 0 and `theshold * scale` when the input hits
        `threshold * scale`.

        e.g. if the result should always be between 0 and 100, and be 90
        when the input is 90, then
        
        - scale must be set to 100
        - threshold must be set to 0.95

        The output will never be over scale or below 0.
        """
        def inverse_sigmoid(y: float) -> float:
            # See https://stackoverflow.com/questions/66116840/inverse-sigmoid-function-in-python-for-neural-networks
            return -math.log((1 / (y + 1e-8)) - 1)
        # we want to implement a function based on a sigmoid,
        # but that crosses the points:
        # (x = 0, y = 0)
        # (x = threshold * scale, y = threshold * scale)
        # (x = infinite, y = scale)
        #
        # This can be achieved by setting the function to:
        # y(x) = A * sigmoid (B*x + C) + D
        #
        # And chosing A, B, C and D so that the curve passes
        # through the intended points.
        #
        # We have three conditions and four degrees of freedom,
        # and we can take advantage of this, and the fact that
        # sigmoid(x) = 1 - sigmoid(-x).
        #
        # After a bit of pen and paper, it turns out that if we
        # choose one of our degrees of freedom to be:
        #
        # B = -2 * C / (threshold * scale)
        #
        # Then the conditions are satisifed by these numbers:
        C = inverse_sigmoid((1.0 - threshold) / (2.0 - threshold))
        A = (2.0 - threshold) * scale
        D = 1.0 - A
        B = (-2.0 * C) / (threshold * scale)
        def scaled_func(x: torch.Tensor, A=A, B=B, C=C, D=D):
            return A * torch.sigmoid(B * x + C) + D
        return scaled_func

class Decoder:
    """
    This class decodes the hidden layer to an output vector.
    """
    meta_map: typing.Mapping[str, Metadata]
    main_layer: DecoderLayer
    # If we add sourcerefs to the decoder, we must
    # append new rows to the output vector.
    #
    # However, we can not do it by manipulating the
    # weights and biases tensors of the main layer,
    # because the weights are currently sparse, but the
    # new sourcerefs will tipically use dense weights.
    #
    # So we keep a list of additional layers
    add_layers: typing.List[DecoderLayer]

    def __init__(self, meta_map: typing.Mapping[str, Metadata], index: pd.MultiIndex):
        """Builds the decoder with the given metadata and props"""
        self.meta_map = meta_map
        ref_length = len(index)
        # Indices of the non-zero elements (diagonal elements)
        diagonal = torch.tensor([range(ref_length), range(ref_length)])
        # Values of the non-zero elements
        values = torch.ones(ref_length)
        # Create the sparse tensor
        self.main_layer = DecoderLayer(
            index=index,
            weights=torch.sparse_coo_tensor(diagonal, values, (ref_length, ref_length)),
            biases=torch.zeros(ref_length),
            # By default, do not modify the outputs.
            activation=DecoderLayer.linear
        )
        self.add_layers = []

    def decode(self, props: DatasetProperties, hidden: HiddenLayer) -> pd.Series:
        """
        Run the decoder over the given hidden state tensor, and return the corresponding vector.
        The index of the returned series has thefollowing levels:

        ('entitytype', 'metric', 'sourceref', 'hour', 'minute')
        """
        private = torch.nan_to_num(hidden.private)
        layers = [self.main_layer]
        layers.extend(self.add_layers)
        return pd.concat((layer.decode(private) for layer in layers), axis=0)

    def drop_sourceref(self, entitytype: str, sourceref: str):
        """
        Updates the decoder so that it will disregard the results
        for the provided sourceref and entitytype
        """
        self.main_layer.drop_entity(entitytype=entitytype, sourceref=sourceref)

    def add_layer(self, layer: DecoderLayer):
        """
        Updates the decoder so that it will include the results
        for the provided index. Index includes
        (entitytype, metric, sourceref, hour and minute)

        The dimensions of the weights must be A x B, where:

        - A: length of the index.
        - B: number of rows of the hidden layer, which is also the
          width of the current weight matrix.

        The dimensions of the bias must be A x 1
        """
        # Let's calculate a reference vector for the entity type,
        # so we can make sure the sizes match
        # Compare sizes for matrix multiplication
        assert(layer.weights.shape[0] == len(layer.index))
        assert(layer.weights.shape[1] == self.main_layer.weights.shape[1])
        assert(layer.biases.shape[0] == len(layer.index))
        # We will add the data for the new entity
        # right to the end of the current index
        self.add_layers.append(layer)

    def averaged_layer(self, entitytype: str, sourceref: str) -> DecoderLayer:
        """
        Generates the index, weights and biases that have to be appended
        to the decoder for it to produce results for a new sourceref of the
        given entitytype.
        
        The weights and biases for this sourceref will be averaged
        from the weights and biases of all other sourcerefs of the same
        entitytype.
        """
        # Build a typed vector for the entitytype and sourceref
        dims_df = pd.DataFrame([sourceref], columns=['sourceref'])
        meta = self.meta_map[entitytype]
        typed_vector = meta.normalize(fixed_df=meta.get_fixed_df(dims_df), dataset=None)
        added_vector = meta.unpivot(typed_vector=typed_vector)
        assert(added_vector.index.names == ["entitytype", "metric", "sourceref", "hour", "minute"])
        # Index of rows in the bias and weights
        vector_offsets = pd.Series(
            range(0, len(self.main_layer.index)),
            index=self.main_layer.index,
            dtype=np.int32
        )
        weights = []
        biases = []
        for idx, _ in added_vector.items():
            # Find other rows for the same sourceref, hour and minute
            entitytype, metric, sourceref, hour, minute = typing.cast(tuple, idx)
            related = vector_offsets.loc[entitytype, metric, :, hour, minute]
            reductor = self.main_layer.reductor_matrix(related)
            # Append the mean of the reduced weigths and biases
            weights.append(torch.mean(torch.matmul(reductor, self.main_layer.weights).to_dense(), 0, keepdim=True))
            biases.append(torch.mean(torch.matmul(reductor , self.main_layer.biases).to_dense(), 0, keepdim=True))
        return DecoderLayer(
            index=typing.cast(pd.MultiIndex, added_vector.index),
            weights=torch.cat(weights, dim=0),
            biases=torch.cat(biases),
            activation=DecoderLayer.linear
        )

    def weighted_layer(self, entitytype: str, metric: str, sourceref: str, weights: pd.Series) -> DecoderLayer:
        """
        Generates an Entity Decoder that will produce results for a new
        entity with id `sourceref` and type `entitytype`. The new results
        will include the metric `metric`.

        The results or this decoder will be a weighhted average of
        the metrics of other entities. The weighted average is derived
        from the `weights` series provided, which must have multiindex:

        ('entitytype', 'metric', 'sourceref')

        The weights will be multiplied by the specified metrics, and
        aggregated.

        The activation function for this decoder is linear by default,
        unless the target metric has a fixed scale. In that case, the
        activation function is replaced by a scaled sigmoid to keep it
        within range.
        """
        assert(weights.index.names == ('entitytype', 'metric', 'sourceref'))
        weights.name = 'weight'
        # We want the offsets in the main decoder layer that map
        # to the entitytype, metric and sourcerefs given by the weight series
        vector_offsets = pd.Series(
            range(0, len(self.main_layer.index)),
            index=self.main_layer.index,
            dtype=np.int32
        )
        vector_offsets.name = 'offset'
        weighted_offsets = pd.merge(
            vector_offsets.reset_index(['hour', 'minute'], drop=False),
            weights,
            how='inner',
            left_index=True,
            right_index=True,
            sort=False
        ).set_index(['hour', 'minute'], append=True)
        assert(weighted_offsets.index.names == ['entitytype', 'metric', 'sourceref', 'hour', 'minute'])
        # Now get a reductor matrix for these rows only
        reductor = self.main_layer.reductor_matrix(weighted_offsets['offset'])
        assert(reductor.shape[0] == len(weighted_offsets))
        assert(reductor.shape[1] == len(self.main_layer.index))
        # The reductor matrix must be scaled by the given weights.
        # To do so, we expand the weight tensor which is [N]
        # using weights_vector[:, None] to become [N, 1], and then
        # multiply row-by-row with the reductor matrix
        weights_vector = torch.Tensor(weighted_offsets['weight'].to_numpy())
        scaled_reductor = weights_vector[:, None] * reductor
        assert(scaled_reductor.shape[0] == len(weighted_offsets))
        assert(scaled_reductor.shape[1] == len(self.main_layer.index))
        # Build a series for the target entitytype and sourceref
        dims_df = pd.DataFrame([sourceref], columns=['sourceref'])
        meta = self.meta_map[entitytype]
        typed_vector = meta.normalize(fixed_df=meta.get_fixed_df(dims_df), dataset=None)
        added_vector = meta.unpivot(typed_vector=typed_vector, requested_metrics=[metric,])
        assert(added_vector.index.names == ["entitytype", "metric", "sourceref", "hour", "minute"])
        # Now, we must match the dimensionality of the weights_tensor
        # to the dimensionalty of the added_vector.
        #
        # The added vector has a row per each valid combination of hour and
        # 10-minute interval, according to the target entitytype.
        #
        # The weights tensor has a row per each valid combination of
        # sourceref, hour and 10-minute interval, according to the
        # weighted entity types
        #
        # To make the dimensionality match, we will add per each row
        # of the added vector, all rows of the weights tensor that belong
        # to the same hour and ten-minute interval.
        hasHour = meta.hasHour
        hasMinute = meta.hasMinute
        rows = []
        for row_idx in added_vector.index:
            _, _, _, row_hour, row_minute = typing.cast(tuple, row_idx)
            row = []
            for col_idx in weighted_offsets.index:
                _, _, _, col_hour, col_minute = typing.cast(tuple, col_idx)
                match = (
                    (not hasHour) or
                    (not hasMinute and row_hour == col_hour) or
                    (row_hour == col_hour and row_minute == col_minute)
                )
                row.append(1 if match else 0)
            rows.append(row)
        agg_tensor = torch.Tensor(rows)
        assert(agg_tensor.shape[0] == len(added_vector))
        assert(agg_tensor.shape[1] == len(weighted_offsets))
        agg_reductor = torch.matmul(agg_tensor, scaled_reductor)
        agg_tensor = torch.matmul(agg_reductor, self.main_layer.weights)
        agg_bias = torch.matmul(agg_reductor, self.main_layer.biases)
        # If the target metric is scaled, use a compression
        # activation function so it does not excede the scale
        activation: typing.Callable[[torch.Tensor], torch.Tensor] = DecoderLayer.linear
        scale = self.meta_map[entitytype].metrics[metric].scale
        if scale:
            activation = DecoderLayer.scaled_sigmoid(scale, 0.9)
        return DecoderLayer(
            index=typing.cast(pd.MultiIndex, added_vector.index),
            weights=agg_tensor,
            biases=agg_bias,
            activation=activation
        )

@dataclass
class SimulationProperties:
    """
    Contains properties related to the simulation:
    sceneref, timestamp, name, etc.
    """
    # ID y Fecha de la vista identidad en la que se basa esta simulacion
    identityref: str
    identity_date: datetime
    # Datos de la simulacion
    sceneref: str
    entitytype: str
    sim_date: datetime
    name: str
    description: str
    location: typing.Any
    settings: typing.Sequence[typing.Any]

    @staticmethod
    def create(broker: Broker, identityref: str, identity_date: datetime, fallback: typing.Any=None) -> typing.Optional['SimulationProperties']:
        """Fetch simulation data from context broker"""
        sim_type = os.getenv("ETL_VECTORIZE_SIMULATION_TYPE")
        sim_id = os.getenv("ETL_VECTORIZE_SIMULATION_ID")
        entity = fallback
        if broker.cb is not None and sim_type and sim_id:
            entity = broker.fetch_one(entitytype=sim_type, entityid=sim_id)
        if not entity:
            return None
        sceneref = entity['id']
        return SimulationProperties(
            identityref=identityref,
            identity_date=identity_date,
            sceneref=sceneref,
            entitytype=entity['type'],
            sim_date=datetime.fromisoformat(entity.get('timestamp', datetime.now().isoformat())),
            name=entity.get('name', {}).get('value', sceneref),
            description=entity.get('description', {}).get('value', ''),
            location=entity.get('location', {}).get('value', None),
            settings=(entity,),
        )

    def feedback(self, broker: Broker, status: str, *args):
        """Send feedback to the broker"""
        broker.push(entities=[{
            'id': self.sceneref,
            'type': self.entitytype,
            'status': {
                'type': 'TextUnrestricted',
                'value': status % args
            }
        }])

    def to_sql(self, engine: Engine, dryrun: bool=False):
        """Save simulation information to lastdata table"""
        with engine.begin() as conn:
            query = text(f"""
                INSERT INTO dtwin_simulation_lastdata (
                    entityid,
                    entitytype,
                    timeinstant,
                    name,
                    description,
                    location,
                    recvtime,
                    fiwareservicepath
                )
                VALUES (
                    :sceneref, 'Simulation', :datesim, :name, :description,
                    ST_GeomFromGeoJSON(:location), NOW(), '/digitaltwin'
                )
                ON CONFLICT(entityid) DO UPDATE SET
                    timeinstant = EXCLUDED.timeinstant,
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    recvtime = NOW(),
                    location = EXCLUDED.location,
                    fiwareservicepath = '/digitaltwin'
                """)
            conn.execute(query.bindparams(
                sceneref=self.sceneref,
                datesim=self.sim_date,
                name=self.name,
                description=self.description,
                location=json.dumps(self.location)
            ))
            if dryrun:
                conn.rollback()

    def to_broker(self, broker: Broker):
        """
        Update simulation data in orion.
        This is only done when we need to manipulate the location.
        """
        if self.location is None:
            return
        broker.push(entities=[{
            'id': self.sceneref,
            'type': self.entitytype,
            'location': self.location
        }])

    def signature(self) -> str:
        """Return simulationsignature, for logging purposes"""
        return f"{self.sceneref} - {self.sim_date}"

class Simulation(typing.Protocol):
    """
    Protocol to represent the simulation API
    """

    def add_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        """
        Add any entities created by the simulation to the dims_df_map and,
        if needed, to the database or broker.
        
        Might create rows, update entities, or add information to
        the dimension table if needed for the simulation.
        """

    def drop_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        """
        Remove any entities destroyed by the simulation from the dims_df_map and,
        if needed, from the database or broker.
        
        Might create rows, update entities, or add information to
        the dimension table if needed for the simulation.
        """

    def prepare_decoder(self, reference: Reference, decoder: Decoder):
        """
        Prepare the decoder for simulation

        Might update the decoder layers to add or remove
        entities from the decoder output
        """
        pass

    def perturb_hidden(self, props: DatasetProperties, hidden: HiddenLayer) -> HiddenLayer:
        """
        Updates the hidden layer to reflect the impact
        of the simulation in the city status
        """
        return hidden

    def vet_output(self, result: pd.Series) -> pd.Series:
        """
        Vets the output of the simulation,
        potentially changing values that deviate
        from reasonable expections (e.g. percent > 100%)
        """
        return result

def main(reference: Reference, engine: Engine, broker: Broker, fallback: typing.Optional[str]=None, dryrun: bool=False):
    """
    Vectorizes the data in the database
    """
    fallback_sim: typing.Any = None
    if fallback:
        logging.info("using fallback simulation %s", fallback)
        with pathlib.Path(fallback).open(encoding='utf-8') as f:
            fallback_sim = json.load(f)
    start = datetime.now()

    # Get the latest identity we are working with
    identityref = os.getenv("ETL_VECTORIZE_IDENTITYREF", "N/A")
    last_identity_date = Reference.last_simulation(engine=engine, sceneref=identityref)
    logging.info("Latest identity data %s: %s", identityref, last_identity_date)

    # Get the simulation properties
    sim_props = SimulationProperties.create(broker=broker, identityref=identityref, identity_date=last_identity_date, fallback=fallback_sim)
    if not sim_props:
        logging.warning("No simulation found")
        return
    sim_props.feedback(broker, "initiating simulation")
    sim_handlers = list(create_simulators(reference=reference, sim_props=sim_props, engine=engine))

    # Collect data for all the combinations of trend and daytype
    scene_variations: typing.Dict[typing.Tuple[str, str], typing.List[str]] = defaultdict(list)
    dims_df_map: typing.Dict[str, pd.DataFrame] = {}
    fixed_df_map: typing.Dict[str, pd.DataFrame] = {}
    data_df_map: typing.Dict[str, pd.DataFrame] = {}
    for entitytype, meta in reference.metadata.items():
        dims_df = meta.get_dim_df(engine=engine, sceneref=identityref)
        logging.info("Dims shape for scene %s, timeinstant %s, entity type %s: %s", identityref, last_identity_date, entitytype, dims_df.shape)
        dims_df_map[entitytype] = dims_df
        fixed_df = meta.get_fixed_df(dims_df)
        logging.info("Fixed shape for scene %s, timeinstant %s, entity type %s: %s", identityref, last_identity_date, entitytype, fixed_df.shape)
        fixed_df_map[entitytype] = fixed_df
        scene_df = meta.get_scene_df(engine=engine, sceneref=identityref, timeinstant=last_identity_date)
        for _, cols in scene_df[['trend', 'daytype']].drop_duplicates().iterrows():
            scene_variations[(cols['trend'], cols['daytype'])].append(entitytype)
        logging.info("Data shape for scene %s, timeinstant %s, entity type %s: %s", identityref, last_identity_date, entitytype, scene_df.shape)
        data_df_map[entitytype] = scene_df
    logging.info("scene variations for scene %s, timeinstant %s: %s", identityref, last_identity_date, scene_variations)

    # Save references to dimulation dims and facts
    reference.dims_df_map = dims_df_map
    reference.data_df_map = data_df_map

    # Handle adding entities to the scene
    logging.info("Creating simulation entities for %s", sim_props.signature())
    for handler in sim_handlers:
        handler.add_entities(engine=engine, broker=broker, reference=reference, dryrun=dryrun)

    # Calculate distances across all points.
    logging.info("Calculating distances for %s", sim_props.signature())
    reference.calculate_distances(dims_df_map)
    if reference.distance_df is not None:
        distance_df_path = "distance_df.csv"
        reference.distance_df.to_csv(distance_df_path)

    # Handle removing entities from the scene
    logging.info("Removing simulation entities for %s", sim_props.signature())
    for handler in sim_handlers:
        handler.drop_entities(engine=engine, broker=broker, reference=reference, dryrun=dryrun)

    # Update the simulation table from the ETL
    sim_props.to_sql(engine=engine, dryrun=dryrun)

    # Create the decoder. Apply all simulation modifications.
    logging.info("Preparing decoder for %s", sim_props.signature())
    empty_vector = Vector.create(meta_map=reference.metadata, fixed_df_map=fixed_df_map, data_map={})
    decoder = Decoder(meta_map=reference.metadata, index=typing.cast(pd.MultiIndex, empty_vector.df.index))
    for handler in sim_handlers:
        handler.prepare_decoder(reference=reference, decoder=decoder)

    # Iterate over all combinations of trend and daytype
    for scene_index, entitytypes in scene_variations.items():
        trend, daytype = scene_index
        logging.info("Iterating on scene %s, trend %s, daytype %s", sim_props.signature(), trend, daytype)
        # Separate data by trend and daytype
        data_map: typing.Dict[str, Dataset] = {}
        for entitytype in entitytypes:
            scene_df = data_df_map[entitytype]
            scene_df = scene_df[(scene_df['trend'] == trend) & (scene_df['daytype'] == daytype)]
            data_map[entitytype] = Dataset(
                timeinstant=last_identity_date,
                trend=trend,
                daytype=daytype,
                entityType=entitytype,
                df=scene_df.copy()
            )
        # Collect all simulation data into a vector
        vector = Vector.create(meta_map=reference.metadata, fixed_df_map=fixed_df_map, data_map=data_map)
        logging.info("Vector shape for scene %s, timeinstant %s, trend %s, daytype %s: %s",
            sim_props.sceneref,
            last_identity_date,
            trend,
            daytype,
            vector.df.shape
        )
        sim_props.feedback(broker, "vector shape %s", vector.df.shape)

        # Write input vector for debugging purposes
        # input_vector_path = f"input_vector_{trend}_{daytype}.csv"
        # logging.info("Saving input vector to %s", input_vector_path)
        # vector.df.to_csv(input_vector_path)

        # Encode and update hidden state
        dataset_props = DatasetProperties(
            timeinstant=sim_props.sim_date,
            trend=trend,
            daytype=daytype
        )
        hidden = encode_vector(metadata=meta, props=dataset_props, vector=vector)
        logging.info("Hidden shape for scene %s, timeinstant %s, trend %s, daytype %s: %s",
            sim_props.sceneref,
            last_identity_date,
            trend,
            daytype,
            hidden.private.shape
        )
        sim_props.feedback(broker, "hidden shape %s", hidden.private.shape)

        for handler in sim_handlers:
            hidden = handler.perturb_hidden(props=dataset_props, hidden=hidden)
        logging.info("Simulated state shape for scene %s, timeinstant %s, trend %s, daytype %s: %s",
            sim_props.sceneref,
            last_identity_date,
            trend,
            daytype,
            hidden.private.shape
        )
        sim_props.feedback(broker, "simulated state shape %s", hidden.private.shape)

        # Decode the hidden status and vet the results
        result = decoder.decode(props=dataset_props, hidden=hidden)
        for handler in sim_handlers:
            result = handler.vet_output(result)
        logging.info("Simulated result shape for scene %s, timeinstant %s, trend %s, daytype %s: %s",
            sim_props.sceneref,
            last_identity_date,
            trend,
            daytype,
            result.shape
        )
        sim_props.feedback(broker, "simulated result shape %s", result.shape)

        # Write output vector for debugging purposes
        # output_vector_path = f"output_vector_{trend}_{daytype}.csv"
        # logging.info("Saving output vector to %s", output_vector_path)
        # result.to_csv(output_vector_path)

        # Split into Datasets to save back to the database
        for entityType, meta in reference.metadata.items():
            dataset = vector.pivot(meta=meta, props=dataset_props, series=result)
            dims_df = dims_df_map[entityType]
            meta.to_sql(engine=engine, sceneref=sim_props.sceneref, dataset=dataset, dims_df=dims_df, dryrun=dryrun)

    stop = datetime.now()
    logging.info("Total memory usage: %s", psutil.Process().memory_info().rss)
    sim_props.feedback(broker, f"done in {stop - start}")

def encode_vector(metadata: Metadata, props: DatasetProperties, vector: Vector) -> HiddenLayer:
    """
    Run the encoder over the given vector, and return the corresponding hidden states
    """
    return HiddenLayer(
        private=torch.Tensor(vector.df.to_numpy()),
        index=typing.cast(pd.MultiIndex, vector.df.index)
    )

def create_simulators(reference: Reference, sim_props: SimulationProperties, engine: Engine) -> typing.Iterable[Simulation]:
    for sim in sim_props.settings:
        if sim['type'] == 'SimulationParking':
            logging.info("SimulationParking")
            yield SimParking(reference=reference, sim_props=sim_props, sim=sim)
        elif sim['type'] == 'SimulationTraffic':
            logging.info("SimulationParking")
            yield SimTraffic(reference=reference, sim_props=sim_props, sim=sim)
        elif sim['type'] == 'SimulationRoute':
            logging.info("SimulationParking")
            yield SimRoute(reference=reference, sim_props=sim_props, sim=sim, engine=engine)
        else:
            logging.warn("unrecognized simulation info: %s", sim)
        return None

class SimParking:
    """Simulation for parking creation"""

    def __init__(self, reference: Reference, sim_props: SimulationProperties, sim: typing.Any):
        self.sim_date = sim_props.sim_date
        self.entitytype = "OffStreetParking"
        self.sceneref = sim_props.sceneref
        self.sourceref = f"{self.sceneref}_{self.sim_date.strftime('%Y_%m_%d')}"
        self.name = sim.get('name', {}).get('value', '')
        self.location = sim.get('location', {}).get('value', {})
        self.capacity = int(sim.get('capacity', {}).get('value', '1000'))
        self.bias = int(sim.get('bias', {}).get('value', 5))

    def add_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        # Add a new parking to the dims_df_map
        assert(reference.dims_df_map is not None)
        metadata = reference.metadata[self.entitytype]
        dims_df = reference.dims_df_map[self.entitytype]
        zone = reference.match_zone(geometry.shape(self.location), "1")
        new_parking = {
            'sourceref': self.sourceref,
            'zone': zone,
            'zonelist': [zone],
            'location': geometry.shape(self.location),
            'capacity': self.capacity,
        }
        assert(frozenset(dims_df.columns).issuperset(new_parking.keys()))
        reference.dims_df_map[self.entitytype] = pd.concat([
            dims_df,
            pd.DataFrame([tuple(new_parking.values())], columns=tuple(new_parking.keys()))
        ], axis=0)
        # Save the new parking to the database
        with engine.begin() as conn:
            # Remove the simulated parking, if it exists
            statement = text(f"DELETE FROM {metadata.dimsTableName} WHERE sourceref = :sourceref")
            with conn.execute(statement.bindparams(sourceref=self.sourceref)) as cursor:
                cursor.close()
            statement = text(f"""
                INSERT INTO {metadata.dimsTableName} (
                    timeinstant, entityid, entitytype, recvtime, fiwareservicepath,
                    sourceref, sceneref, zone, location,
                    name, capacity
                ) VALUES (
                    :timeinstant, :entityid, :entitytype, :recvtime,  :fiwareservicepath,
                    :sourceref, :sceneref, :zone, ST_GeomFromGeoJSON(:location),
                    :name, :capacity
                )
                """)
            bound = statement.bindparams(
                timeinstant=self.sim_date,
                entityid=self.sourceref,
                entitytype=self.entitytype,
                recvtime=self.sim_date,
                fiwareservicepath="/digitaltwin",
                sourceref=self.sourceref,
                sceneref=self.sceneref,
                zone=zone,
                location=json.dumps(self.location),
                name=self.name,
                capacity=self.capacity,
            )
            with conn.execute(bound) as cursor:
                cursor.close()
            if dryrun:
                conn.rollback()

    def drop_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        pass

    def prepare_decoder(self, reference: Reference, decoder: Decoder):
        # Get weights to calculate the ocupation of the new
        # parking as a weighted average of the occupations of the
        # existing parkings, weighted by distance
        distance_averages = reference.softmax_by_distance('OffStreetParking', self.sourceref, 'OffStreetParking')
        assert(distance_averages.index.names == ['to_sourceref'])
        distance_averages.name = 'weight'
        # Scale the weights by the relative capacities
        # of the parkings
        assert(reference.dims_df_map is not None)
        parkings = reference.dims_df_map['OffStreetParking'].set_index('sourceref')['capacity']
        capacities = pd.merge(distance_averages, parkings, how='left', left_index=True, right_index=True, sort=False)
        assert(capacities.index.names == ['to_sourceref'])
        assert(capacities.columns.to_list() == ['weight', 'capacity'])
        capacities['weight'] = capacities.apply(lambda x: x['weight'] * x['capacity'] / self.capacity, axis=1)
        # Generate the weights series
        weights = capacities.reset_index()
        weights['entitytype'] = 'OffStreetParking'
        weights['sourceref'] = weights['to_sourceref']
        weights['metric'] = 'occupationpercent'
        weights = weights.set_index(['entitytype', 'metric', 'sourceref'])
        weights_series = weights['weight']
        # Apply the weights series to the "occupationpercent"
        # metric of the entitytype
        decoder.add_layer(decoder.weighted_layer(self.entitytype, 'occupationpercent', self.sourceref, weights_series))

    def perturb_hidden(self, props: DatasetProperties, hidden: HiddenLayer) -> HiddenLayer:
        # Produce an impact on other things close to the parking
        return hidden

    def vet_output(self, result: pd.Series) -> pd.Series:
        return result

class SimTraffic:
    """Simulation for traffic affectation"""

    def __init__(self, reference: Reference, sim_props: SimulationProperties, sim: typing.Any):
        self.sim_date = sim_props.sim_date
        self.sceneref = sim_props.sceneref
        self.name = sim.get('name', {}).get('value', '')
        self.capacity = int(sim.get('capacity', {}).get('value', '1000'))
        self.bias = int(sim.get('bias', {}).get('value', 5))
        self.category = sim.get('category', {}).get('value', 'pedestrian').lower().strip()
        self.bbox = shapely.MultiPoint(sim.get('location').get('value', [[0,0],[0,0]]))
        # Save location to sim_props, so that it can be used
        # in the database.
        sim_props.location = json.loads(shapely.to_geojson(self.bbox))

    def add_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        pass

    def drop_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        identityref = 'N/A'
        self.affected_places = reference.metadata['TrafficCongestion'].in_bbox(engine=engine, sceneref=identityref, bbox=self.bbox)
        logging.info("Affected TrafficCongestion entities: %s", ", ".join(self.affected_places))
        # Locate all TrafficIntensity entities close enough to any of the affected entities
        self.related_places = reference.get_closest(
            from_type='TrafficCongestion',
            from_sourceref=self.affected_places,
            to_type='TrafficIntensity',
            distance=10 # meters
        )
        logging.info("Related TrafficIntensity entities: %s", ", ".join(self.related_places))

    def prepare_decoder(self, reference: Reference, decoder: Decoder):
        if self.affected_places:
            for place in self.affected_places:
                decoder.drop_sourceref('TrafficCongestion', place)
        if self.related_places:
            for place in self.related_places:
                decoder.drop_sourceref('TrafficIntensity', place)

    def perturb_hidden(self, props: DatasetProperties, hidden: HiddenLayer) -> HiddenLayer:
        # Produce an impact on other things close to the parking
        return hidden

    def vet_output(self, result: pd.Series) -> pd.Series:
        return result

class SimRoute:
    """Simulation for route affectation"""

    def __init__(self, reference: Reference, sim_props: SimulationProperties, sim: typing.Any, engine: Engine):
        self.sim_props = sim_props
        self.sceneref = sim_props.sceneref
        self.sim_date = sim_props.sim_date
        self.trips = float(sim.get('trips', {}).get('value', 100))
        self.intensity = float(sim.get('intensity', {}).get('value', 1000))
        self.bias = int(sim.get('bias', {}).get('value', 5))
        self.sim_id = sim['id']
        self.sim_type = sim['type']
        self.sourceref = f"{self.sceneref}_{self.sim_date.strftime('%Y_%m_%d')}"

    def add_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        assert(reference.dims_df_map is not None)
        # Rename stops and associate to the proper sourceref
        stops = broker.fetch(entitytype='Stop', q="refSimulation:none")
        if not stops:
            raise ValueError("No stops found for %s", self.sceneref)
        # Sort the stops in order of creation
        sorted_stops = sorted(stops, key=lambda s: s['TimeInstant']['value'])
        sorted_ids = [stop['id'] for stop in sorted_stops]
        logging.info("SimRoute: sorted stops = %s", sorted_ids)
        # Get the zone of each stop
        coords: typing.List[typing.Any] = []
        zones: typing.List[str] = []
        for stop in sorted_stops:
            stop['id'] = f"{self.sourceref}_{stop['id']}"
            stop['refSimulation'] = {
                'type': 'Text',
                'value': self.sim_id
            }
            coord = stop['location']['value']
            coords.append(coord)
            zones.append(reference.match_zone(point=geometry.shape(coord), default="1"))
        location = {
            'type': 'MultiLineString',
            'coordinates': [[c['coordinates'] for c in coords]]
        }
        self.sim_props.location = location
        # Update the simulation entity with the line
        if not dryrun:
            logging.info("SimRoute: Updating geometry in entity %s of type %s", self.sim_id, self.sim_type)
            broker.push(entities=[{
                'id': self.sim_id,
                'type': self.sim_type,
                'location': {
                    'type': 'geo:json',
                    'value': location
                }
            }])
            # Remove stops
            logging.info("SimRoute: pushing %d stops", len(stops))
            broker.push(stops)
            logging.info("SimRoute: removing stops with refSimulation: none")
            broker.delete("Stop", q="refSimulation:none")
        # Count zones and get most repeated
        zone_count = sorted(((count, zone) for zone, count in Counter(zones).items()), reverse=True)
        zone = zone_count[0][1]
        zonelist = list(frozenset(zones))
        # Add new Routes to the dims_df_map
        forwardstops = len(coords)
        returnstops = len(coords)
        new_route = {
            'sourceref': self.sourceref,
            'zone': zone,
            'zonelist': zonelist,
            'location': geometry.shape(location),
            'forwardstops': forwardstops,
            'returnstops': returnstops,
        }
        logging.info("SimRoute: new route = %s", new_route)
        with engine.begin() as conn:
            for entitytype in ('RouteSchedule', 'RouteIntensity'):
                dims_df = reference.dims_df_map[entitytype]
                assert(frozenset(dims_df.columns).issuperset(new_route.keys()))
                reference.dims_df_map[entitytype] = pd.concat([
                    dims_df,
                    pd.DataFrame([tuple(new_route.values())], columns=tuple(new_route.keys()))
                ], axis=0)
                # Save the new parking to the database
                metadata = reference.metadata[entitytype]
                statement = text(f"DELETE FROM {metadata.dimsTableName} WHERE sourceref = :sourceref")
                with conn.execute(statement.bindparams(sourceref=self.sourceref)) as cursor:
                    cursor.close()
                statement = text(f"""
                    INSERT INTO {metadata.dimsTableName} (
                        timeinstant, entityid, entitytype, recvtime, fiwareservicepath,
                        sourceref, sceneref, zone, zonelist, location,
                        name, forwardstops, returnstops
                    ) VALUES (
                        :timeinstant, :entityid, :entitytype, :recvtime,  :fiwareservicepath,
                        :sourceref, :sceneref, :zone, CAST(:zonelist AS jsonb), ST_GeomFromGeoJSON(:location),
                        :name, :forwardstops, :returnstops
                    )
                    """)
                bound = statement.bindparams(
                    timeinstant=self.sim_date,
                    entityid=self.sourceref,
                    entitytype=entitytype,
                    recvtime=self.sim_date,
                    fiwareservicepath="/digitaltwin",
                    sourceref=self.sourceref,
                    sceneref=self.sceneref,
                    zone=zone,
                    zonelist=json.dumps(zonelist),
                    location=json.dumps(location),
                    name=self.sourceref,
                    forwardstops=forwardstops,
                    returnstops=returnstops,
                )
                with conn.execute(bound) as cursor:
                    cursor.close()
            if dryrun:
                conn.rollback()

    def drop_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        pass

    def prepare_decoder(self, reference: Reference, decoder: Decoder):
        # Add a new layer for the new parking, averaging the
        # values of the other parkings
        # get the average intensity, forwardtrips and returntrips per route
        assert(reference.data_df_map is not None)
        entities = reference.data_df_map['RouteIntensity'][['sourceref', 'intensity', 'forwardtrips', 'returntrips']].groupby('sourceref').mean()
        assert(entities.index.names == ['sourceref'])
        distance_averages = reference.softmax_by_distance('RouteIntensity', self.sourceref, 'RouteIntensity')
        assert(distance_averages.index.names == ['to_sourceref'])
        distance_averages.name = 'weight'
        # Prepare dataframe with the scale of each route, both
        # intensity and number of trips
        capacities = pd.merge(distance_averages.to_frame(), entities, how='left', left_index=True, right_index=True, sort=False)
        assert(capacities.index.names == ['to_sourceref'])
        assert(capacities.columns.to_list() == ['weight', 'intensity', 'forwardtrips', 'returntrips'])
        capacities = capacities.reset_index()
        capacities['sourceref'] = capacities['to_sourceref']
        capacities['intensity_scale'] = capacities.apply(lambda x: self.intensity / x['intensity'], axis=1)
        capacities['trips_scale'] = capacities.apply(lambda x: self.trips / (x['forwardtrips'] + x['returntrips']), axis=1)
        # Prepare weights for each metric
        capacities['intensity_weight'] = capacities.apply(lambda x: x['intensity_scale'] * x['weight'], axis=1)
        capacities['trips_weight'] = capacities.apply(lambda x: x['trips_scale'] * x['weight'], axis=1)
        # We need to add a layer per entity type and metric
        layers = {
            'RouteSchedule': {
                'forwardtrips': 'trips_weight',
                'returntrips': 'trips_weight'
            },
            'RouteIntensity': {
                'forwardtrips': 'trips_weight',
                'returntrips': 'trips_weight',
                'intensity': 'intensity_weight'
            }
        }
        for entitytype, metrics in layers.items():
            for metric, weight in metrics.items():
                metric_cap = capacities
                metric_cap['entitytype'] = entitytype
                metric_cap['metric'] = metric
                metric_cap = metric_cap.set_index(['entitytype', 'metric', 'sourceref'])
                metric_weights = metric_cap[weight]
                decoder.add_layer(decoder.weighted_layer(entitytype, metric, self.sourceref, metric_weights))

    def perturb_hidden(self, props: DatasetProperties, hidden: HiddenLayer) -> HiddenLayer:
        return hidden

    def vet_output(self, result: pd.Series) -> pd.Series:
        return result

if __name__ == "__main__":
    logging.basicConfig(
        level= os.getenv('ETL_LOG_LEVEL', 'DEBUG'),
        format="time=%(asctime)s | lvl=%(levelname)s | comp=ETL-DIGITALTWIN-VECTORIZE | op=%(name)s:%(filename)s[%(lineno)d]:%(funcName)s | msg=%(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="append", nargs=1)
    parser.add_argument("-m", "--meta", default="meta.json")
    parser.add_argument("-d", "--dryrun", action="store_true", default=False)
    parser.add_argument("-f", "--fallback")
    args = parser.parse_args()

    for config in args.config:
        logging.debug("loading config file %s", config)
        loadConfig(pathlib.Path(config[0]))
    logging.info("Configuration:\n%s", json.dumps(dumpConfig(), indent=2))

    try:
        with ExitStack() as stack:
            engine = stack.enter_context(psql_engine())
            broker = stack.enter_context(orion_engine())
            reference = Reference.create(meta_path=pathlib.Path(args.meta), engine=engine)
            logging.info("Metadata order:\n%s", ", ".join(reference.metadata.keys()))
            main(reference, engine, broker, args.fallback, args.dryrun)
        logging.info("ETL OK")
    except Exception as err:
        logging.exception(msg="Error during vectorization", stack_info=True)
        sys.exit(-1)
