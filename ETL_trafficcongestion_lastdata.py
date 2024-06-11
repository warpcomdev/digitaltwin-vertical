import datetime
import json
import logging
import os
from typing import List

import pandas as pd
import requests

from rutinas_auxiliares import send_data_to_CB, calculo_distritos

URL_ESTADO_TRAFICO = ('http://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/'
                      'estat-transit-temps-real-estado-trafico-tiempo-real/exports/json?'
                      'limit=-1&timezone=UTC&use_labels=false&epsg=4326')
ENTITYTYPE = 'TrafficCongestion'
FIWARE_PATH_SERVICE = '/digitaltwin'
#NAMES_FILE = 'F:/desarrollo/warpcom/gemelo/nombres_puntos_medida_tráfico.csv'

# def set_point_name(df_data:pd.DataFrame): # Provisional procedure. Method to be defined
#
#     df = pd.read_csv(NAMES_FILE)
#     dict_names = dict(zip(df['entityid'].to_list(), df['name'].to_list())) # Dictionary of names
#
#     df_data['name'] = df_data['entityid'].map(lambda x: dict_names.get(x, ''))
#     return df_data


def get_measure_points_raw_data() -> List:

    url = URL_ESTADO_TRAFICO
    headers = {'accept': 'application/json'}
    try:
        resul = requests.get(url=url, headers=headers)
    except Exception as Argument:
        logging.exception('Error: ', Argument)
        # print(f"Error: {e.args}")
        return [] # Empty list
    else:
        if resul.status_code == 200:  # Successful
            data = json.loads(resul.text)
            return data
        else:
            logging.error('There was a problem:', resul.text)
            # print(f"There was a problem: {resul.text}")
            return []  # Empty list

def process_measure_points_raw_data(raw_data_list:List) -> pd.DataFrame:

    df_measure_points = pd.DataFrame()

    for item in raw_data_list:
        row = pd.DataFrame()
        row['entityid'] = [item['idtramo']]
        row['geom'] = [item['geo_shape']['geometry']]
        row['latitud'] = [item['geo_point_2d']['lat']]
        row['longitud'] = [item['geo_point_2d']['lon']]
        row['name'] = [item['denominacion']]
        df_measure_points = pd.concat([df_measure_points, row])

    df_measure_points.drop_duplicates(subset=['entityid'], inplace=True)

    # Now, we have to calculate the city district where the measure point are and add it in column 'zone'
    df_distritos = calculo_distritos(df_measure_points, 'entityid', 'latitud', 'longitud')
    dict_puntos_distrito = dict(zip(df_distritos['entityid'].to_list(), df_distritos['coddistrit'].to_list()))
    df_measure_points['zone'] = df_measure_points['entityid'].map(lambda x: str(dict_puntos_distrito.get(x, 0)))

    return df_measure_points

def ETL_trafficintensity_lastdata() -> pd.DataFrame:

    timeinstant = datetime.datetime.now()
    timeinstant = timeinstant.replace(hour=0, minute=0, second=0, microsecond=0)  # Fecha de cálculo
    timeinstant = str(timeinstant.isoformat())  # CB needs string of ISO format

    raw_data = get_measure_points_raw_data()  # Data from public API
    if not raw_data:
        df = pd.DataFrame()
        return df  # Return empty dataframe as orginal data couldn't be gotten

    df_measure_points = process_measure_points_raw_data(raw_data)


    #df_measure_points['location'] = df_measure_points['geom'].map(lambda x: shape(geojson.loads(json.dumps(x))))
    df_measure_points['location'] = df_measure_points['geom']

    # Now we adapt our DataFrame to the structure PostgreSQL table
    df_measure_points['entityid'] = df_measure_points['entityid'].map(lambda x: 'puntoMedida_' + str(x) + '_tra')
    df_measure_points['timeinstant'] = timeinstant
    df_measure_points['sourceref'] = df_measure_points['entityid']
    df_measure_points['entitytype'] = ENTITYTYPE
    df_measure_points['fiwarepathservice'] = FIWARE_PATH_SERVICE

    #set_point_name(df_measure_points)  # Name (address) of measure point (provisional method)
    df_measure_points.drop(columns=['geom', 'latitud', 'longitud'], inplace=True) # Deletion of useless fields

    return df_measure_points


if __name__ == '__main__':

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
