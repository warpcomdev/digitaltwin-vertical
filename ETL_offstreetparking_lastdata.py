import datetime
import json
import logging
import os
from typing import List

import pandas as pd
import requests
from dotenv import load_dotenv

from rutinas_auxiliares import send_data_to_CB, calculo_distritos

ENTITYTYPE = 'OffStreetParking'
FIWARE_PATH_SERVICE = '/digitaltwin'

URL_VALENCIA_OFFSTREETPARKINGS = ('https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/'
                                  'parkings/records?limit=-1')


def get_parkings_data() -> List:

    url = URL_VALENCIA_OFFSTREETPARKINGS
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
            return data['results']
        else:
            logging.error('There was a problem: ', resul.text)
            #print(f"There was a problem: {resul.text}")
            return []  # Empty list


def process_parkings_raw_data(raw_data_list: List) -> pd.DataFrame:
    df_parkings = pd.DataFrame()

    for item in raw_data_list:
        row = pd.DataFrame()
        row['entityid'] = [item['id_aparcamiento']]
        row['geom'] = [item['geo_shape']['geometry']]
        row['latitud'] = [item['geo_shape']['geometry']['coordinates'][1]]
        row['longitud'] = [item['geo_shape']['geometry']['coordinates'][0]]
        row['name'] = [item['nombre']]
        row['capacity'] = [str(item['plazastota'])]
        df_parkings = pd.concat([df_parkings, row])

    df_parkings.drop_duplicates(subset=['entityid', 'latitud', 'longitud'], inplace=True)

    # Now, we have to calculate the city district where the measure point are and add it in column 'zone'
    df_distritos = calculo_distritos(df_parkings, 'entityid', 'latitud', 'longitud')
    dict_puntos_distrito = dict(zip(df_distritos['entityid'].to_list(), df_distritos['coddistrit'].to_list()))
    df_parkings['zone'] = df_parkings['entityid'].map(lambda x: str(dict_puntos_distrito.get(x, 0)))

    return df_parkings


def etl_offstreetparking_lastdata() -> pd.DataFrame:

    timeinstant = datetime.datetime.now()
    timeinstant = timeinstant.replace(hour=0, minute=0, second=0, microsecond=0)  # Fecha de cálculo
    timeinstant =str(timeinstant.isoformat())

    raw_data = get_parkings_data()  # Data from public API
    df_parkings = process_parkings_raw_data(raw_data)

    # Creation of new column with location in WKT format from geojson
    #df_parkings['location'] = df_parkings['geom'].map(lambda x: shape(geojson.loads(json.dumps(x))))
    df_parkings['location'] = df_parkings['geom']

    # Now we adapt our DataFrame to the structure PostgreSQL table
    df_parkings['entityid'] = df_parkings['entityid'].map(lambda x: 'Parking_' + str(int(x)))
    df_parkings['timeinstant'] = timeinstant
    df_parkings['sourceref'] = df_parkings['entityid']
    df_parkings['entitytype'] = ENTITYTYPE
    df_parkings['fiwarepathservice'] = FIWARE_PATH_SERVICE

    df_parkings.drop(columns=['geom', 'latitud', 'longitud'], inplace=True)  # Deletion of useless fields
    #df_parkings.to_csv('e:prueba.csv', index=False, sep=';')

    return df_parkings


if __name__ == '__main__':

    load_dotenv(os.path.join(os.getcwd(), 'config.env'))  # Loads enviromments variables

    logging.basicConfig(
        level=os.getenv('ETL_LOG_LEVEL', 'DEBUG'),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()])

    logging.info('Start of execution ETL_offstreetparking_lastdata')

    df = etl_offstreetparking_lastdata()
    if df.empty:
        logging.info('No data obtained from web source')
    else:
        send_data_to_CB(df)

    logging.info('End of execution')