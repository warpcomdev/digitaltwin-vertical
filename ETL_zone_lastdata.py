import ast
import datetime
import json
import logging
import os
import sys
from typing import Any

import geopandas
import pandas as pd
import requests
import shapely
from dotenv import load_dotenv
from shapely.geometry import shape

from rutinas_auxiliares import send_data_to_CB

geopandas.options.io_engine = "pyogrio"

ENTITYTYPE = 'Zone'
FIWARE_PATH_SERVICE = '/digitaltwin'
PYOGRYO_FILE = 'barris-barrios.shp'

URL_DISTRITOS = ('https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/districtes-distritos/exports/'
                 'csv?lang=es&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B')


def get_geometry(geo_data: pd.Series) -> Any:
    if len(geo_data) == 1:  # It is a single polygon
        return json.loads(geo_data.iloc[0])

    else:  # This district is defined by more than a Polygon -> we have to convert in a single MultiPolygon
        pass
        list_polygons = geo_data.to_list()
        list_polygons = [ast.literal_eval(x) for x in list_polygons]
        # list_polygons = [shapely.wkt.loads(poly) for poly in list_polygons]
        list_polygons = [shape(x).wkt for x in list_polygons]
        list_polygons = [shapely.wkt.loads(poly) for poly in list_polygons]  # Translate to WKT
        mp_wkt =  shapely.geometry.MultiPolygon(list_polygons)  # We convert a list of two Polygons t MultiPolygon WKT
        # mp_geo = shape(mp_wkt)
        mp_geo = shapely.to_geojson(mp_wkt) # We pass from WKT a GeoJson, suitable for CB

        return json.loads(mp_geo)


def get_district_raw_data():
    url = URL_DISTRITOS
    df = pd.DataFrame()
    try:
        resul = requests.get(url=url)
    except Exception as e:
        print(f"Error: {e.args}")
        return df  # Empty dataframe
    else:
        if resul.status_code == 200:  # Successful
            resp = requests.get(url=url)
            outfil = os.path.join(os.getcwd(), 'dis.csv')
            with open(outfil, 'w', encoding='UTF-8') as f:
                f.write(resp.text)
            df = pd.read_csv(outfil, sep=';')
            # os.remove(outfil)
            return df
        else:
            print(f"There was a problem: {resul.text}")
            return df  # Empty dataframe


def process_raw_district_data(df: pd.DataFrame) -> pd.DataFrame:
    timeinstant = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    timeinstant = str(timeinstant.isoformat())
    df_districts = pd.DataFrame()
    district_list = list(df['Código distrito'].unique())  # List of city districts

    df_group = df.groupby('Código distrito')
    for distrito in district_list:
        entityid = str(distrito)
        row = pd.DataFrame()  # Auxiliary dataframe with only one column
        row['timeinstant'] = [timeinstant]
        row['recvtime'] = [timeinstant]
        row['entityid'] = [entityid]
        row['entitytype'] = [ENTITYTYPE]
        row['zoneid'] = [entityid]
        row['sourceref'] = [entityid]
        row['name'] = df_group.get_group(distrito).iloc[0]['Nombre']
        row['label'] = format(distrito, '02d') + '_' + row['name']
        geometry = get_geometry(df_group.get_group(distrito)['geo_shape'])
        row['location'] = [geometry]
        df_districts = pd.concat([df_districts, row], ignore_index=True)
    pass
    return df_districts


if __name__ == '__main__':

    load_dotenv(os.path.join(os.getcwd(), 'config.env'))

    logging.basicConfig(
        level=os.getenv('ETL_LOG_LEVEL', 'DEBUG'),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()])

    logging.info('Start of execution ETL_zone_lastdata')

    df_districts = pd.DataFrame()
    df = get_district_raw_data()
    if df.empty:
        logging.info('No data obtained from web source')

    else:
        df_districts = process_raw_district_data(df)
        send_data_to_CB(df_districts)  # Send data to Context Broker

    logging.info('End of execution')

