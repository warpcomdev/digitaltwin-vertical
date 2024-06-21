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
from dataclasses import dataclass
from contextlib import contextmanager, ExitStack
from sqlalchemy import create_engine, event, text, URL, Engine
import pandas as pd
from shapely import geometry

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
    print("URL_OBJECT: %s", url_object)
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
    
    @staticmethod
    def create_from_lastdata(entityType: str, cols: typing.Dict[str, str]) -> 'Metadata':
        """Fake metadata for non-twin entities"""
        return Metadata(
            dimensions=[],
            metrics={},
            fixedProps={},
            non_metrics=cols,
            calcs={},
            hasHour=False,
            hasMinute=False,
            multiZone=False,
            namespace="dtwin",
            entityType=entityType,
            dataTableName=f"dtwin_{entityType.lower()}_lastdata",
            dimsTableName="",
        )

def meta_to_csv(engine: Engine, meta: Metadata, label: str):
    """Dump metadata to a CSV file"""
    columns = ({
        k: v.ngsiType for k, v in meta.metrics.items()
    })
    columns.update({
        k: v for k, v in meta.non_metrics.items()
    })
    with engine.begin() as conn:
        sql_cols = [k.lower() for k, v in columns.items() if v != 'geo:json']
        sql_cols += [f"ST_AsGeoJSON({k.lower()}) AS {k.lower()}" for k, v in columns.items() if v == 'geo:json']
        # Read from data table, or from sim table if the entty has both dims and data
        tableName = meta.dataTableName
        if meta.dimsTableName:
            tableName = f"{meta.dataTableName}_sim"
        query = text(f"SELECT entityid, {','.join(sql_cols)} FROM {tableName} WHERE sceneref='N/A'")
        if not 'sceneRef' in meta.non_metrics:
            query = text(f"SELECT entityid, {','.join(sql_cols)} FROM {tableName}")
        dims = pd.read_sql(query, conn)
        # Split into two groups, one of them will have only one row per
        # entityId, the other group will have the reamining rows
        if 'sourceref' in dims.columns:
            dims_grouped = dims.groupby('sourceref').tail(1)
            dims_last = dims_grouped.reset_index(drop=True)
            dims_other = dims.drop(dims_last.index).reset_index(drop=True)
            for k in meta.non_metrics.keys():
                dims_other[k] = None
            dims = pd.concat([dims_other, dims_last], axis=0)
        # Take the columns we need and add entityId and entityType
        cols_rename = {
            k.lower(): f"{k}<{v}>" for k, v in columns.items()
        }
        cols_rename['entityid'] = 'entityID'
        dims_csv = dims[list(cols_rename.keys())].copy()
        dims_csv['entityType'] = meta.entityType
        # rename to the proper entity attrib names
        dims_csv = dims_csv.rename(columns=cols_rename)
        # reorder to match the expected order in CSVs
        final_cols = dims_csv.columns.to_list()
        fixed_cols = ['entityID', 'entityType']
        final_cols = fixed_cols + list(frozenset(final_cols).difference(fixed_cols))
        dims_csv = dims_csv[final_cols]
        dims_csv.to_csv(f"{label}.csv", index=False)

if __name__ == "__main__":
    logging.basicConfig(
        level= os.getenv('ETL_LOG_LEVEL', 'DEBUG'),
        format="time=%(asctime)s | lvl=%(levelname)s | comp=ETL-DIGITALTWIN-DUMP | op=%(name)s:%(filename)s[%(lineno)d]:%(funcName)s | msg=%(message)s",
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
            meta_file = stack.enter_context(open(args.meta, "r", encoding="utf-8"))
            items = (Metadata.create(params) for params in json.load(meta_file))
            meta = {item.entityType: item for item in items}
            meta = {k: meta[k] for k in sorted(meta.keys())}
            logging.info("Metadata order:\n%s", ", ".join(meta.keys()))
            meta.update({
                'Zone': Metadata.create_from_lastdata('Zone', {
                    'TimeInstant': 'DateTime',
                    'zoneId': 'Number',
                    'name': 'TextUnrestricted',
                    'label': 'TextUnrestricted',
                    'location': 'geo:json',
                }),
                'DayType': Metadata.create_from_lastdata('DayType', {
                    'TimeInstant': 'DateTime'
                }),
                'Trend': Metadata.create_from_lastdata('Trend', {
                    'TimeInstant': 'DateTime'
                }),
                'Simulation': Metadata.create_from_lastdata('Simulation', {
                    'TimeInstant': 'DateTime',
                    'sceneRef': 'Text',
                    'name': 'TextUnrestricted',
                    'description': 'TextUnrestricted',
                }),
            })
            for label, m in meta.items():
                meta_to_csv(engine, m , label)
        logging.info("ETL OK")
    except Exception as err:
        logging.exception(msg="Error during vectorization", stack_info=True)
        sys.exit(-1)
