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
from dataclasses import dataclass, replace
from contextlib import contextmanager, ExitStack
from collections import defaultdict, Counter
from sqlalchemy import create_engine, event, text, URL, Engine, Connection,TextClause
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
            sleep_send_batch=int(os.getenv('ETL_VECTORIZE_SLEEP_SEND_BATCH', '1')),
            timeout=int(os.getenv('ETL_VECTORIZE_TIMEOUT', '10')),
            post_retry_connect=float(os.getenv('ETL_VECTORIZE_POST_RETRY_CONNECT', '3')),
            post_retry_backoff_factor=float(os.getenv('ETL_VECTORIZE_POST_RETRY_BACKOFF_FACTOR', '2')),
            batch_size=int(os.getenv('ETL_VECTORIZE_BATCH_SIZE', '20')),
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

    def change_time(self, must_have_hour: bool, must_have_minute: bool) -> pd.DataFrame:
        """
        Return a new DataFrame where the `hour` and `minute` columns
        are changed to reflect the new values of `hasHour` and `hasMinute`.
        """
        result_df = self.df
        minute_df = pd.DataFrame([10 * i for i in range(0, 6)], columns=('minute',))
        hour_df = pd.DataFrame(list(range(0, 24)), columns=('hour',))
        hasMinute = ('minute' in self.df.columns)
        hasHour = ('hour' in self.df.columns)
        if must_have_minute:
            assert(must_have_hour)
            # We need to expand the DataFrame to one row
            # per hour and to-minute interval, optionally
            # filling the gaps with copies.
            if not hasMinute:
                result_df = pd.merge(result_df, minute_df, how='cross')
            if not hasHour:
                assert(not hasMinute)
                result_df = pd.merge(result_df, hour_df, how='cross')
        elif must_have_hour:
            # We need to adjust the perturb df to one row
            # per hour, potentially copying or aggregating
            # rows depending on whether the pertur metadata
            # hasHour and hasMinute.
            if hasMinute:
                assert(hasHour)
                # The "mean" below won't drop the minute because it is numeric,
                # so we must drop it beforehand.
                result_df = result_df.drop(columns=['minute'])
                result_df = result_df.groupby(by=['sourceref', 'hour']).mean(numeric_only=True)
            elif not hasHour:
                assert(not hasMinute)
                result_df = pd.merge(result_df, hour_df, how='cross')
        elif hasMinute or hasHour:
            # The "mean" below won't drop the hour and minute because they are numeric,
            # so we must drop them beforehand.
            result_df = result_df.drop(columns=['hour', 'minute'])
            result_df = result_df.groupby(by=['sourceref']).mean(numeric_only=True)
        return result_df

@dataclass
class TypedVector:
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
    entitytype: str
    df: pd.DataFrame

# -------------------------------------
# Schema bearing types
# -------------------------------------

@dataclass
class Metric:
    """
    Describes properties of a metric
    """
    ngsiType: str
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
    non_metrics: typing.Dict[str, str]
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

    def with_interval(self, hasHour: bool, hasMinute: bool) -> 'Metadata':
        return replace(self, hasHour=hasHour, hasMinute=hasMinute)

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
        fixed_df.reset_index(inplace=True, drop=True)
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
            entitytype=self.entityType,
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

    def embed(self, fixed_df: pd.DataFrame, dataset: typing.Optional[pd.DataFrame], requested_metrics: typing.Optional[typing.Sequence[str]]=None) -> pd.Series:
        """
        Embeds a Dataset into a one-dimensional vector.

        Currently, the embedding is a combination of normalizing the dataset to
        have one row per time step, and unpivoting it to make the metrics go into
        separate rows.
        """
        return self.unpivot(self.normalize(fixed_df=fixed_df, dataset=dataset), requested_metrics=requested_metrics)

    def pivot(self, props: DatasetProperties, series: pd.Series) -> Dataset:
        """
        Pivots a pd.Series that has a multi-index with
        (metric, sourceref, hour, minute)
        into a dataset for the given entitytype.

        It will filter the rows for this particular entitytype, and
        then pivot the metrics so that each metric becomes a column.
        """
        assert(series.index.names == ['metric', 'sourceref', 'hour', 'minute'])
        typed_series: pd.Series = series
        metrics: typing.List[pd.Series] = []
        if self.metrics:
            # Extract the rows corresponding to each metric
            for metric in self.metrics.keys():
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
            group['entitytype'] = self.entityType
            group['sourceref'] = sourceref
            groups.append(group)
        # concatenate all groups
        df = pd.concat(groups, axis=0).reset_index(drop=True)
        if '_none_' in df.columns:
            df.drop('_none_', axis=1, inplace=True)
        # Hour and minute only belong in the dataset if the
        # input has those dimensions
        if not self.hasHour:
            df = df.drop('hour', axis=1)
        if not self.hasMinute:
            df = df.drop('minute', axis=1)
        return Dataset(
            timeinstant=props.timeinstant,
            trend=props.trend,
            daytype=props.daytype,
            entityType=self.entityType,
            df=df
        )

    def clean_sql(self, conn: Connection, sceneref: str, trend: typing.Optional[str]=None, daytype: typing.Optional[str]=None, dims_also: bool=False):
        """Remove simulation data from database"""
        assert(sceneref is not None and sceneref != 'N/A')
        kw: typing.Dict[str, typing.Any] = {
            "sceneref": sceneref
        }
        # Add optional filters
        statement = f"DELETE FROM {self.dataTableName} WHERE sceneref=:sceneref"
        for key, val in { 'trend': trend, 'daytype': daytype }.items():
            if val is not None:
                statement = statement + f" AND {key}=:{key}"
                kw[key] = val
        # Clear the simulation table to avoid pkey duplicates
        sql = text(statement).bindparams(**kw)
        with conn.execute(sql) as curr:
            curr.close()
        if dims_also and trend is None and daytype is None:
            # Remove from dims table too
            statement = f"DELETE FROM {self.dimsTableName} WHERE sceneref=:sceneref"
            with conn.execute(text(statement).bindparams(sceneref=sceneref)) as curr:
                curr.close()

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
            # Clear the simulation table to avoid pkey duplicates
            self.clean_sql(conn, sceneref=sceneref, trend=dataset.trend, daytype=dataset.daytype)
            kw: typing.Dict[str, typing.Any] = {
                "timeinstant": dataset.timeinstant,
                "sceneref": sceneref,
                "trend": dataset.trend,
                "daytype": dataset.daytype,
            }
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

    def merge_fixed_props(self, data_df: typing.Union[pd.Series, pd.DataFrame], dims_df: pd.DataFrame, how='left') -> pd.DataFrame:
        """
        Merge a series with the fixedProps properties
        obtained from the dims_df.

        - The data_df must be indexed at least by sourceref.
          It can optionally have other levels (e.g. hour, minute)
        - The result is a dataframe eith the same index as
          the data_df, and a column per fixedProperty.
        """
        if not self.fixedProps:
            if isinstance(data_df, pd.Series):
                return data_df.to_frame()
            return typing.cast(pd.DataFrame, data_df)
        merged = pd.merge(
            left=data_df,
            right=dims_df[['sourceref'] + list(self.fixedProps.keys())].set_index('sourceref'),
            how=how,
            left_index=True,
            right_index=True,
            sort=False
        )
        assert(data_df.index.names == merged.index.names)
        return merged

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
    zones_df: typing.Optional[pd.DataFrame] = None

    # Distance between each pair of entities in the
    # simulation. It has a multiindex
    # (from_entitytype, from_sourceref, to_entitytype, to_sourceref)
    # and "distance", "from_zone", "to_zone",
    # "from_zonelist" and "to_zonelist" columns.
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
        return Reference(metadata=meta)

    def match_zone(self, point: geometry.Point, default: str) -> str:
        """Find the zone to which a point belongs"""
        assert(self.zones_df is not None)
        for _, row in self.zones_df.iterrows():
            if row.location and row.location.contains(point):
                return row.entityid
        return default

    def last_simulation(self, engine: Engine, sceneref: str) -> datetime:
        """Retrieve the date of the latest simulation for the given sceneref"""
        with engine.connect() as con:
            # Take the chance to load the zones_df, if not done already
            if self.zones_df is None:
                zones_df = pd.read_sql(text(f"""
                    SELECT
                        entityid, zoneid, name, label,
                        ST_AsGeoJSON(ST_ConvexHull(location)) AS location
                    FROM dtwin_zone_lastdata
                    """),
                    con=con
                )
                zones_df = geojson_to_shape(zones_df, 'location')
                self.zones_df = zones_df
            query = text(f"""
            SELECT timeinstant
            FROM dtwin_simulation_lastdata
            WHERE entityid = :sceneref
            ORDER BY timeinstant DESC
            LIMIT 1
            """)
            df = pd.read_sql(query.bindparams(sceneref=sceneref), con)
        #print(df)
        return df.iloc[0]['timeinstant']

    def calculate_distances(self, dims_df_map: typing.Mapping[str, pd.DataFrame]):
        """
        Calculate the distance between each pair of entities.

        The result is stored in the distance_df DataFrame,
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
                return 10
            return d

        distances: typing.List[pd.DataFrame] = []
        for from_type, _ in self.metadata.items():
            from_df = dims_df_map[from_type]
            from_entities = from_df[["sourceref", "location", "zone", "zonelist"]].rename(columns={
                "entityid": "from_entityid",
                "sourceref": "from_sourceref",
                "location": "from_location",
                "zone": "from_zone",
                "zonelist": "from_zonelist"
            })
            from_entities['from_entitytype'] = from_type
            for to_type, _ in self.metadata.items():
                to_df = dims_df_map[to_type]
                to_entities = to_df[["sourceref", "location", "zone", "zonelist"]].rename(columns={
                    "entityid": "to_entityid",
                    "sourceref": "to_sourceref",
                    "location": "to_location",
                    "zone": "to_zone",
                    "zonelist": "to_zonelist"
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

    def weights_by_distance(self, from_type: str, from_sourceref: str, to_type: str, to_sourceref: typing.Optional[typing.List[str]]=None) -> pd.Series:
        """
        Calculates the similarity between the (from_type, from_sourceref)
        entity, and every other entity of type `to_type` (except itself,
        if the from_type and to_type are the same).

        If the to_sourceref parameter is provided, it is used to filter
        the list of candidates.

        Then generates a series with scaled weights between each pair
        of entities. the returned series has a row for each `to_sourceref`
        of the given `to_type`, and is indexed by `to_sourceref`.

        The weights in this series add up to one, and can be used to
        calculate a weighted average of some metric from other entitites

        Currently the similarity criteria is just the distance
        between the entities. The distances are scaled so they
        are in a range between 1 and 10, and then a softmax
        is applied to turn them into a probability distribution.
        """
        assert(self.distance_df is not None)
        distance_series = self.distance_df['distance']
        candidates = typing.cast(pd.Series, distance_series.loc[from_type, from_sourceref, to_type])
        candidates = candidates.dropna()
        assert(isinstance(candidates, pd.Series))
        # remove the entity itself from the candidates
        candidates = candidates[typing.cast(pd.Series, candidates) > 0]
        if to_sourceref is not None:
            # We have some problems with buses not having all lines
            # in lastdata array.
            good_keys = candidates.index.intersection(to_sourceref)
            candidates = candidates.loc[good_keys]
        assert(candidates.index.names == ['to_sourceref'])
        # Distances have a wildly large range (from tens of meters to kilometers),
        # and applying a softmax directly yields terrible results.
        # We will convert them to logarithmic scale first.
        log_candidates = candidates.apply(lambda x: np.log(x))
        max_distance = typing.cast(float, log_candidates.max())
        assert(isinstance(max_distance, float))
        # We want to give more weight to the closest entities,
        # so we invert the distance
        inverted_distance = torch.Tensor(log_candidates.apply(lambda x: max_distance / x).to_numpy())
        softmax = inverted_distance.softmax(dim=0)
        return pd.Series(softmax.numpy(), index=log_candidates.index)

# -------------------------------------
# Schemaless types
# -------------------------------------

@dataclass
class Vector:
    """
    Untyped Vector class.

    Contains the complete series of metrics that make up
    the input of the encoder.

    The index of the series is expected to be a tuple
    (entitytype, metric, sourceRef, hour, minute).
    """
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
        for entitytype, meta in meta_map.items():
            entity_data = data_map.get(entitytype, None)
            entity_fixed = fixed_df_map[entitytype]
            entity_df: typing.Optional[pd.DataFrame] = None
            if entity_data is not None:
                entity_df = entity_data.df
            vector_list.append(meta.embed(fixed_df=entity_fixed, dataset=entity_df))
        vector = pd.concat(vector_list, axis=0)
        return Vector(df=vector.astype(np.float64))

@dataclass
class SimulationImpact:
    """
    This class contains the information needed to apply
    impacts to the simulation, after creating or removing
    entities.

    - source_entitytype: the entity type that has been added or removed.
    - source_removed:
        - if None, the impact is due to entities being added, not removed.
        - Otherwise, it must contains the data of the removed entities.
    - impacted_entitytype: the entitytype that is impacted by the change.
    - impacted_metric: the metric of the entitytype that is impacted by the change.
    - impact_func: the function that computes the impact.

    The impact_function must calculate the impact of a change into
    a series of target entities. It receives the Reference to the current
    meta and info, a target entitytype, and a DataFrame to update.
    
    The dataframe has the following index:
    - (sourceref, hour, minute), where sourceref belongs to the impacted_entitytype.

    And the following columns:
    - a `hidden` column with the values of the impacted_metric.
    - all the fixed properties of the impacted_entitytype
    - `from_entitytype` and `from_sourceref` identifying the entity
      that has been added or removed.
    - a `distance` column with the distance to from_sourceref.
    - all the metrics of `from_sourceref`.

    The function is expected to calculate an impact on the
    impacted_metric based on the initial status on the metric
    (`hidden` column) and the distance and metrics on the
    entity being added or removed, and then return a series
    with the same index as the dataframe, and the incremental
    impact on the impacted_metric.
    """
    source_entitytype: str
    source_removed: typing.Optional[typing.Sequence[str]]
    impacted_entitytype: str
    impacted_metric: str
    impact_func: typing.Callable[[Reference, pd.DataFrame], pd.Series]

@dataclass
class HiddenLayer:
    """Represents the hidden layer of the autoencoder"""

    # This is the hidden layer (status) of the autoencoder
    private: torch.Tensor
    # This index describes the order in which the information is
    # layed out in the hidden layer.
    # Currently, it has the following levels:
    # (entitytype, metric, sourceref, hour, minute)
    index: pd.MultiIndex

    def add_to_tensor(self, series: pd.Series, target_entitytype: str, target_metric: str, scale: int=0):
        """
        Receives a series with a multi-index with levels
        (sourceref, hour, minute), and
        adds the values of the series to the corresponding positions
        of the hidden tensor.

        if the metrics in the series are scaled,
        the function truncates the values after adding to the result
        tensor, to make sure the final result is within range.
        """
        assert(series.index.names == ['sourceref', 'hour', 'minute'])
        series = series[series != 0]
        if len(series) <= 0:
            logging.info("series not added to tensor because it is 0")
            return
        # Find of the offsets in the tensor where I have to add the values
        vector_offsets = pd.Series(range(0, len(self.index)), index=self.index, dtype=np.int32)
        vector_offsets.name = 'offset'
        vector_offsets = vector_offsets[target_entitytype, target_metric]
        assert(vector_offsets.index.names == ['sourceref', 'hour', 'minute'])
        # Align values and offsets
        series.name = 'metric'
        offsets_df = pd.merge(series, vector_offsets, how='inner', left_index=True, right_index=True, sort=False)
        offsets_key = offsets_df['offset'].to_list()
        offsets_val = offsets_df['metric'].to_numpy()
        activation: typing.Callable[[torch.Tensor], torch.Tensor] = DecoderLayer.linear
        if scale > 0:
            activation = DecoderLayer.scaled_sigmoid(scale, 0.9)
        # Cast tensor types
        addition = self.private[offsets_key] + torch.from_numpy(offsets_val).type(self.private.dtype)
        self.private[offsets_key] = activation(addition)

@dataclass
class Encoder:
    """
    Represents the encoder part of the autoencoder.
    """
    # This is the hidden layer
    hidden: HiddenLayer
    # This is an accumulator for additional metrics that
    # get added to the hidden layer as part of the simulation process.
    accumulator: typing.Dict[str, typing.Dict[str, pd.Series]]

    def impact(self, reference: Reference, perturbation: Dataset, from_impact: SimulationImpact) -> pd.Series:
        """
        Calculates the impact of the given perturbation into the target entity types.

        - The perturbation is a Dataset with information of the entities that
          have been added or dropped from the city.
        - The target entitytype and metric are the thing that we want to impact.
        - The from_impact is the SimulationImpact that we musr evaluate for this
          perturbation.

        The function will add up the impact of every sourceref in the
        perturbation dataset, and return a series indexed by
        (`sourceref`, `hour`, `minute`) with the incremental impact
        to consider for the simulation target entitytype and metric.
        """
        assert(reference.metadata is not None)
        assert(reference.dims_df_map is not None)
        # Get the part of the input tensor that belongs to the target entitytype and metric
        target_series = pd.Series(self.hidden.private.numpy(), index=self.hidden.index)
        target_series = typing.cast(pd.Series, target_series.loc[from_impact.impacted_entitytype, from_impact.impacted_metric])
        target_series = target_series.fillna(0.0)
        target_series.name = 'hidden'
        assert(target_series.index.names == ['sourceref', 'hour', 'minute'])
        target_meta = reference.metadata[from_impact.impacted_entitytype]
        target_df = target_meta.merge_fixed_props(target_series, reference.dims_df_map[from_impact.impacted_entitytype])
        # Restore the `entitytype` and `metric` levels that were dropped by the `loc` above
        target_df['entitytype'] = from_impact.impacted_entitytype
        target_df['metric'] = from_impact.impacted_metric
        # Make sure the perturbation dataframe has the same number of rows
        # per entity as the target dataframe (hours and minutes)
        perturb_meta = reference.metadata[perturbation.entityType].with_interval(hasHour=target_meta.hasHour, hasMinute=target_meta.hasMinute)
        perturb_dims = perturbation.df['sourceref'].drop_duplicates().to_frame()
        perturb_fixed_df = perturb_meta.get_fixed_df(perturb_dims)
        perturb_df = perturb_meta.normalize(fixed_df=perturb_fixed_df, dataset=perturbation.change_time(target_meta.hasHour, target_meta.hasMinute)).df
        perturb_df = perturb_df.rename(columns={'sourceref': 'from_sourceref'}).fillna(0)
        perturb_df['from_entitytype'] = perturbation.entityType
        # Now we iterate on the input dataset
        distinct_targets = target_df.index.get_level_values('sourceref').drop_duplicates().to_series()
        accumulator = pd.Series([0.0] * len(target_series), index=target_series.index)
        assert(reference.distance_df is not None)
        for key, group in perturb_df.groupby('from_sourceref'):
            # Extend the target_df with the distance to the perturbing entity
            perturb_sourceref = typing.cast(str, key)
            candidates = typing.cast(pd.DataFrame, reference.distance_df.loc[perturbation.entityType, perturb_sourceref, from_impact.impacted_entitytype]).reset_index() # type: ignore
            candidates = candidates.rename(columns={ 'to_sourceref': 'sourceref' }).set_index('sourceref')
            candidates = candidates[['distance', 'from_zone', 'from_zonelist', 'to_zone', 'to_zonelist']]
            assert(candidates.index.names == ['sourceref'])
            target_with_distance = pd.merge(
                target_df,
                candidates,
                how='left',
                left_index=True,
                right_index=True,
                sort=False
            )
            assert(target_df.index.equals(target_with_distance.index))
            # Now, join by hour and minute to the values of the
            # perturbing entity
            # First, make sure the normalization is fine, and we have
            # hour and minute rows matching in target_df and perturb_df.
            assert(len(group) * len(distinct_targets) == len(target_df))
            perturb_indexed = pd.merge(distinct_targets, group, how='cross', sort=False)
            perturb_indexed = perturb_indexed.set_index(['sourceref', 'hour', 'minute'])
            target_and_perturb = pd.merge(
                target_with_distance,
                perturb_indexed,
                how='left',
                left_index=True,
                right_index=True,
                sort=False
            )
            assert(target_df.index.equals(target_and_perturb.index))
            increment = from_impact.impact_func(reference, target_and_perturb)
            assert(increment.index.equals(target_and_perturb.index))
            accumulator = accumulator.add(increment)
        assert(accumulator.index.names == ['sourceref', 'hour', 'minute'])
        return accumulator

    @staticmethod
    def from_vector(metadata: Metadata, props: DatasetProperties, vector: Vector) -> 'Encoder':
        """
        Run the encoder over the given vector, and return the corresponding hidden states
        """
        return Encoder(
            hidden=HiddenLayer(
                private = torch.Tensor(vector.df.to_numpy()),
                index = typing.cast(pd.MultiIndex, vector.df.index)
            ),
            accumulator = defaultdict(dict)
        )

    def add_dataset(self, reference: Reference, dataset: Dataset, from_impact: SimulationImpact):
        """Add a set of new data from the simulation to the encoding"""
        # Accumulate all the impacts per entitytype and metric
        start = datetime.now()
        delta = self.impact(reference=reference, perturbation=dataset, from_impact=from_impact)
        entity_accum = self.accumulator[from_impact.impacted_entitytype]
        if from_impact.impacted_metric in entity_accum:
            delta = entity_accum[from_impact.impacted_metric].add(delta, fill_value=0)
        entity_accum[from_impact.impacted_metric] = delta
        stop = datetime.now()
        logging.debug("TIME FOR ADD_DATASET(from_impact: %s): %s", from_impact, stop-start)

    def drop_dataset(self, reference: Reference, dataset: Dataset, from_impact: SimulationImpact):
        """Drops data of removed entities from the encoding"""
        self.add_dataset(reference=reference, dataset=dataset, from_impact=from_impact)

    def get_hidden(self, reference: Reference) -> HiddenLayer:
        """Gets the current status of the hidden layer"""
        if len(self.accumulator) > 0:
            # And apply them all at once
            for entitytype, impacted_metrics in self.accumulator.items():
                for metric, delta in impacted_metrics.items():
                    logging.info("Adding to tensor %s lines of impact for entitytype %s and metric %s", delta.shape, entitytype, metric)
                    self.hidden.add_to_tensor(delta, entitytype, metric, reference.metadata[entitytype].metrics[metric].scale)
            self.accumulator = defaultdict(dict)
        return self.hidden

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
        Run the decoder over the given status tensor, and return the corresponding
        output tensor as a pd.Series. The series has a MultiIndex with levels
        (entityType, metric, sourceref, hour, minute)
        """
        result = torch.matmul(self.weights, hidden)
        result = result + self.biases
        result = self.activation(result)
        series = pd.Series(result.numpy(), index=self.index)
        return series

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
        # Then the conditions are satisfied by these numbers:
        C = inverse_sigmoid((1.0 - threshold) / (2.0 - threshold))
        A = (2.0 - threshold) * scale
        D = scale * 1.0 - A
        B = (-2.0 * C) / (threshold * scale)
        def scaled_func(x: torch.Tensor, A=A, B=B, C=C, D=D, st=threshold*scale):
            # Voy a separarlo en una curva lineal a la izquierda
            # del threshold, y la sigmoide a la derecha, para evitar
            # la distorisión que mete la sigmoide a los valores
            # distintos de la media
            negative_mask = (x <= 0)
            left_mask = (x <= st)
            left_values = x[left_mask]
            right_mask = (x > st)
            right_values = (A * torch.sigmoid(B * x[right_mask] + C) + D).type(x.dtype)
            result = torch.empty_like(x)
            result[negative_mask] = 0
            result[left_mask] = left_values
            result[right_mask] = right_values
            return result
        return scaled_func

    @staticmethod
    def scaled_gaussian(y0: float, x1: float, y1: float, x2: float, y2: float, yinf: float, bias: int) -> typing.Callable[[torch.Tensor], torch.Tensor]:
        """
        Generates a gaussian function with maximum at (x1, y1) and tending to yinf when x tends to infinity.

        The generated gaussian crosses the points:
        
        (0, y0)
        (x1, y1) (maximum)
        (x2, y2)
        (infinity, yinf)

        if x1 == 0, y0 is ignored

        """
        # Assertions to ensure the invariants hold
        assert x1 == 0 or y0 < y1, "y0 must be less than y1"
        assert x1 >= 0, "x1 must be greater than 0"
        assert x2 > x1, "x2 must be greater than x1"
        assert y1 > y2, "y2 must be less than y1"
        assert y2 > yinf, "y2 must be greater than yinf"

        # el bias puede ir de 1 (mínimo impacto) a 9 (máximo impacto)
        # lo usamos para escalar el alcance de la función y sus efectos.
        logging.info(f"BEFORE BIAS: bias={bias}, x1={x1}, y1={y1}, x2={x2}, y2={y2}, yinf={yinf}")
        bias_f = 1 + 0.05 * (bias - 5)
        y1 = yinf + (y1 - yinf) * bias_f
        y2 = yinf + (y2 - yinf) * bias_f # Reducir proporcionalmente y2, para garantizar que sigue siendo menor que el nuevo y1
        x2 = x2 * bias_f
        logging.info(f"AFTER BIAS: bias_f={bias_f}, x1={x1}, y1={y1}, x2={x2}, y2={y2}")

        logging.info(f"inverse_sigma_right: y1={y1}, y2={y2}, x2={x2}, x1={x1}")
        inverse_sigma_right = math.sqrt(math.log((y1 - yinf + 0.0)/(y2 - yinf))) / (x2 - x1 + 0.0)
        if x1 == 0:
            # This is not a piecewise gaussian, but a regular gaussian
            def gaussian(tensor: torch.Tensor, amplitude=y1-yinf, sigma=inverse_sigma_right) -> torch.Tensor:
                return amplitude * torch.exp(-((tensor * sigma) ** 2)) + yinf
            return gaussian

        # Calculate sigma for the left and right sides
        logging.info(f"inverse_sigma_left: y1={y1}, y0={y0}, x1={x1}")
        inverse_sigma_left = math.sqrt(math.log((y1 + 0.0)/y0)) / (x1 + 0.0)
        def piecewise_gaussian(tensor: torch.Tensor, amp_left=y1, amp_right=y1-yinf, bias=yinf, mean=x1, inverse_sigma_left=inverse_sigma_left, inverse_sigma_right=inverse_sigma_right) -> torch.Tensor:
            left_mask = tensor < mean
            left_values = (amp_left * torch.exp(-(((tensor[left_mask] - mean) * inverse_sigma_left) ** 2))).type(tensor.dtype)
            right_mask = tensor >= mean            
            right_values = (amp_right * torch.exp(-(((tensor[right_mask] - mean) * inverse_sigma_right) ** 2)) + bias).type(tensor.dtype)
            result = torch.empty_like(tensor)
            result[left_mask] = left_values
            result[right_mask] = right_values
            return result
        return piecewise_gaussian

    @staticmethod
    def apply_scale(series: pd.Series, scale: typing.Callable[[torch.Tensor], torch.Tensor], name: str="distance_scale") -> pd.Series:
        """
        Apply a scaling function to a pandas series
        
        When the input value is 0, the output value os also 0.
        This is to avoid issues with distances from an entity
        to itself.
        """
        tensor = torch.nan_to_num(torch.from_numpy(series.to_numpy()))
        tensor_mask = tensor > 0
        scaled_tensor = scale(tensor[tensor_mask]) + 1e-8
        result_tensor = torch.zeros_like(tensor)
        result_tensor[tensor_mask] = scaled_tensor
        scaled_series = pd.Series(result_tensor.numpy(), index=series.index)
        scaled_series.name = name
        return scaled_series

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

    def decode(self, props: DatasetProperties, hidden: HiddenLayer, additive: bool) -> typing.Optional[pd.Series]:
        """
        Run the decoder over the given hidden state tensor, and return the corresponding vector.
        The index of the returned series has thefollowing levels:

        ('entitytype', 'metric', 'sourceref', 'hour', 'minute')

        If `additive` is True, return results only for the additional layers.
        This is to generate a preview of the results of the additional entities.

        If `additive` is False, return results only for the base layer. This is to just
        compute changes on the base entities, after the simulation has run.
        """
        private = torch.nan_to_num(hidden.private)
        layers = self.add_layers if additive else [self.main_layer]
        if not layers:
            return None
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
        of the provided layer in the output.
        """
        # Compare sizes for matrix multiplication
        assert(layer.weights.shape[0] == len(layer.index))
        assert(layer.weights.shape[1] == self.main_layer.weights.shape[1])
        assert(layer.biases.shape[0] == len(layer.index))
        # We will add the data for the new entity
        # right to the end of the current index
        self.add_layers.append(layer)

    def weighted_layer(self, entitytype: str, metric: str, sourceref: str, weights: pd.Series) -> DecoderLayer:
        """
        Generates an Entity Decoder that will produce results for a new
        entity with id `sourceref` and type `entitytype`. The new results
        will include the metric `metric`.

        The results or this decoder will be a weighted average of
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
        added_vector = meta.embed(fixed_df=meta.get_fixed_df(dims_df), dataset=None, requested_metrics=[metric,])
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
    dryrun: bool=False

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
        if self.dryrun:
            return
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
        pass

    def add_impacts(self, reference: Reference, dryrun:bool=False) -> typing.Iterable[SimulationImpact]:
        """
        Generates Simulation impacts for any relation between entities that
        might impact the final results of the decoding process.

        Generates a sequence of SimulationImpact that tell the
        autoencoder how to incoporate the data of the removed entities
        to the encoding.
        """
        return tuple()

    def prepare_decoder(self, reference: Reference, decoder: Decoder):
        """
        Prepare the decoder for simulation

        Update the decoder layers to add or remove
        entities from the decoder output
        """
        pass

def create_simulators(reference: Reference, sim_props: SimulationProperties, broker: Broker, dryrun: bool=False) -> typing.Iterable[Simulation]:
    for sim in sim_props.settings:
        if sim['type'] == 'SimulationParking':
            logging.info("SimulationParking")
            yield SimParking(reference=reference, sim_props=sim_props, sim=sim)
        elif sim['type'] == 'SimulationTraffic':
            logging.info("SimulationParking")
            yield SimTraffic(reference=reference, sim_props=sim_props, sim=sim)
        elif sim['type'] == 'SimulationRoute':
            logging.info("SimulationParking")
            yield SimRoute(broker=broker, reference=reference, sim_props=sim_props, sim=sim, dryrun=dryrun)
        else:
            logging.warn("unrecognized simulation info: %s", sim)
        return None

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
    last_identity_date = reference.last_simulation(engine=engine, sceneref=identityref)
    logging.info("Latest identity data %s: %s", identityref, last_identity_date)

    # Get the simulation properties
    sim_props = SimulationProperties.create(broker=broker, identityref=identityref, identity_date=last_identity_date, fallback=fallback_sim)
    if not sim_props:
        logging.warning("No simulation found")
        return
    sim_props.dryrun = dryrun
    sim_props.feedback(broker, "initiating simulation")
    sim_handlers = list(create_simulators(reference=reference, sim_props=sim_props, broker=broker, dryrun=dryrun))

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

    # Handle adding entities or dropping entities from the scene
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
    logging.info("Adding simulation impacts for %s", sim_props.signature())
    add_impact: typing.Dict[str, typing.List[SimulationImpact]] = defaultdict(list)
    del_impact: typing.Dict[str, typing.List[SimulationImpact]] = defaultdict(list)
    for handler in sim_handlers:
        for impact in handler.add_impacts(reference=reference, dryrun=dryrun):
            if impact.source_removed is None:
                add_impact[impact.source_entitytype].append(impact)
            elif len(impact.source_removed) > 0:
                del_impact[impact.source_entitytype].append(impact)

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
        encoder = Encoder.from_vector(metadata=meta, props=dataset_props, vector=vector)
        logging.info("Hidden shape for scene %s, timeinstant %s, trend %s, daytype %s: %s",
            sim_props.sceneref,
            last_identity_date,
            trend,
            daytype,
            encoder.hidden.private.shape
        )
        sim_props.feedback(broker, "hidden shape %s", encoder.hidden.private.shape)

        # Perform a pre-run to generate values for the new entities
        additive_result = decoder.decode(props=dataset_props, hidden=encoder.get_hidden(reference=reference), additive=True)
        logging.info("Simulated partial result shape for scene %s, timeinstant %s, trend %s, daytype %s: %s",
            sim_props.sceneref,
            last_identity_date,
            trend,
            daytype,
            additive_result.shape if additive_result is not None else None
        )

        # Accumulate all the impacts per entitytype and metric
        for entitytype, impacts in del_impact.items():
            meta = reference.metadata[entitytype]
            original_ds = data_map[entitytype]
            original_df = original_ds.df
            for impact in impacts:
                assert(impact.source_removed is not None and len(impact.source_removed) > 0)
                dataset = Dataset(
                    timeinstant=original_ds.timeinstant,
                    trend=original_ds.trend,
                    daytype=original_ds.daytype,
                    entityType=entitytype,
                    df=original_df[original_df['sourceref'].isin(impact.source_removed)],
                )
                logging.info("Processing impact of removed entities of type %s (%s)", impact.source_entitytype, impact.source_removed)
                encoder.drop_dataset(reference=reference, dataset=dataset, from_impact=impact)

        for entitytype, impacts in add_impact.items():
            meta = reference.metadata[entitytype]
            assert(additive_result is not None)
            additive_dataset = meta.pivot(props=dataset_props, series=additive_result[entitytype])
            for impact in impacts:
                # Otherwise, get the data from the parial result
                logging.info("Processing impact of added entities of type %s", impact.source_entitytype)
                encoder.add_dataset(reference=reference, dataset=additive_dataset, from_impact=impact)

        # Decode the hidden status and vet the results
        result = decoder.decode(props=dataset_props, hidden=encoder.get_hidden(reference=reference), additive=False)
        assert(result is not None)
        sim_props.feedback(broker, "simulated result shape %s", result.shape)

        # Write output vector for debugging purposes
        # output_vector_path = f"output_vector_{trend}_{daytype}.csv"
        # logging.info("Saving output vector to %s", output_vector_path)
        # result.to_csv(output_vector_path)

        # Split into Datasets to save back to the database
        if additive_result is not None:
            result = pd.concat([result, additive_result], axis=0)
        for entityType, meta in reference.metadata.items():
            dataset = meta.pivot(props=dataset_props, series=result[entityType])
            dims_df = dims_df_map[entityType]
            meta.to_sql(engine=engine, sceneref=sim_props.sceneref, dataset=dataset, dims_df=dims_df, dryrun=dryrun)

    # Update the simulation table from the ETL
    logging.info("Storing simultation id in database")
    sim_props.to_sql(engine=engine, dryrun=dryrun)

    stop = datetime.now()
    logging.info("Total memory usage: %s", psutil.Process().memory_info().rss)
    sim_props.feedback(broker, f"done in {stop - start}")

def cleanup(reference: Reference, engine: Engine, broker: Broker, dryrun: bool=False):
    """
    Cleans up a simulation
    """
    sim_id = os.getenv("ETL_VECTORIZE_SIMULATION_ID")
    assert(sim_id is not None)
    assert(sim_id != "N/A")
    with engine.begin() as con:
        # Remove simulation form all entity types
        for meta in reference.metadata.values():
            logging.warning("Removing simulation %s data from %s", sim_id, meta.dataTableName)
            meta.clean_sql(con, sim_id, dims_also=True)
        logging.warning("Removing simulation %s from simlation_lastdata", sim_id)
        stmt = text("DELETE FROM dtwin_simulation_lastdata where entityid=:sceneref").bindparams(sceneref=sim_id)
        with con.execute(stmt) as cur:
            cur.close()
        if dryrun:
            con.rollback()

class SimParking:
    """Simulation for parking creation"""

    def __init__(self, reference: Reference, sim_props: SimulationProperties, sim: typing.Any):
        self.sim_date = sim_props.sim_date
        self.entitytype = "OffStreetParking"
        self.sceneref = sim_props.sceneref
        self.sourceref = f"sim_{self.sceneref}"
        self.name = sim.get('name', {}).get('value', '')
        self.location = sim.get('location', {}).get('value', {})
        self.capacity = int(sim.get('capacity', {}).get('value', '1000'))
        self.bias = int(sim.get('bias', {}).get('value', 5) or 5)
        self.zone = reference.match_zone(geometry.shape(self.location), "1")
        logging.info("SimParking entity loaded: %s", self.__dict__)

    def add_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        assert(reference.dims_df_map is not None)
        new_parking = {
            'sourceref': self.sourceref,
            'zone': self.zone,
            'zonelist': [self.zone],
            'location': geometry.shape(self.location),
            'capacity': self.capacity,
        }
        # Add simulated entity to the reference dims_df_map, so it is
        # available for other parts of the simulation.
        dims_df = reference.dims_df_map[self.entitytype]
        assert(frozenset(dims_df.columns).issuperset(new_parking.keys()))
        reference.dims_df_map[self.entitytype] = pd.concat([
            dims_df,
            pd.DataFrame([tuple(new_parking.values())], columns=tuple(new_parking.keys()))
        ], axis=0)
        # Save the new parking to the database
        with engine.begin() as conn:
            self.save_simulation_entity(conn=conn, broker=broker, reference=reference)
            if dryrun:
                conn.rollback()

    def add_impacts(self, reference: Reference, dryrun:bool=False) -> typing.Iterator[SimulationImpact]:
        # Add an impact on other parkings
        yield SimulationImpact(
            source_entitytype=self.entitytype,
            source_removed=None,
            impacted_entitytype='OffStreetParking',
            impacted_metric='occupationpercent',
            impact_func=self.impact_parkings
        )
    
    def impact_parkings(self, reference: Reference, df: pd.DataFrame) -> pd.Series:
        logging.debug("SimParking::impact_parkings. Received df columns:\n%s", df.columns)
        # Cuanta gente he "robado" del parking de al lado:
        # si estamos muy cerca, calculo que la mitad de mi ocupación
        # viene del otro parking; si nos vamos alejando, vamos "robando" menos gente.
        scale_func = DecoderLayer.scaled_gaussian(y0=0, x1=0, y1=0.75, x2=1000.0, y2=0.25, yinf=0.0, bias=self.bias)
        merged = pd.concat([df, DecoderLayer.apply_scale(series=df['distance'], scale=scale_func, name="distance_scale")], axis=1)
        scale = reference.metadata['OffStreetParking'].metrics['occupationpercent'].scale
        # El número máximo de personas dispuestas a trasladarse
        # de un parking a otro, dependerá de la distancia entre
        # parkings y la capacidad de los mismos.
        merged['old_occupation'] = merged['capacity'] * merged['hidden'] / scale
        merged['new_occupation'] = self.capacity * merged['occupationpercent'] / scale
        merged['people_to_move'] = merged['distance_scale'] * merged[['old_occupation', 'new_occupation']].min(axis=1)
        merged['occupation_difference'] = merged['hidden'] - merged['occupationpercent']
        # La cantidad de personas que realmente se trasladará,
        # dependerá de la diferencia de llenado entre ambos parkings.
        # Vamos a estimar que si la diferencia es de -100%, no se
        # va nadie, y si la dierencia es 100% se va todo el mundo.
        # Vamos a hacer una exponencial que se va a llevar más gente
        # cuanto mayor sea esa diferencia
        coefficient = math.log(2) / (2.0 * scale)
        merged['displaced_people'] = merged['people_to_move'] * (np.exp((merged['occupation_difference'] + scale) * coefficient) - 1)
        merged['displaced_percent'] = (merged['displaced_people'] / merged['capacity']) * scale
        # logging.debug("PARKING IMPACT CALCULATIONS:\n%s", merged[[
        #     "from_entitytype", "from_sourceref", "to_entitytype", "to_sourceref", "capacity", "hidden", "occupationpercent",
        #     "distance", "distance_scale", "people_to_move", "displaced_people", "displaced_percent"
        # ]].to_string())
        return (merged['displaced_percent'] * -1)

    def save_simulation_entity(self, conn: Connection, broker: Broker, reference: Reference):
        """generate simulated OffStreetParking entity"""
        metadata = reference.metadata[self.entitytype]
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
            zone=self.zone,
            location=json.dumps(self.location),
            name=self.name,
            capacity=self.capacity,
        )
        with conn.execute(bound) as cursor:
            cursor.close()

    def prepare_decoder(self, reference: Reference, decoder: Decoder):
        # Get weights to calculate the ocupation of the new
        # parking as a weighted average of the occupations of the
        # existing parkings, weighted by distance
        capacities = self.build_similarity_df(reference).reset_index()
        capacities['sourceref'] = capacities['to_sourceref']
        layers = {
            'OffStreetParking': {
                # use the capacity_scale to scale
                # the average for the occupationpercent metric
                'occupationpercent': 'capacity_scale'
            }
        }
        for entitytype, metrics in layers.items():
            for metric, scale in metrics.items():
                weights = capacities
                weights['metric'] = metric
                weights[metric] = weights.apply(lambda x: x[scale] * x['weight'], axis=1)
                weights = weights.set_index(['entitytype', 'metric', 'sourceref'])
                weights_series = weights[metric]
                layer = decoder.weighted_layer(entitytype, metric, self.sourceref, weights_series)
                decoder.add_layer(layer)

    def build_similarity_df(self, reference: Reference) -> pd.DataFrame:
        """
        Build a DataFrame that contains similarity weights
        from the new parking to be added, to any other parking.

        The dataframe has the columns:
        ['to_entitytype', 'to_sourceref', 'weight', 'capacity_scale'], where:

        - `weight` is the similarity between the new parking,
          and the `to_sourceref`.
        - `capacity_scale` is the ratio of the capacity
          of the `to_sourceref` and the new parking.
        """
        # Get the similarity_Df for other parkings
        distance_parkings = reference.weights_by_distance('OffStreetParking', self.sourceref, 'OffStreetParking')
        assert(distance_parkings.index.names == ['to_sourceref'])
        distance_parkings.name = 'weight'
        # Find the relative capacities between this parking and the others
        assert(reference.dims_df_map is not None)
        entitytype = 'OffStreetParking'
        meta = reference.metadata[entitytype]
        parking_capacities = meta.merge_fixed_props(data_df=distance_parkings, dims_df=reference.dims_df_map[entitytype])
        assert(parking_capacities.index.names == ['to_sourceref'])
        assert(parking_capacities.columns.to_list() == ['weight', 'capacity'])
        parking_capacities = parking_capacities.reset_index()
        parking_capacities['entitytype'] = entitytype
        # Add a prevision of how many new people will try to
        # use the new parking, based on the zone intensity.
        intensities = self.find_close_intensity(reference)
        max_intensity = intensities['intensity'].max()
        # This is the capacity I have over the typical parking
        extra_capacity = max(self.capacity - parking_capacities['capacity'].mean(), 0)
        # This is how much from the zone traffic intensity I expect
        # to be able to use the parking
        biased_intensity = min(extra_capacity, max_intensity) * (1 + self.bias) / 10
        # Now let's scale the capacity of each parking so when
        # they are at 100%, they would add biased_intensity to
        # my parking.
        parking_capacities['capacity_scale'] = parking_capacities.apply(lambda x: (x['capacity'] + biased_intensity) / self.capacity, axis=1)
        return parking_capacities

    def find_close_intensity(self, reference: Reference) -> pd.DataFrame:
        """
        Find the TrafficIntensity entities in the same zone,
        and return a pd.DataFrame with the intensity measurements.
        """
        assert(reference.dims_df_map is not None)
        zones_df = reference.dims_df_map['TrafficIntensity']
        zones_df = zones_df[zones_df['zone'] == self.zone]
        closest_intensity = zones_df['sourceref']
        assert(reference.data_df_map is not None)
        intensities_df = reference.data_df_map['TrafficIntensity']
        intensities_df.to_csv("intensities_df.csv")
        intensities_df = intensities_df[intensities_df['sourceref'].isin(closest_intensity)]
        intensities_df.to_csv("intensities_df_after.csv")
        return intensities_df

class SimTraffic:
    """Simulation for traffic affectation"""

    def __init__(self, reference: Reference, sim_props: SimulationProperties, sim: typing.Any):
        self.sim_date = sim_props.sim_date
        self.sceneref = sim_props.sceneref
        self.name = sim.get('name', {}).get('value', '')
        self.capacity = int(sim.get('capacity', {}).get('value', '1000'))
        self.bias = int(sim.get('bias', {}).get('value', 5) or 5)
        self.category = sim.get('category', {}).get('value', 'pedestrian').lower().strip()
        self.bbox = shapely.MultiPoint(sim.get('location').get('value', [[0,0],[0,0]]))
        # Save location to sim_props, so that it can be used
        # in the database.
        sim_props.location = json.loads(shapely.to_geojson(self.bbox))
    
    def add_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        pass

    def add_impacts(self, reference: Reference, dryrun:bool=False) -> typing.Iterable[SimulationImpact]:
        identityref = 'N/A'
        self.affected_places = reference.metadata['TrafficCongestion'].in_bbox(engine=engine, sceneref=identityref, bbox=self.bbox)
        logging.info("Affected TrafficCongestion entities: %s", ", ".join(self.affected_places))
        #Locate all TrafficIntensity entities close enough to any of the affected entities
        self.related_places = reference.get_closest(
            from_type='TrafficCongestion',
            from_sourceref=self.affected_places,
            to_type='TrafficIntensity',
            distance=25 # meters
        )
        logging.info("Affected TrafficIntensity entities: %s", ", ".join(self.affected_places))
        if len(self.affected_places) > 0:
            yield SimulationImpact(
                source_entitytype='TrafficCongestion',
                source_removed=self.affected_places,
                impacted_entitytype='TrafficCongestion',
                impacted_metric='congestion',
                impact_func=self.impact_congestion
            )
            yield SimulationImpact(
                source_entitytype='TrafficCongestion',
                source_removed=self.affected_places,
                impacted_entitytype='OffStreetParking',
                impacted_metric='occupationpercent',
                impact_func=self.impact_parking
            )

    def prepare_decoder(self, reference: Reference, decoder: Decoder):
        if self.affected_places:
            for place in self.affected_places:
                decoder.drop_sourceref('TrafficCongestion', place)
        if self.related_places:
            for place in self.related_places:
                decoder.drop_sourceref('TrafficIntensity', place)

    def impact_congestion(self, reference: Reference, df: pd.DataFrame) -> pd.Series:
        logging.info("SimTraffic impact_congestion:\n%s", df.columns)
        scale_func = DecoderLayer.scaled_gaussian(y0=0.25, x1=1000, y1=1, x2=3000, y2=0.5, yinf=0.0, bias=self.bias)
        merged = pd.concat([df, DecoderLayer.apply_scale(series=df['distance'], scale=scale_func, name="distance_scale")], axis=1)
        # Traslado la congestión a las vías cercanas
        merged['displaced'] = merged['congestion'] * merged['distance_scale'] / len(self.affected_places)
        return merged['displaced']

    def impact_parking(self, reference: Reference, df: pd.DataFrame) -> pd.Series:
        logging.info("SimTraffic impact_parking:\n%s\n%s", df.index.names, df.columns)
        # The closer the parking to the affected streets, the more people will use it
        if self.category == 'pedestrian':
            scale_func = DecoderLayer.scaled_gaussian(y0=0, x1=0, y1=1, x2=1000, y2=0.5, yinf=0, bias=self.bias)
        else:
            scale_func = DecoderLayer.scaled_gaussian(y0=0, x1=0, y1=0.25, x2=1000, y2=0.15, yinf=0, bias=self.bias)
        merged = pd.concat([df, DecoderLayer.apply_scale(series=df['distance'], scale=scale_func, name="distance_scale")], axis=1)
        scale = reference.metadata['OffStreetParking'].metrics['occupationpercent'].scale
        # Modulo el incremento por hora del día. Vamos a aumentarlo más cuando más demanda hay
        range_per_entity = merged.reset_index()[['sourceref', 'hidden']].groupby('sourceref', as_index=True).agg(
            min_occupationpercent=('hidden', 'min'),
            max_occupationpercent=('hidden', 'max')
        )
        logging.info("SimTraffic range_per_entity:\n%s\n%s", range_per_entity.index.names, range_per_entity.columns)
        range_per_entity['slope_occupationpercent'] = range_per_entity['max_occupationpercent'] - range_per_entity['min_occupationpercent'] + 1e-8
        merged = pd.merge(merged, range_per_entity, left_index=True, right_index=True)
        merged['hour_scale'] = (merged['hidden'] - merged['min_occupationpercent'] + 1e-8) / merged['slope_occupationpercent']
        # Get a measure of the spare capacity, affected by the bias
        # In this impact, the hidden column is occupationpercent.
        merged['spare_capacity'] = (merged['capacity'] * (1 - merged['hidden'] / scale)) * (0.25 + 0.5 * self.bias / 10)
        merged['increased_occupation'] = merged['spare_capacity'] * merged['distance_scale'] * merged['hour_scale']
        merged['increase'] = (merged['increased_occupation'] * scale) / merged['capacity']
        # Since this will be computed once per street closure, divide
        # by number of closed streets
        merged['displaced'] = merged['increase'] / len(self.affected_places)
        return merged['displaced']

class SimRoute:
    """Simulation for route affectation"""

    def __init__(self, broker: Broker, reference: Reference, sim_props: SimulationProperties, sim: typing.Any, dryrun: bool=False):
        self.sceneref = sim_props.sceneref
        self.sim_date = sim_props.sim_date
        self.trips = float(sim.get('trips', {}).get('value', 100))
        self.intensity = float(sim.get('intensity', {}).get('value', 1000))
        self.bias = int(sim.get('bias', {}).get('value', 5) or 5)
        self.sim_id = sim['id']
        self.sim_type = sim['type']
        self.sourceref = f"sim_{self.sceneref}"
        self.fetch_stops(broker=broker, reference=reference, dryrun=dryrun)
        # Add location to the simulation properties, so it can be
        # updated to the database.
        sim_props.location = self.location
        logging.info("SimRoute entity loaded: %s", self.__dict__)

    def fetch_stops(self, broker: Broker, reference: Reference, dryrun:bool=False):
        """Fetch all stops for this simulation"""
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
        if len(sorted_stops) <= 1:
            raise ValueError("SimRoute scene %s: routes must have more than one stop", self.sceneref)
        for stop in sorted_stops:
            stop['id'] = f"{self.sourceref}_{stop['id']}"
            stop['refSimulation'] = {
                'type': 'Text',
                'value': self.sim_id
            }
            coord = stop['location']['value']
            coords.append(coord)
            zones.append(reference.match_zone(point=geometry.shape(coord), default="1"))
        self.location = {
            'type': 'MultiLineString',
            'coordinates': [[c['coordinates'] for c in coords]]
        }
        # Update the simulation entity with the line
        # Count zones and get most repeated
        zone_count = sorted(((count, zone) for zone, count in Counter(zones).items()), reverse=True)
        self.zone = zone_count[0][1]
        self.zonelist = list(frozenset(zones))
        # Add new Routes to the dims_df_map
        self.forwardstops = len(coords)
        self.returnstops = len(coords)
        if not dryrun:
            logging.info("SimRoute: Updating geometry in entity %s of type %s", self.sim_id, self.sim_type)
            broker.push(entities=[{
                'id': self.sim_id,
                'type': self.sim_type,
                'location': {
                    'type': 'geo:json',
                    'value': self.location
                }
            }])
            # Remove stops
            #logging.info("SimRoute: pushing %d stops", len(stops))
            broker.push(stops)
            #logging.info("SimRoute: removing stops with refSimulation: none")
            broker.delete("Stop", q="refSimulation:none")

    def add_entities(self, engine: Engine, broker: Broker, reference: Reference, dryrun:bool=False):
        assert(reference.dims_df_map is not None)
        # Rename stops and associate to the proper sourceref
        logging.debug("self.location: %s", self.location)
        new_route = {
            'sourceref': self.sourceref,
            'zone': self.zone,
            'zonelist': self.zonelist,
            'location': geometry.shape(self.location),
            'forwardstops': self.forwardstops,
            'returnstops': self.returnstops,
        }
        logging.info("SimRoute: new route = %s", new_route)
        with engine.begin() as conn:
            for entitytype in ('RouteSchedule', 'RouteIntensity'):
                # Save the entity to the reference dims_df_map,
                # so it is available for other parts of the simulation
                dims_df = reference.dims_df_map[entitytype]
                assert(frozenset(dims_df.columns).issuperset(new_route.keys()))
                reference.dims_df_map[entitytype] = pd.concat([
                    dims_df,
                    pd.DataFrame([tuple(new_route.values())], columns=tuple(new_route.keys()))
                ], axis=0)
                self.save_simulation_entity(conn, reference, entitytype)
            if dryrun:
                conn.rollback()

    def add_impacts(self, reference: Reference, dryrun:bool=False) -> typing.Iterable[SimulationImpact]:
        # Add an impact on other routes
        yield SimulationImpact(
            source_entitytype='RouteIntensity',
            source_removed=None,
            impacted_entitytype='RouteIntensity',
            impacted_metric='intensity',
            impact_func=self.impact_route_intensity
        )
        # Add an impact on parkings
        yield SimulationImpact(
            source_entitytype='RouteIntensity',
            source_removed=None,
            impacted_entitytype='OffStreetParking',
            impacted_metric='occupationpercent',
            impact_func=self.impact_parking
        )

    def prepare_decoder(self, reference: Reference, decoder: Decoder):
        capacities = self.build_similarity_df(reference).reset_index()
        capacities['sourceref'] = capacities['to_sourceref']
        # We need to add a layer per entity type and metric
        layers = {
            'RouteSchedule': {
                'forwardtrips': 'trips_scale',
                'returntrips': 'trips_scale'
            },
            'RouteIntensity': {
                'forwardtrips': 'trips_scale',
                'returntrips': 'trips_scale',
                'intensity': 'intensity_scale'
            }
        }
        for entitytype, metrics in layers.items():
            for metric, scale in metrics.items():
                weights = capacities
                weights['entitytype'] = entitytype
                weights['metric'] = metric
                weights[metric] = weights.apply(lambda x: x[scale] * x['weight'], axis=1)
                weights = weights.set_index(['entitytype', 'metric', 'sourceref'])
                weights_series = weights[metric]
                decoder.add_layer(decoder.weighted_layer(entitytype, metric, self.sourceref, weights_series))

    def impact_route_intensity(self, reference: Reference, df: pd.DataFrame) -> pd.Series:
        logging.info("SimRoute impact_route_intensity:\n%s\n%s", df.index.names, df.columns)
        return pd.Series([0] * len(df), index=df.index)

    def impact_parking(self, reference: Reference, df: pd.DataFrame) -> pd.Series:
        logging.info("SimRoute impact_parking:\n%s\n%s", df.index.names, df.columns)
        # Localizo la cantidad de viajeros que tienen las líneas cercanas a cada parking
        assert(reference.distance_df is not None)
        scale_func = DecoderLayer.scaled_gaussian(y0=0, x1=0, y1=1, x2=1000, y2=0.5, yinf=0, bias=self.bias)
        # from_sourceref = parking
        # to_sourceref = RouteIntensity
        distance_df = reference.distance_df.reset_index()
        distance_df = distance_df[(distance_df['from_entitytype'] == 'OffStreetParking') & (distance_df['to_entitytype'] == 'RouteIntensity')]
        # No consideramos la nueva línea en estos cálculos
        distance_df = distance_df[distance_df['to_sourceref'] != self.sourceref]
        # Añadimos la columna "distance_scale"
        distance_df = pd.concat([distance_df, DecoderLayer.apply_scale(series=distance_df['distance'], scale=scale_func, name="distance_scale")], axis=1)
        # Añadimos la columna "intensity"
        assert(reference.data_df_map is not None)
        distance_df = pd.merge(
            distance_df,
            reference.data_df_map['RouteIntensity'][['sourceref', 'intensity']].groupby('sourceref').mean(),
            how='left',
            left_on='to_sourceref',
            right_on='sourceref'
        )
        # Y añadimos los forwardstops y returnstops
        assert(reference.dims_df_map is not None)
        distance_df = pd.merge(
            distance_df,
            reference.dims_df_map['RouteIntensity'][['sourceref', 'forwardstops', 'returnstops']].fillna(1),
            how='left',
            left_on='to_sourceref',
            right_on='sourceref'
        )
        # Y calculamos la cantidad de gente que pasa cerca del parking,
        # en función de la intensidad de las líneas y su distancia
        distance_df['sum_intensity'] = distance_df['intensity'] * distance_df['distance_scale'] / (distance_df['forwardstops'] + distance_df['returnstops'])
        logging.debug("impact_parking: distance_df=\n%s", distance_df.to_string())
        intensity_df = distance_df[['from_sourceref', 'sum_intensity']].rename(columns={
            "from_sourceref": "sourceref"
        }).groupby('sourceref', as_index=True).sum()
        logging.debug("impact_parking: intensity_df=\n%s", intensity_df.to_string())
        # Ahora, veo para este parking, qué distancia e intensidad hay
        merged = pd.concat([df, DecoderLayer.apply_scale(series=df['distance'], scale=scale_func, name="distance_scale")], axis=1)
        merged['new_intensity'] = merged['intensity'] * merged['distance_scale'] / (self.forwardstops + self.returnstops)
        # Uno estos datos con los de intensidad cercana
        merged = pd.merge(merged, intensity_df, how='left', left_index=True, right_index=True)
        merged = merged.fillna(0)
        merged['sum_intensity'] = merged[['sum_intensity', 'new_intensity']].max(axis=1)
        merged['ratio_intensity'] = merged['new_intensity'] / merged['sum_intensity']
        # La gente que deja de usar el parking será una proporción entre la intensidad
        # de la nueva línea, y las intensidades de las líneas que ya existen y pasan cerca.
        # - Si la relación intensidad-distancia es similar a la suma de las líneas que ya hay,
        #   la ocupación bajará poco.
        # - Si la relación intensidad-distancia es muy superior a la suma de las líneas que
        #   ya hay, la ocupación bajará bastante más.
        scale = reference.metadata['OffStreetParking'].metrics['occupationpercent'].scale
        merged['occupation'] = merged['capacity'] * merged['hidden'] / scale
        merged['budget_occupation'] = merged['occupation'] * (0.1 + (self.bias / 9) * 0.25)
        merged['new_occupation'] = merged['occupation'] - merged['ratio_intensity'] * merged['budget_occupation']
        merged['decrement'] = ((merged['new_occupation'] - merged['occupation']) * scale) / merged['capacity']
        logging.debug("SimRoute merged_df:\n%s", merged.to_string())
        return merged['decrement']

    def save_simulation_entity(self, conn: Connection, reference: Reference, entitytype: str):
        """generate simulated RouteSchedule or RouteIntensity entity"""
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
            zone=self.zone,
            zonelist=json.dumps(self.zonelist),
            location=json.dumps(self.location),
            name=self.sourceref,
            forwardstops=self.forwardstops,
            returnstops=self.returnstops,
        )
        with conn.execute(bound) as cursor:
            cursor.close()

    def build_similarity_df(self, reference: Reference):
        """
        Build a DataFrame that contains similarity weights
        from the new Route to be added, to any other route

        The dataframe has the columns:
        ['to_sourceref', 'weight', 'intensity_scale', 'trips_scale'], where:

        - `weight` is the similarity between the new route,
          and the `to_sourceref`.
        - `intensity_scale` is the ratio of the intensity
          of the `to_sourceref` RouteIntensity, and the new route.
        - `trips_scale` is the ratio of the number of trips
          of the `to_sourceref` RouteIntensity, and the new route.
        """
        assert(reference.data_df_map is not None)
        entities = reference.data_df_map['RouteIntensity'][['sourceref', 'intensity', 'forwardtrips', 'returntrips']].groupby('sourceref').mean()
        # Some lines have NaN metrics, they must be removed.
        # Otherwise, the NaNs will crop into the output.
        entities = entities.dropna()
        assert(entities.index.names == ['sourceref'])
        distance_averages = reference.weights_by_distance('RouteIntensity', self.sourceref, 'RouteIntensity', entities.index.to_list())
        assert(distance_averages.index.names == ['to_sourceref'])
        distance_averages.name = 'weight'
        # Prepare dataframe with the scale of each route, both
        # intensity and number of trips
        capacities = pd.merge(distance_averages.to_frame(), entities, how='left', left_index=True, right_index=True, sort=False)
        assert(capacities.index.names == ['to_sourceref'])
        assert(capacities.columns.to_list() == ['weight', 'intensity', 'forwardtrips', 'returntrips'])
        capacities = capacities.reset_index()
        capacities['intensity_scale'] = capacities.apply(lambda x: self.intensity / x['intensity'], axis=1)
        capacities['trips_scale'] = capacities.apply(lambda x: self.trips / (x['forwardtrips'] + x['returntrips']), axis=1)
        return capacities

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

    for config in args.config or tuple():
        logging.debug("loading config file %s", config)
        loadConfig(pathlib.Path(config[0]))
    logging.info("Configuration:\n%s", json.dumps(dumpConfig(), indent=2))

    try:
        with ExitStack() as stack:
            engine = stack.enter_context(psql_engine())
            broker = stack.enter_context(orion_engine())
            reference = Reference.create(meta_path=pathlib.Path(args.meta), engine=engine)
            logging.info("Metadata order:\n%s", ", ".join(reference.metadata.keys()))
            changeType = os.getenv("ETL_VECTORIZE_ALTERATIONTYPE", "")
            logging.warning("ETL_VECTORIZE_ALTERATIONTYPE=%s", changeType)
            if changeType == "entityDelete":
                logging.warning("Cleaning up database after simulation removal")
                cleanup(reference, engine, broker, args.dryrun)
            else:
                logging.warning("Starting simulation")
                main(reference, engine, broker, args.fallback, args.dryrun)
        logging.info("ETL OK")
    except Exception as err:
        logging.exception(msg="Error during vectorization", stack_info=True)
        sys.exit(-1)
