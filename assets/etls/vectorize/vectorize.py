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
import torch


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
    Contains data for a particular set of aeasures
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
    Holds the properties of a regularized dataset for a given
    entity type.

    A regularized dataset must be scaled prior to analysis, so
    that all values are comparable and the encoder does not
    get too much issues with the scale.
    
    So in this implementation, all vales are scaled between
    0 and 1:
      - metrics that contain probabilites are left as is.
      - metrics that do not contain probabilities are scaled
        to be between 0 and 1.
        If metrics could be negative, an offset would be applied
        before scaling. IT is currently not the case for any
        metric.

    In order to de-scale a metric, first you should multiply
    by the scale factor and then add the offset value.
    """
    entityType: str
    offset: typing.Dict[str, float]
    scale: typing.Dict[str, float]

@dataclass
class TypedVector(VectorProperties):
    """
    Holds the data of a regularized dataset for a given entity type.
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

    def dim_df(self, sceneref: str) -> TextClause:
        """Build SQL query to determine all entity IDs in the model"""
        if self.multiZone:
            columns = "sourceref, zone, zonelist, ST_AsGeoJSON(location) AS location"
        else:
            columns = "sourceref, zone, Array[zone]::json[] as zonelist, ST_AsGeoJSON(location) AS location"
        return text(f"SELECT {columns} FROM {self.dimsTableName} ORDER BY sourceref ASC")

    def dim_data(self, engine: Engine, sceneref: str) -> pd.DataFrame:
        """Builds a dataframe of all entity IDs in the model"""
        query = self.dim_df(sceneref)
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

    def scene_data(self, engine: Engine, sceneref: str, timeinstant: datetime) -> typing.Iterable[Dataset]:
        """Retrieves datasets for all trends and daytypes of the scene"""
        query = self.scene_query()
        df = pd.read_sql(query.bindparams(sceneref=sceneref, timeinstant=timeinstant), engine)
        # Separate by trend and dayType
        for group, data in df.groupby(['trend', 'daytype']):
            yield Dataset(
                timeinstant=timeinstant,
                trend=group[0],
                daytype=group[1],
                entityType=self.entityType,
                df=data
            )

    def fixed_df(self, dims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a placeholder dataset with a fixed size. The generated
        dataset will have the columns: "sourceref", "hour" and "minute",
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
        Turns a regularized dataset into a typed vector, i.e.:

        - Sorts entries so that they match the order in fixed_df.
        - Fills in missing metrics for hours or minutes, with NaN.
        - Scales metrics so that the vector information is within range [0, 1]
        
        The dataset must be regularized in time, i.e. there must be only
        one entry per "sourceref" and set of dimensions:

        - if "hasHour" is true, there must be only one entry per sourceref
          and hour
        - if "hasMinute" is true, there must be only one entry per sourceref,
          hour and ten-minute interval.

        Each dataset is regularized differently. See the documentation of
        datasets for more infor on regularization.
        """
        typed_vector = TypedVector(
            entityType=self.entityType,
            offset={
                k: 0 for k in self.metrics.keys()
            },
            scale={
                k: 1 for k in self.metrics.keys()
            },
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
            # All our measures are either probabilities or intensities,
            # larger than 0 in any case.
            # We will normalize intensities to [0, 1] so that
            # they are within the range of the vector.
            for metric, props in self.metrics.items():
                if props.probability:
                    continue
                max_val = float(dataset[metric].max())
                if max_val > 0:
                    # Keep track of the scale factor to be able to de-scale later.
                    typed_vector.scale[metric] = max_val
                    dataset[metric] = dataset[metric] / max_val
            # Finally, do the merge of the fixed_df to the scaled metrics
            typed_vector.df = pd.merge(
                typed_vector.df,
                dataset,
                how='left',
                on=on_columns
            )
        return typed_vector

    def extract(self, props: VectorProperties, vector: pd.Series) -> TypedVector:
        """
        Extract the part corresponding to this entitytype from
        a pd.Series that has a multi-index with the following
        values:
        (entitytype, metric, sourceref, hour, minute)
        """
        typed_series = vector.loc[props.entityType]
        if not self.metrics:
            # If the entity type has no metrics, we still need
            # to identify the proper sourcerefs, because
            # the simulation might have added or removed
            # entities.
            # In order to do so, we remove the next level from
            # the multiindex, which in regular conditions would
            # be the metric name; and rename the columns
            # to just "_none_".
            df = typed_series.loc['_none_'].to_frame()
            df.columns = ['_none_']
        else:
            # Extract the rows corresponding to each metric
            metrics = []
            for metric in self.metrics.keys():
                # Get measures for the metric
                metric_series = typed_series.loc[metric]
                metric_offset = props.offset[metric]
                metric_scale = props.scale[metric]
                metric_series = metric_series * metric_scale + metric_offset
                # Rename the value column to the metric
                metric_series.name = metric
                metrics.append(metric_series)
            # concatenate all metrics as columns
            df = pd.concat(metrics, axis=1)
        # Drop NaN and 0, but make sure we return at least one row per
        # sourceref, otherwise the sourceref will not be present in
        # the simulation dashboard.
        groups = []
        for sourceref, group in df.groupby(level='sourceref'):
            # This filters out the rows where all values are 0
            group = group.fillna(0)
            group = group.loc[~(group == 0).all(axis=1)]
            if group.empty:
                original_group = df.loc[sourceref]
                group = original_group.head(1)
            # turn "hour" and "minute" into columns
            group = group.reset_index()
            # overwrite other columns
            group['entitytype'] = props.entityType
            group['sourceref'] = sourceref
            groups.append(group)
        # concatenate all groups
        df = pd.concat(groups, axis=0).reset_index()
        if '_none_' in df.columns:
            df.drop('_none_', axis=1, inplace=True)
        return TypedVector(
            entityType=props.entityType,
            offset=props.offset,
            scale=props.scale,
            df=df
        )

# -------------------------------------
# Schemaless types
# -------------------------------------

@dataclass
class Vector:
    """
    Untyped Vector class.

    Contains both the complete series of metrics that make up
    the inpt of the encoder, as well as the properties of all
    TypedVectors that went into the series.

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
            props[entityType] = VectorProperties(
                entityType=typed_vector.entityType,
                offset=typed_vector.offset,
                scale=typed_vector.scale
            )
            # Add entityType to the dataframe. If the entity type has
            # no metrics, add a "fake" metric "_none_" with value np.NaN.
            typed_vector.df['entitytype'] = entityType
            metric_keys = list(meta.metrics.keys())
            if not meta.metrics:
                typed_vector.df['_none_'] = np.NaN
                metric_keys = ['_none_']
            # Turn the dataframe into a series with a
            # multilevel index. The index will have the following keys:
            # (entitytype, metric, sourceref, hour, minute)
            for metric in metric_keys:
                slim_df = typed_vector.df[['entitytype', 'sourceref', 'hour', 'minute', metric]].copy()
                slim_df['metric'] = metric
                slim_df = slim_df.set_index(['entitytype', 'metric', 'sourceref', 'hour', 'minute'])
                vector_list.append(slim_df.squeeze())
            vector = pd.concat(vector_list, axis=0)
        return Vector(properties=props, df=vector.astype(np.float64))

@dataclass
class HiddenLayer:
    """
    Represents the hidden layer of the autoencoder
    """
    private: torch.Tensor

class Decoder:
    """
    This class decodes the hidden layer to an output vector.
    """
    meta_map: typing.Mapping[str, Metadata]
    # This series contains the index for the output vector.
    # This series is indexed by (entityType, metric, sourceRef, hour, minute)
    vector_index: pd.MultiIndex
    # This is the decoding weights and biases
    weights: torch.Tensor
    biases: torch.Tensor

    def __init__(self, meta_map: typing.Mapping[str, Metadata], index: pd.MultiIndex):
        """Builds the decoder with the given metadata and props"""
        self.meta_map = meta_map
        self.vector_index = index
        self.weights = torch.eye(len(index))
        self.biases = torch.zeros(len(index))

    def decode(self, props: DatasetProperties, hidden: HiddenLayer) -> pd.Series:
        """
        Run the decoder over the given hidden state tensor, and return the corresponding vector
        """
        result = torch.matmul(self.weights, hidden.private)
        result = result + self.biases
        return pd.Series(result.numpy(), index=self.vector_index)

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
    df = pd.read_sql(query.bindparams(sceneref=sceneref), engine)
    print(df)
    return df.iloc[0]['timeinstant']

def main(metadata: typing.Mapping[str, Metadata], engine: Engine):
    """
    Vectorizes the data in the database
    """
    # Get the latest identity we are working with
    identityref = os.getenv("ETL_VECTORIZE_IDENTITYREF", "N/A")
    last_sim_date = last_simulation(engine=engine, sceneref=identityref)
    logging.info("Latest simulation for sceneref %s: %s", identityref, last_sim_date)

    # Group all data by combinations of trend and daytype, and then by entityType
    scene_by_type: typing.Dict[typing.Tuple[str, str], typing.Dict[str, Dataset]] = defaultdict(dict)
    dims_df_map: typing.Dict[str, pd.DataFrame] = {}
    fixed_df_map: typing.Dict[str, pd.DataFrame] = {}
    for entityType, meta in metadata.items():
        entity_dims = meta.dim_data(engine=engine, sceneref=identityref)
        logging.info("Dims shape for scene %s, entity type %s: %s", identityref, entityType, entity_dims.shape)
        dims_df_map[entityType] = entity_dims
        fixed_df_map[entityType] = meta.fixed_df(entity_dims)
        for scene_data in meta.scene_data(engine=engine, sceneref=identityref, timeinstant=last_sim_date):
            logging.info("Dataset shape for scene %s, timeinstant %s, trend %s, daytype %s, entity type %s: %s",
                identityref,
                last_sim_date,
                scene_data.trend,
                scene_data.daytype,
                entityType,
                scene_data.df.shape
            )
            scene_by_type[(scene_data.trend, scene_data.daytype)][entityType] = scene_data

    # Crete the decoder
    empty_vector = Vector.create(meta_map=metadata, fixed_df_map=fixed_df_map, data_map={})
    decoder = Decoder(meta_map=metadata, index=typing.cast(pd.MultiIndex, empty_vector.df.index))

    # Iterate over all combinations of trend and daytype
    for scene_index, entities in scene_by_type.items():
        trend, daytype = scene_index
        # Turn typed data into vector
        vector = Vector.create(meta_map=metadata, fixed_df_map=fixed_df_map, data_map=entities)
        logging.info("Vector shape for scene %s, timeinstant %s, trend %s, daytype %s: %s",
            identityref,
            last_sim_date,
            trend,
            daytype,
            vector.df.shape
        )

        # Write input vector for debugging purposes
        input_vector_path = f"input_vector_{trend}_{daytype}.csv"
        logging.info("Saving input vector to %s", input_vector_path)
        vector.df.to_csv(input_vector_path)
        print("** DTYPE: ", vector.df.dtype)

        # Encode, perturb and decode
        hidden = encode_vector(metadata=meta, props=scene_data, vector=vector)
        simulated_state = perturb_hidden(metadata=meta, props=scene_data, hidden=hidden)
        simulated_result = decoder.decode(props=scene_data, hidden=simulated_state)

        # Write output vector for debugging purposes
        output_vector_path = f"output_vector_{trend}_{daytype}.csv"
        logging.info("Saving output vector to %s", output_vector_path)
        simulated_result.to_csv(output_vector_path)

        # Split into TypedVectors
        for entityType, meta in metadata.items():
            typed_vector = meta.extract(props=vector.properties[entityType], vector=simulated_result)

def encode_vector(metadata: Metadata, props: DatasetProperties, vector: Vector) -> HiddenLayer:
    """
    Run the encoder over the given vector, and return the corresponding hidden states
    """
    return HiddenLayer(private=torch.Tensor(vector.df.to_numpy()))

def perturb_hidden(metadata: Metadata, props: DatasetProperties, hidden: HiddenLayer) -> HiddenLayer:
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
            main(meta, engine)
        logging.info("ETL OK")
    except Exception as err:
        logging.exception(msg="Error during vectorization", stack_info=True)
