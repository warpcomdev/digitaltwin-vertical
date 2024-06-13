import logging

import pandas as pd
import json
import datetime
import os
import requests
from typing import Dict, List
import geojson
from dotenv import load_dotenv
from shapely.geometry import shape
from rutinas_auxiliares import send_data_to_CB, calculo_distritos

URL_VLCI_ESPIRAS = 'https://geoportal.valencia.es/apps/OpenData/Trafico/tra_espiras_p.json'
ENTITYTYPE = 'TrafficIntensity'
FIWARE_PATH_SERVICE = '/digitaltwin'
NAMES_FILE = 'nombres_puntos_medida_tráfico.csv'

def set_point_name(df_data:pd.DataFrame): # Provisional procedure. Method to be defined

    df = pd.read_csv(NAMES_FILE)
    dict_names = dict(zip(df['entityid'].to_list(), df['name'].to_list())) # Dictionary of names

    df_data['name'] = df_data['entityid'].map(lambda x: dict_names.get(x, ''))
    return df_data


def get_measure_points_data() -> List:

    url = URL_VLCI_ESPIRAS
    headers = {'accept': 'application/json'}
    try:
        resul = requests.get(url=url, headers=headers)
    except Exception as e:
        print(f"Error: {e.args}")
        return [] # Empty list
    else:
        if resul.status_code == 200:  # Successful
            data = json.loads(resul.text)
            return data['features']
        else:
            print(f"There was a problem: {resul.text}")
            return []  # Empty list

def process_measure_points_raw_data(raw_data_list:List) -> pd.DataFrame:

    df_measure_points = pd.DataFrame()

    for item in raw_data_list:
        row = pd.DataFrame()
        row['entityid'] = [item['properties']['idpm']]
        row['geom'] = [item['geometry']]
        row['latitud'] = [item['geometry']['coordinates'][1]]
        row['longitud'] = [item['geometry']['coordinates'][0]]
        df_measure_points = pd.concat([df_measure_points, row])

    df_measure_points.drop_duplicates(subset=['entityid', 'latitud', 'longitud'], inplace=True)

    # Now, we have to calculate the city district where the measure point are and add it in column 'zone'
    df_distritos = calculo_distritos(df_measure_points, 'entityid', 'latitud', 'longitud')
    dict_puntos_distrito = dict(zip(df_distritos['entityid'].to_list(), df_distritos['coddistrit'].to_list()))
    df_measure_points['zone'] = df_measure_points['entityid'].map(lambda x: dict_puntos_distrito.get(x, 0))

    return df_measure_points

def ETL_trafficintensity_lastdata() -> pd.DataFrame:

    timeinstant = datetime.datetime.now()
    timeinstant = timeinstant.replace(hour=0, minute=0, second=0, microsecond=0)  # Fecha de cálculo
    timeinstant = str(timeinstant.isoformat())  # CB needs str on ISO format

    raw_data = get_measure_points_data()  # Data from public API
    df_measure_points = process_measure_points_raw_data(raw_data)

    # Creation of new column with location in WKT format from geojson
    df_measure_points['location'] = df_measure_points['geom']

    # Now we adapt our DataFrame to the structure PostgreSQL table
    df_measure_points['entityid'] = df_measure_points['entityid'].map(lambda x: 'puntoMedida_' + str(x) + '_tra')
    df_measure_points['timeinstant'] = timeinstant
    df_measure_points['sourceref'] = df_measure_points['entityid']
    df_measure_points['entitytype'] = ENTITYTYPE
    df_measure_points['fiwarepathservice'] = FIWARE_PATH_SERVICE

    set_point_name(df_measure_points)  # Name (address) of measure point (provisional method)
    df_measure_points.drop(columns=['geom', 'latitud', 'longitud'], inplace=True) # Deletion of useless fields

    return df_measure_points


if __name__ == '__main__':

    load_dotenv(os.path.join(os.getcwd(), 'config.env'))  # Loads enviromments variables

    logging.basicConfig(
    level=os.getenv('ETL_LOG_LEVEL', 'DEBUG'),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()])

    logging.info('Start of execution ETL_trafficcongestion_lastdata')

    df = ETL_trafficintensity_lastdata()
    if df.empty:
        logging.info('No data obtained from web source')
    else:
        send_data_to_CB(df)  # Send data to Context Broker

    logging.info('End of execution')
