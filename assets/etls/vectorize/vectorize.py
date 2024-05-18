#!/usr/bin/env python

import os
import pathlib
import argparse
import json
import typing
import logging
from datetime import datetime
from dataclasses import dataclass
from contextlib import contextmanager
from collections import defaultdict
from sqlalchemy import create_engine, event, text, URL, Engine, TextClause
import pandas as pd
import numpy as np


# -------------------------------------
# Config management section
# -------------------------------------

def loadConfig(jsonPath: pathlib.Path):
    """Loads script configuration into environment from json file"""
    with open(jsonPath) as f:
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
def psql_engine() -> typing.Iterable[Engine]:
    """Yields a postgres connection to the database"""
    url_object = URL.create(
        "postgresql+psycopg",
        username=os.getenv("ETL_VECTORIZE_PG_USER"),
        password=os.getenv("ETL_VECTORIZE_PG_PASSWORD"),
        host=os.getenv("ETL_VECTORIZE_PG_HOST"),
        port=os.getenv("ETL_VECTORIZE_PG_PORT"),
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

# -------------------------------------
# Data bearing types
# -------------------------------------

@dataclass
class SceneData:
    """
    Contains data for a particular scene, trend and daytype.

    This data is not scaled, i.e. it holds the original info
    from the database for the scene.
    """
    sceneref: str
    timeinstant: str
    trend: str
    daytype: str
    df: pd.DataFrame

@dataclass
class VectorData:
    """
    Holds the data of a regularized dataframe. This data is:

    - fixed length. There is a row per entity id, hour (if hasHour)
      and 10-minute interval (if hasMinute).
      - The entities included in the vector must always be the same
        for a given entityType: the entities the model has been
        trained on. This is given by the dimension table for the
        entityType. Entities are always sorted by id in the vector.
      - if hasHour, there is a row per hour from 00 to 23.
      - if hasMinute, there is a row per 10-minute interval from 00 to 50.

    - scaled so that all vales are between 0 and 1
      - metrics that contain probabilites are left as is.
      - metrics that do not contain probabilities are scaled
        to be between 0 and 1.
        If metrics could be negative, an offset would be applied
        before scaling. IT is currently not the case for any
        metric.

    The columns in the dataframe are at least "sourceref",
    "hour", "minute", and a column per "metric". Note that
    "hour" and/or "minute" might be 0 if not hasHour or not
    hasMinute, respectively.

    Notice that the metrics in a row can be NaN if the source
    does not have data for the given combination of sourceref,
    hour and minute.

    In order to de-scale a metric, first you should multiply
    by the scale factor and then add the offset value.
    """
    entityType: str
    hasHour: bool
    hasMinute: bool
    metrics: typing.Tuple[str]
    offset: typing.Mapping[str, float]
    scale: typing.Mapping[str, float]
    df: pd.DataFrame

# -------------------------------------
# Schema bearing types
# -------------------------------------

@dataclass
class Metric:
    """
    Describes properties of a metric
    """
    probability: bool

@dataclass
class Metadata:
    """
    Describes each of the datasets in the database
    """
    dimensions: typing.List[str]
    metrics: typing.Mapping[str, Metric]
    hasHour: bool
    hasMinute: bool
    multiZone: bool
    namespace: str
    entityType: str
    dataTableName: str
    dimsTableName: str

    @staticmethod
    def fromdict(kw: typing.Dict[str, typing.Any]) -> 'Metadata':
        """Read Metadata from a json object"""
        # Convert metrics to dict of `Metric` objects
        metrics = {k: Metric(v) for k, v in kw.pop("metrics", {}).items()}
        # Sort metrics in a stable order, and lowercase them
        # to match database column names
        kw['metrics'] = { k.lower(): metrics[k] for k in sorted(metrics.keys()) }
        return Metadata(**kw)

    def dim_query(self) -> TextClause:
        """Build SQL query to determine all entity IDs in the model"""
        if self.multiZone:
            columns = "sourceref, zone, zonelist, ST_AsGeoJSON(location) AS location"
        else:
            columns = "sourceref, zone, Array[zone]::json[] as zonelist, ST_AsGeoJSON(location) AS location"
        return text(f"SELECT {columns} FROM {self.dimsTableName} ORDER BY sourceref ASC")

    def dim_df(self, engine: Engine) -> pd.DataFrame:
        """Builds a dataframe of all entity IDs in the model"""
        query = self.dim_query()
        logging.debug("Querying statics for %s: %s", self.entityType, query)
        df = pd.read_sql(query, engine)
        df['entitytype'] = self.entityType
        # Make sure to sort by entity id. The order of columns
        # in the vector is important.
        df.sort_values(by=['sourceref'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def scene_query(self) -> TextClause:
        """Build SQL query for a given sceneref and timeinstant"""
        columns = ", ".join(c.lower() for c in (self.dimensions + list(self.metrics.keys())))
        return text(f"""
        SELECT {columns}
        FROM {self.dataTableName}
        WHERE sceneref = :sceneref
        AND timeinstant = :timeinstant
        """)

    def scene_set(self, engine: Engine, sceneref: str, timeinstant: datetime) -> typing.Iterable[SceneData]:
        """Retrieves a given sceneRef and TimeInstant, generates SceneData"""
        query = self.scene_query()
        logging.info("Querying scene %s (at %s) for entity type  %s: %s", sceneref, timeinstant, self.entityType, query)
        df = pd.read_sql(query.bindparams(sceneref=sceneref, timeinstant=timeinstant), engine)
        # Separate by trend and dayType
        for group, data in df.groupby(['trend', 'daytype']):
            yield SceneData(
                sceneref=sceneref,
                timeinstant=timeinstant,
                trend=group[0],
                daytype=group[1],
                df=data
            )

    def vectorize(self, metrics_df: pd.DataFrame, dim_df: pd.DataFrame) -> VectorData:
        """
        Turns a regularized metrics dataframe into a vector, i.e.:
        - Sorts entries so that they match the entity order in dim_df.
        - Fills in missing rows for hours or days.
        - Scales metrics so that the vector information is within range [0, 1]

        The metrics_df must be regularized in time, i.e. there must be only
        one entry per "sourceref" and set of dimensions:
        - if "hasHour" is true, there must be only one entry per sourceref
          and hour
        - if "hasMinute" is true, there must be only one entry per sourceref,
          hour and ten-minute interval.

        Each dataset is regularized differently. See the documentation of
        datasets for more infor on regularization.
        """
        vector = VectorData(
            entityType=self.entityType,
            hasHour=self.hasHour,
            hasMinute=self.hasMinute,
            metrics=tuple(self.metrics.keys()),
            offset={
                k: 0 for k in self.metrics.keys()
            },
            scale={
                k: 1 for k in self.metrics.keys()
            },
            df=None
        )
        for metric, props in self.metrics.items():
            if not props.probability:
                # All our measures are either probabilities or intensities,
                # larger than 0 in any case.
                # We will normalize intensities to [0, 1] so that
                # they are within the range of the vector.
                max_val = metrics_df[metric].max()
                if max_val > 0:
                    # Keep track of the scale factor to be able to de-scale later.
                    vector.scale[metric] = max_val
                    metrics_df[metric] = metrics_df[metric] / max_val
        # Now, make sure there is a metric for each
        # possible combiunation of dimensions, so the vector has
        # always a fixed size. Even if some of the
        # metrics are NaN (they will be considered "padding")
        merger_df = dim_df[['sourceref']]
        on_columns = ['sourceref']
        if self.hasHour:
            hours = tuple(range(24))
            hours_df = pd.DataFrame({'hour': hours}, index=hours)
            merger_df = pd.merge(merger_df, hours_df, how='cross')
            on_columns.append('hour')
        else:
            merger_df['hour'] = 0
        if self.hasMinute:
            minutes = tuple(m*10 for m in range(6))
            minutes_df = pd.DataFrame({'minute': minutes}, index=minutes)
            merger_df = pd.merge(merger_df, minutes_df, how='cross')
            on_columns.append('minute')
        else:
            merger_df['minute'] = 0
        # If might be the case that we need the vector, but we don't have any
        # data at all for the given entityType. Then just return a vector
        # with all dimensions being NaN
        if metrics_df is None:
            vector.df = merger_df
            for col in self.metrics.keys():
                vector.df[col] = np.nan
        else:
            vector.df = pd.merge(merger_df, metrics_df, how='left', on=on_columns)
        vector.df.reset_index(drop=True)
        return vector

# -------------------------------------
# Model type
# -------------------------------------

@dataclass
class SceneModel:
    trend: str
    daytype: str
    # Ordered mapping from entity type to entity ids.
    # The entities in the vector must always be the same
    # and sorted in the same order.
    dims: typing.Mapping[str, pd.DataFrame]
    # Ordered mapping from entity type to data vectors.
    # The entries in each vector must always be the same
    # and sorted in the same order.
    vecs: typing.Optional[typing.Mapping[str, pd.DataFrame]]

def read_meta(path: pathlib.Path) -> typing.Dict[str, Metadata]:
    """Reads metadata from json file"""
    with open(path) as f:
        items = (Metadata.fromdict(params) for params in json.load(f))
        meta = {item.entityType: item for item in items}
    return {k: meta[k] for k in sorted(meta.keys())}

def last_simulation(engine: Engine, sceneref: str) -> datetime:
    """Retrieeve the date of the latest simulation for the given sceneref"""
    query = text(f"""
    SELECT timeinstant
    FROM dtwin_simulation_lastdata
    WHERE entityid = :sceneref
    ORDER BY timeinstant DESC
    LIMIT 1
    """)
    logging.debug("Querying last simulation for %s: %s", sceneref, query)
    df = pd.read_sql(query.bindparams(sceneref=sceneref), engine)
    print(df)
    return df.iloc[0]['timeinstant']

def vectorize(meta: typing.Mapping[str, Metadata], engine: Engine):
    """
    Vectorizes the data in the database
    """
    # Get the latest identity we are working with
    identityref = os.getenv("ETL_VECTORIZE_IDENTITYREF", "N/A")
    last_sim_date = last_simulation(engine=engine, sceneref=identityref)
    logging.info("Last simulation date for sceneRef '%s': %s", identityref, last_sim_date)

    # Group all data by combinations of trend and daytype, and then by entityType
    scene_sets: typing.Mapping[typing.Tuple[str, str], typing.Mapping[str, SceneData]] = defaultdict(dict)
    for entityType, m in meta.items():
        dim_df = m.dim_df(engine)
        for scene_data in m.scene_set(engine=engine, sceneref=identityref, timeinstant=last_sim_date):
            scene_sets[(scene_data.trend, scene_data.daytype)][entityType] = scene_data

    # Iterate over all combinations of trend and daytype
    for k, entities in scene_sets.items():
        trend, daytype = k
        logging.info("Vectorizing trend %s, daytype %s", trend, daytype)
        vector_list = []
        for entityType, m in meta.items():
            scene_set = entities.get(entityType, None)
            # If we got no data for this entity type, we will just
            # generate a vector with all NaN metrics.
            if scene_set is None:
                logging.info("No data for entity type %s, generating NaN frame", entityType)
                scene_set = SceneData(
                    sceneref=identityref,
                    timeinstant=last_sim_date,
                    trend=trend,
                    daytype=daytype,
                    df=None
                )
            vector = m.vectorize(metrics_df=scene_set.df, dim_df=dim_df)
            logging.info("Vector for entityType %s has size %s, scale %s, offset %s, columns: %s",
                         entityType,
                         vector.df.shape,
                         vector.scale,
                         vector.offset,
                         ",".join(vector.df.columns)
            )
            # Now we will turn the dataframe into a series with a
            # multilevel index. The index will have four keys:
            # (sourceRef, metric, hour, minute)
            for metric in m.metrics.keys():
                logging.info("Creating series for metric %s", metric)
                slim_df = vector.df[['sourceref', 'hour', 'minute', metric]].copy()
                slim_df['metric'] = metric
                slim_df = slim_df.set_index(['sourceref', 'metric', 'hour', 'minute'])
                vector_list.append(slim_df.squeeze())
        vector = pd.concat(vector_list, axis=0)
        print("FINAL VECTOR FOR ", trend, ", ", daytype, ":\n", vector)

        #hidden = encode_vector(metadata=m, trend=scene_data.trend, daytype=scene_data.daytype, vector=vector)
        #sim_result = simulate_scene(metadata=m, trend=scene_data.trend, daytype=scene_data.daytype, hidden=hidden)
        #m.save_data(engine=engine, data=sim_result)


def encode_vector(metadata: Metadata, trend: str, daytype: str, vector=pd.Series):
    """
    Run the encoder over the given vector, and return the corresponding hidden states
    """
    return vector

def simulate_scene(metadata: Metadata, trend: str, daytype: str, hidden=pd.Series):
    """
    Run the simulation, given the hidden state vector.

    Returns a series with the results vector, scaled. The results should be
    unscaled before saving.
    """
    return hidden

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
    args = parser.parse_args()

    for config in args.config:
        logging.debug("loading config file %s", config)
        loadConfig(pathlib.Path(config[0]))

    meta = read_meta(pathlib.Path(args.meta))
    logging.info("Configuration:\n%s", json.dumps(dumpConfig(), indent=2))
    logging.info("Metadata order:\n%s", ", ".join(meta.keys()))

    try:
        with psql_engine() as engine:
            vectorize(meta, engine)
        logging.info("ETL OK")
    except Exception as err:
        logging.exception(msg="Error during vectorization", stack_info=True)
