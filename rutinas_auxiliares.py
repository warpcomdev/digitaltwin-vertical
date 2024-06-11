import logging
import typing
from dataclasses import dataclass

import pandas as pd
import os
import requests
import geopandas
from shapely.geometry import Point
from zipfile import ZipFile
from dotenv import load_dotenv
import tc_etl_lib as tc

geopandas.options.io_engine = "pyogrio"

PYOGRYO_FILE = 'barris-barrios.shp'

URL_SHP_DISTRICTS = ('https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/barris-barrios/exports/'
                     'shp?lang=es&timezone=Europe%2FBerlin')

dict_class_cb_data = {'sourceref': 'Text', 'entityid': 'Text', 'name': 'TextUnrestricted', 'zone': 'Text',
                      'entitytype': 'Text', 'location': 'geo:json', 'fiwarepathservice': 'Text', 'capacity': 'Number',
                      'forwardstops': 'Number', 'returnstops': 'Number', 'name_original': 'TextUnrestricted',
                      'timeinstant': 'DateTime', 'recvtime': 'DateTime', 'zonelist': 'Text', 'zoneid': 'Number',
                      'label': 'TextUnrestricted'}

@dataclass
class Broker:
    """
    Encapsulates the communication to the context broker
    """
    auth: typing.Optional[tc.authManager] = None
    cb: typing.Optional[tc.cbManager] = None

    @staticmethod
    def create() -> 'Broker':
        password = os.getenv('PASSWORD')
        if not password:
            logging.warning("No broker password provided, running in dettached mode")
            return Broker(auth=None, cb=None)
        auth = tc.auth.authManager(
            endpoint=os.getenv('ENDPOINT_KEYSTONE'),
            service=os.getenv('SERVICE'),
            subservice=os.getenv('SUBSERVICE'),
            user=os.getenv('USER'),
            password=password,
        )
        cb = tc.cb.cbManager(
            endpoint=os.getenv('ENDPOINT_CB'),
            sleep_send_batch=int(os.getenv('SLEEP_SEND_BATCH', '1')),
            timeout=int(os.getenv('TIMEOUT', '10')),
            post_retry_connect=float(os.getenv('POST_RETRY_CONNECT', '3')),
            post_retry_backoff_factor=float(os.getenv('POST_RETRY_BACKOFF_FACTOR', '2')),
            batch_size=int(os.getenv('BATCH_SIZE', '20')),
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

def calculo_distritos(input_df: pd.DataFrame, key: str, latitud: str, longitud: str) -> pd.DataFrame:
    """
    Partiendo de un fichero shp (pyogrio_file) que delimita la geografía de los distritos de la ciudad, esta rutina
    devuelve el distrito al que pertenecen una serie de puntos geográficos definidos por sus coordenadas y que se
    contienen en el DataFrame de entrada input_df. Este DataFrame ha de contener obligatoriamente tres columnas:
    - key: en esta columna se da el código o nombre identificativo del punto
    - latitud: la coordenada de latitud del punto
    - longitud: la coordenada de longitud del punto
    El resto de columnas (si se incluyen) no se tendrán en cuenta
    :param input_df: DataFrame de entrada de datos
    :param key: Nombre de la columna identificativa de los registros
    :param latitud: Nombre de la columna que contiene la latitud del punto
    :param longitud: Nombre de la columna que contiene la longitud del punto
    :return: Dataframe que da el distrito al que pertenece cada punto. Sólo contiene dos columnas: key (identificación
             del punto), y coddistrit, el distrito al que pertenece
    """
    load_dotenv(os.path.join(os.getcwd(), 'config.env'))  # Loads enviromments variables
    shp_dir = os.getenv('SHP_DIR')

    if os.path.exists(os.path.join(shp_dir, PYOGRYO_FILE)):  # Verify if shp file already exists

        df_geo = geopandas.read_file(os.path.join(shp_dir, PYOGRYO_FILE),
                                     engine='pyogrio')  # Lectura del fichero de Geopandas
    else:  # Get file from web
        success = get_shp_data()
        if success == 'OK':  # Data loaded
            df_geo = geopandas.read_file(os.path.join(shp_dir, PYOGRYO_FILE),
                                         engine='pyogrio')  # Lectura del fichero de Geopandas
        else:
            df = pd.DataFrame()
            return df  # Return empty DataFrame

    input_df['coords'] = list(zip(input_df[longitud], input_df[latitud]))
    input_df['coords'] = input_df['coords'].apply(Point)
    points = geopandas.GeoDataFrame(input_df, geometry='coords', crs=df_geo.crs)
    point_in_polys = geopandas.tools.sjoin(points, df_geo, predicate="within", how='left')
    point_in_polys.sort_values(by=[key], inplace=True)
    columns = [key, 'coddistrit']
    point_in_polys = point_in_polys[columns]
    input_df.drop('coords', axis=1, inplace=True)  # No nos hace falta la columna coords
    point_in_polys.dropna(inplace=True)
    return point_in_polys  # No nos hace falta la columna coords


def get_shp_data() -> str:
    """
    Access to compressed file that defines districts and quarters of the city and stores shp file in SHP_DIR
    :return: Message OK or NOK to tell the result of operation
    """

    load_dotenv(os.path.join(os.getcwd(), 'config.env'))  # Cargamos as variables de 'entorno'
    SHP_DIR = os.getenv('SHP_DIR')

    try:  # We create the directory in case it does not exists
        os.mkdir('SHP_DIR')
    except FileExistsError:
        pass

    url = URL_SHP_DISTRICTS
    try:  # Access to web data
        resp = requests.get(url)

    except Exception as e:
        print(f"Excepción en el acceso a los datos: {e.args}")
        return 'NOK'

    else:  # Access OK
        if resp.status_code == 200:
            output_file = os.path.join(SHP_DIR, 'barrios.zip')  # Compressed file with data is returned
            with resp as r:
                with open(output_file, "wb") as f:
                    f.write(r.content)

            with ZipFile(output_file, 'r') as Zobject:  # Extraemos en el mismo directorio los ficheros del .zip
                Zobject.extractall(path=SHP_DIR)
            os.remove(output_file)
            return 'OK'
        else:
            return 'NOK'


def send_data_to_CB(df: pd.DataFrame):
    """
    This procedure receives a dataframe with data to be sent to Context Broker. It has to:
    - Convert dataframe into list of dictionaries as accepted by Context Broker
    - Get access permision to CB
    - Send converted data to CB
    :param df: Data to be sent
    :return:
    """

    # Conversion to list of dictionaries
    # ----------------------------------
    list_data = []  # List of dictionaries
    row_dict = dict()  # Dictionary related to each dataframe row

    columns_list = list(df.columns)  # Columns of dataframe
    columns_list = [x for x in columns_list if x != 'entityid' and x != 'entitytype']
    for i in range(len(df)):
        row_dict = dict()  # Dictionary related to each dataframe row
        row_dict['id'] = df.iloc[i]['entityid']
        row_dict['type'] = df.iloc[i]['entitytype']
        row_dict['sceneref'] = {'type': 'Text', 'value': 'N/A'}
        for feature in columns_list:
            feat_data = df.iloc[i][feature]   # Column data
            row_dict[feature] = {'type': dict_class_cb_data[feature], 'value': feat_data}
        list_data.append(row_dict)

    # Sending to CB
    # -------------
    br = Broker.create()
    br.push(entities=list_data)


if __name__ == '__main__':
    #get_shp_data()
    #df = pd.read_csv('e:/prueba.csv', sep= ';')
    #send_data_to_CB(df)
    load_dotenv(os.path.join(os.getcwd(), 'config.env'))  # Loads enviromments variables

    pass
