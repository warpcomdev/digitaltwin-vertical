import datetime
import json
import logging
import os
from typing import List

import pandas as pd
import requests

from rutinas_auxiliares import send_data_to_CB, calculo_distritos

ENTITYTYPE = 'AirQualityObserved'
FIWARE_PATH_SERVICE = '/digitaltwin'

URL_VALENCIA_AIRQUALITY = 'https://geoportal.valencia.es/apps/OpenData/MedioAmbiente/estatautomaticas.json'

# As the names of the stations does not match in the observation database and in official web, we compose a
# dictionary to relate both names
dict_names = {'Olivereta': 'A10_OLIVERETA', 'Pista de Silla': 'A04_PISTASILLA', 'Francia': 'A01_AVFRANCIA',
              'Centro': 'A07_VALENCIACENTRE', 'Boulevar Sur': 'A02_BULEVARDSUD', 'Molí del Sol': 'A03_MOLISOL',
              'Universidad Politécnica': 'A05_POLITECNIC', 'Viveros': 'A06_VIVERS', 'Dr. Lluch': 'A08_DR_LLUCH',
              'Cabanyal': 'A09_CABANYAL', 'Patraix': 'A11_PATRAIX'}


def get_airquality_stations_data() -> List:
    """
    Access to official data in geoportal.valencia to get information (JSON format) about the stations that measure
    the air quality in the city
    :return: List of dictionaries with the data of every station
    """

    url = URL_VALENCIA_AIRQUALITY
    headers = {'accept': 'application/json'}
    try:
        resul = requests.get(url=url, headers=headers)
    except Exception as Argument:
        logging.exception('Error: ', Argument)
        # print(f"Error: {e.args}")
        return []  # Empty list
    else:
        if resul.status_code == 200:  # Successful
            data = json.loads(resul.text)
            return data['features']
        else:
            logging.error('There was a problem: ', resul.text)
            # print(f"There was a problem: {resul.text}")
            return []  # Empty list


def process_stations_raw_data(raw_data_list: List) -> pd.DataFrame:
    """
    With data of geoportal.valencia this routine makes a Dataframe that has a structure similar to the final
    database
    :param raw_data_list: List of station data obtained from get_airquality_station
    :return: Dataframe with basic fields of final database
    """

    df_stations = pd.DataFrame()

    for item in raw_data_list:  # From the list of data (one object for each station)
        row = pd.DataFrame()  # Auxiliar DataFrame with only one row
        row['entityid'] = [dict_names.get(item['properties']['nombre'], '')]
        row['geom'] = [item['geometry']]
        row['latitud'] = [item['geometry']['coordinates'][1]]
        row['longitud'] = [item['geometry']['coordinates'][0]]
        row['name'] = [item['properties']['nombre']]
        df_stations = pd.concat([df_stations, row])

    # df_stations.drop_duplicates(subset=['entityid', 'latitud', 'longitud'], inplace=True)

    # Now, we have to calculate the city district where the measure point are and add it in column 'zone'
    df_distritos = calculo_distritos(df_stations, 'entityid', 'latitud', 'longitud')
    dict_puntos_distrito = dict(zip(df_distritos['entityid'].to_list(), df_distritos['coddistrit'].to_list()))
    df_stations['zone'] = df_stations['entityid'].map(lambda x: dict_puntos_distrito.get(x, 0))

    # As there are 11 stations that are referred in database with two different names, we have to duplicate records
    # in df_stations and append to the entityid field '_24h' or '_60m
    df_stations = pd.concat([df_stations, df_stations], ignore_index=True)

    for i in range(len(df_stations)):
        if i < len(df_stations) / 2:
            df_stations.loc[i, 'entityid'] = df_stations.loc[i, 'entityid'] + '_60m'
        else:
            df_stations.loc[i, 'entityid'] = df_stations.loc[i, 'entityid'] + '_24h'

    return df_stations


def etl_airqualityobserved_lastdata() -> pd.DataFrame:
    """
    Invokes procedures get_airquality_stations_data and process_stations_raw_data, getting this way a DataFrame
    with basic    data of the stations. Additionally, this procedure adds some static fields (timeinstant, recvtime,
    sourceref, entitytype, fiwarepathservice) and compose new column 'location' converting 'geom' to WKT format.
    After that, it gets rid of useless columns
    :return: DataFrame to be sent to Context Broker
    """

    timeinstant = datetime.datetime.now()
    timeinstant = timeinstant.replace(hour=0, minute=0, second=0, microsecond=0)  # Fecha de cálculo
    timeinstant = str(timeinstant.isoformat())

    raw_data = get_airquality_stations_data()  # Data from public API
    if not raw_data:
        df = pd.DataFrame()
        return df  # Return empty dataframe as orginal data couldn't be gotten

    df_stations = process_stations_raw_data(raw_data)

    # Creation of new column with location in WKT format from geojson
    # df_stations['location'] = df_stations['geom'].map(lambda x: shape(geojson.loads(json.dumps(x))))
    df_stations['location'] = df_stations['geom']

    # Now we adapt our DataFrame to the structure PostgreSQL table
    # df_stations['entityid'] = df_stations['entityid'].map(lambda x: 'puntoMedida_' + str(x) + '_tra')
    df_stations['timeinstant'] = timeinstant
    df_stations['recvtime'] = timeinstant
    df_stations['sourceref'] = df_stations['entityid']
    df_stations['entitytype'] = ENTITYTYPE
    df_stations['fiwarepathservice'] = FIWARE_PATH_SERVICE

    df_stations.drop(columns=['geom', 'latitud', 'longitud'], inplace=True)  # Deletion of useless fields

    return df_stations


if __name__ == '__main__':

    logging.basicConfig(
        level=os.getenv('ETL_LOG_LEVEL', 'DEBUG'),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()])

    logging.info('Start of execution ETL_airqualityobserved_lastdata')
    df = etl_airqualityobserved_lastdata()  # Data acquisition from official web and processing

    if df.empty:
        logging.info('No data obtained from web source')
    else:
        send_data_to_CB(df)  # Sen data to Context Broker

    logging.info('End of execution')
