import pandas as pd
import datetime
import requests
import os
import logging
from zipfile import ZipFile
from dotenv import load_dotenv

URL_TRANSPORTES_API = 'https://nap.transportes.gob.es/api/Fichero/download/'
FILE_ID = 1166
file_rutas = 'routes.txt'
file_trips = 'trips.txt'
file_frequencies = 'frequencies.txt'
file_stop_times = 'stop_times.txt'


def adquirir_fichero_GTFS_zip(url: str, api_key: str, file_id: int, files_dir: str) -> str:
    """
    Este procedimiento solicita a la web oficial de transportes el ficheri GTFS de información sobre las líneas
    de autobuses urbanos de Valencia. El resultado es un fichero .zip que contiene varios ficheros de texto con
    la información de planificación de trayectos (entre otras). Este fichero se almacenará en el directorio
    files_dir
    :param url: URL de la web oficial de transportes (sección descarga de ficheros)
    :param api_key: Clave para acceder a la API de solicitud de ficheros
    :param file_id: Identidad del fichero solicitado
    :return: OK si no hay problemas, un string informativo en caso contrario
    """
    # Lo primero, creamos el directorio de almacenamiento de ficheros si aún no lo está
    try:
        os.mkdir(files_dir)
    except FileExistsError:
        pass

    # Ahora hacemos la petición
    url_req = url + str(file_id) + '?apiKey=' + api_key
    headers = {'accept': 'application/octet-stream', 'ApiKey': api_key}

    resp = requests.get(url_req, headers=headers)
    if resp.status_code == 200:
        output_file = os.path.join(FILES_DIR, 'GTFS.zip')  # La petición ha sido exitosa
        with resp as r:
            with open(output_file, "wb") as f:
                f.write(r.content)

        with ZipFile(output_file, 'r') as Zobject:  # Extraemos en el mismo directorio los ficheros del .zip
            Zobject.extractall(FILES_DIR, members=['frequencies.txt', 'stop_times.txt', 'stops.txt',
                                                   'routes.txt', 'trips.txt'])
        os.remove(os.path.join(FILES_DIR, 'GTFS.zip')) # The original zip file is no longer needed
        return 'OK'

    else:  # Algo no ha ido bien
        return f'Error: {resp.text}'


def corregir_hora(hora: str) -> str:
    """
    Este procedimiento hace un par de retoques a la información de horas contenida en frequencies.txt:
    - Ajusta a dos dígitos el valor del campo hora
    - A los valores de hora superiores a 23 les resta 24 para ajustarlos a la hora real
    :param hora: Información horaria a ajustar
    :return: Hora ya ajustada
    """
    # Primero, se asegura que la hora figura con dos números
    if hora[1] == ':':
        hora = '0' + hora

    # Y ahora se corrigen los valores de hora superiores a 23
    if int(hora[:2]) >= 24:
        substr1 = str(int(hora[:2]) - 24)
        substr2 = hora[2:]
        return substr1 + substr2

    else:
        return hora


def resta_horas(t_end: datetime.time, t_start: datetime.time) -> int:
    """
    Como los datos de clase datetime.time no admiten la resta directa, este procedimiento devuelve la diferencia
    en segundos de dos datos de esta clase: t_end - t_start
    :param t_end: time mayor
    :param t_start: time menor
    :return:
    """
    hora_end, minuto_end, segundo_end = t_end.hour, t_end.minute, t_end.second
    hora_start, minuto_start, segundo_start = t_start.hour, t_start.minute, t_start.second

    if segundo_end < segundo_start:
        segundo_end += 60
        minuto_end -= 1
    resultado = segundo_end - segundo_start

    if minuto_end < minuto_start:
        minuto_end += 60
        hora_end -= 1

    resultado += 60 * (minuto_end - minuto_start)

    if hora_end < hora_start:
        hora_end += 24

    resultado += 3600 * (hora_end - hora_start)
    return resultado


def generar_fichero_Excel():
    """
    Partiendo de los ficheros GTFS almacenados en el directorio pertinente, este procedimiento genera el fichero
    Excel auxiliar (y otro csv) que usarán las rutinas de relleno de la tabla PostgreSQL emt_schedule, usada para
    componer algunos de los paneles de Urbo. La información suministrada hace referencia a la planificación de viajes
    de la empresa municipal de autobuses EMT de Valencia.
    :return:
    """
    # En primer lugar, generamos un dataframe con cada uno de los cuatro ficheros relevantes
    try:
        rutas = pd.read_csv(os.path.join(FILES_DIR, file_rutas))
        trips = pd.read_csv(os.path.join(FILES_DIR, file_trips))
        frequencies = pd.read_csv(os.path.join(FILES_DIR, file_frequencies))
        stop_times = pd.read_csv(os.path.join(FILES_DIR, file_stop_times))

    except Exception as e:
        logging.error(f'Se ha producido un fallo en la carga de algún fichero de datos GTFS \n {e.args}')
        return

    # Creamos el Dataframe objetivo, que se pasará a csv y Excel
    columns = ['trip_id', 'start_time', 'end_time', 'headway_secs', 'ROUTE_ID', 'SHORT', 'Servicio', 'num_paradas',
               'trayectos']
    frecuencia_paso_EMT = pd.DataFrame(columns=columns)

    # Hacemos un diccionario que relacione el nombre de route_id con el corto (short)
    lista_route_id = rutas['route_id'].to_list()
    lista_short_names = rutas['route_short_name'].to_list()
    dict_routeid_to_short = dict(zip(lista_route_id, lista_short_names))

    # Otro diccionario para relacionar líneas con trips y tipos de día
    lista_lineas = [[trips.iloc[i]['route_id'], trips.iloc[i]['service_id']] for i in range(len(trips))]
    lista_trips = trips['trip_id'].to_list()
    dict_trips_to_route_service = dict(zip(lista_trips, lista_lineas))

    # Y otro que relacione el trip_id con el número de paradas del trayecto
    paradas = stop_times[['trip_id', 'stop_id']]
    contador_paradas = paradas.groupby('trip_id')['stop_id'].count().reset_index()
    lista_trips = contador_paradas['trip_id']
    lista_paradas = contador_paradas['stop_id']
    dict_trips_paradas = dict(zip(lista_trips, lista_paradas))

    # Apoyándonos en los diccionarios creados, vamos rellenando las filas de frecuencia_paso_EMT
    for i in range(len(frequencies)):
        trip_id = frequencies.iloc[i]['trip_id']
        start_time = frequencies.iloc[i]['start_time']
        end_time = frequencies.iloc[i]['end_time']
        headway_secs = frequencies.iloc[i]['headway_secs']
        route_serv = dict_trips_to_route_service[trip_id]
        route_id = route_serv[0]
        short_name = dict_routeid_to_short.get(route_id, 'Error')
        servicio = route_serv[1]
        num_paradas = dict_trips_paradas.get(trip_id, 999)
        trayectos = 0
        new_row = {'trip_id': trip_id, 'start_time': start_time, 'end_time': end_time, 'headway_secs': headway_secs,
                   'ROUTE_ID': route_id, 'SHORT': short_name, 'Servicio': servicio, 'num_paradas': num_paradas,
                   'trayectos': trayectos}
        frecuencia_paso_EMT.loc[len(frecuencia_paso_EMT)] = new_row

    # Retocamos el formato de los campos con información horaria no adecuada
    frecuencia_paso_EMT['start_time'] = frecuencia_paso_EMT['start_time'].map(lambda x: corregir_hora(x))
    frecuencia_paso_EMT['start_time'] = pd.to_datetime(frecuencia_paso_EMT['start_time']).dt.time
    frecuencia_paso_EMT['end_time'] = frecuencia_paso_EMT['end_time'].map(lambda x: corregir_hora(x))
    frecuencia_paso_EMT['end_time'] = pd.to_datetime(frecuencia_paso_EMT['end_time']).dt.time

    # Por último, rellenamos la única columna restante: trayectos. Los calcularemos como la diferencia entre
    # el campo end_time y start_time dividido por headway_secs (intervalo entre autobuses)
    for i in range(len(frecuencia_paso_EMT)):
        frecuencia_paso_EMT.at[i, 'trayectos'] = round(
            resta_horas(frecuencia_paso_EMT.iloc[i]['end_time'], frecuencia_paso_EMT.iloc[i]['start_time']) /
            frecuencia_paso_EMT.iloc[i]['headway_secs'])

    # Ya están efectuados todos los cálculos, por lo que pasamos a almacenar los resultados en un fichero Excel
    # y otro csv
    try:
        output_excel_file = 'frecuencia_paso_EMT.xlsx'
        frecuencia_paso_EMT.to_excel(os.path.join(FILES_DIR, output_excel_file), sheet_name='FREQS')

        output_csv_file = 'frecuencia_paso_EMT.csv'
        frecuencia_paso_EMT.to_csv(os.path.join(FILES_DIR, output_csv_file), index=False)

    except Exception as e:
        logging.error(f'Se ha producido un fallo al pasar de Dataframe a fichero Excel o csv \n {e.args}')
        return

    else:
        logging.info(f'{datetime.datetime.now()} Programa finalizado correctamente')


if __name__ == '__main__':
    """
    Este programa realiza dos funciones principales:
    - De la web estatal de transportes recoge los datos de planificación (GTFS) del servicio de autobuses urbanos de Valencia
      y los almacena en un directorio de trabajo
    - Procesando los datos de cuatro de esos ficheros, compone un fichero Excel (y otro csv) que servirá de fuente para
      el relleno de la tabla PostgreSQL emt_schedule, usada para representar algunos paneles de Urbo
    
    Los nombres de los ficheros de salida son:
        frecuencia_paso_EMT.xlsx
        frecuencia_paso_EMT.csv
    """
    load_dotenv(os.path.join(os.getcwd(), 'config.env'))  # Cargamos as variables de 'entorno'

    API_KEY = os.getenv('API_KEY')  # Clave API para acceder a la web de información de transportes
    BASE_DIR = os.getenv('BASE_DIR')
    FILES_DIR = os.getenv('FILES_DIR') # Carpeta donde se guardarán los resultados del programa

    logging.basicConfig(level=logging.DEBUG)
    logging.info(f'{datetime.datetime.now()} Comienza la ejecución del programa')

    resul = adquirir_fichero_GTFS_zip(URL_TRANSPORTES_API, API_KEY, FILE_ID, FILES_DIR)  # Solicitamos los ficheros GTFS

    if resul == 'OK':
        logging.info(f'{datetime.datetime.now()} Fichero GTFS bajado correctamente')
        generar_fichero_Excel()  # En principio, se almacenará en FILES_DIR
    else:
        logging.error(f'Se ha producido un fallo en la carga del fichero GTFS\n {resul}')

    logging.info(f'{datetime.datetime.now()} Finaliza la ejecución de generación_Excel_EMT.py')
