import datetime
import json
import logging
import os
from statistics import mode
from typing import Dict, List
import pandas as pd
import shapely
from dotenv import load_dotenv

from rutinas_auxiliares import send_data_to_CB, calculo_distritos
from shapely.geometry import shape, MultiLineString
import ast

base_dir = os.getcwd()
files_dir = os.path.join(base_dir, 'ficheros_datos')
file_rutas = 'frecuencia_paso_EMT.csv'
file_stops = 'stops.txt'
file_stop_times = 'stop_times.txt'
file_stop_districts = 'listado_paradas_distritos.csv'
file_frecuencia_paso = 'frecuencia_paso_EMT.csv'
output_file = 'digitaltwin_emt_lastdata.csv'

entitytype = 'RouteSchedule'

def calculate_main_district(lista: List) -> str:
    """
    Calcula el valor más repetido (moda) de una lista en modo string
    :param lista: Lista de entrada
    :return: Moda de la lista en string
    """
    return str(mode(lista))


def get_geometry_format(lista_puntos: List) -> str:

    multiline = MultiLineString(lista_puntos)

    return json.loads(shapely.to_geojson(multiline))

def correccion_de_quotes(fichero: os.path) -> pd.DataFrame:
    # Sustituye los caracteres ' por " en el campo 'distrito' del fichero de entrada y lo almacena de nuevo
    df = pd.read_csv(fichero)
    df['zonelist'] = df['zonelist'].map(lambda x: x.replace("'", '"'))
    df.to_csv(fichero, index=0)
    df = pd.read_csv(fichero)
    os.remove(fichero)
    return df


def calculo_paradas_linea() -> pd.DataFrame:
    """
    Partiendo del fichero frecuencia_paso_EMT.csv, que proporciona muchos datos de planificación del servicio de
    autobuses urbanos de Valencia, esta rutina calcula el número de paradas de los trayectos de ida y de vuelta
    para cada línea de la EMT
    :return:
    """
    # Leemos los datos de planificación
    input_file = os.path.join(files_dir, file_frecuencia_paso)
    df = pd.read_csv(input_file, sep=',')

    # Agrupamos el Dataframe por el código de trayecto. Cada línea tiene generalmente 6 tipos de trayectos distintos,
    # correspondientes a ida/vuelta y tipo de servicio (laborable, sábado y festivo). No obstante, para cada línea
    # el número de paradas sólo depende de si el trayecto es de ida o de vuelta

    list_trips = df['trip_id'].unique()  # Lista de los distintos trayectos (trips)
    df_grp = df.groupby('trip_id')  # Agrupación por trayecto

    # Ahora formamos dos DataFrames auxiliares, uno para viajes de ida y otro de vuelta. Cada uno contendrá tres
    # columnas: linea (código de la línea), nombre y paradas_ida o paradas_vuelta, dependiendo del DataFrame
    df_num_paradas_ida = pd.DataFrame()
    df_num_paradas_vuelta = pd.DataFrame()

    for trip in list_trips:  # Tratamos uno a uno cada código de trayecto
        datos_linea = df_grp.get_group(trip).iloc[0]  # Basta con considerar la primera fila del trayecto
        if datos_linea['Servicio'] == 'LAB':  # Puesto que el tipo de día es irrelevante, sólo tomamos los laborables
            row = pd.DataFrame()  # Dataframe auxiliar, de sólo una fila
            row['entityid'] = [str(datos_linea['ROUTE_ID'])]
            row['name'] = [datos_linea['SHORT']]

            if trip[-1] == 'I':  # Trayecto de ida
                row['forwardstops'] = [datos_linea['num_paradas']]
                row['forwardstops'] = row['forwardstops'].astype(str)
                df_num_paradas_ida = pd.concat([df_num_paradas_ida, row])  # Añadimos nueva línea
            else:
                row['returnstops'] = [datos_linea['num_paradas']]
                row['returnstops'] = row['returnstops'].astype(str)
                df_num_paradas_vuelta = pd.concat([df_num_paradas_vuelta, row])  # Añadimos nueva línea

    # Por último, fundimos ambos Dataframes en uno sólo que agrupa tanto trayectos de ida como de vuelta
    df_num_paradas = pd.merge(df_num_paradas_ida, df_num_paradas_vuelta, how="left", on=["entityid", "name"])
    return df_num_paradas


def generate_dict_paradas_distrito() -> Dict:
    # Returns a dictionary that gives the city district of every bus stop

    paradas = pd.read_csv(os.path.join(files_dir, file_stops), sep=',')  # Lectura de datos de las paradas
    columns = ['stop_id', 'stop_lat', 'stop_lon']
    paradas = paradas[columns]  # Seleccionamos sólo los campos relevantes

    df_distritos = calculo_distritos(paradas, 'stop_id', 'stop_lat', 'stop_lon')
    dict_paradas_distrito = dict(zip(df_distritos['stop_id'].to_list(), df_distritos['coddistrit'].to_list()))

    return dict_paradas_distrito


def generate_dict_paradas_ubicacion() -> Dict:
    """
    Genera un diccionario que tiene como claves los códigos de las paradas de autobús y como valores, las coordenadas
    GPS de sus ubicacciones
    :return: Ese diccionario
    """
    df_stops = pd.read_csv(os.path.join(files_dir, file_stops))
    list_coordenadas = [[df_stops.iloc[i]['stop_lon'], df_stops.iloc[i]['stop_lat']] for i in range(len(df_stops))]
    dict_stops_loc = dict(zip(df_stops['stop_id'].to_list(), list_coordenadas))
    return dict_stops_loc


def generate_dict_paradas_trayecto() -> Dict:
    """
    Genera un diccionario cuyas claves son los códigos de trayecto (trip) de autobuses y sus valores, una lista con
    los códigos de las paradas del trayecto
    :return: Ese diccionario
    """
    df_paradas_trip = pd.read_csv(os.path.join(files_dir, file_stop_times))  # Leemos el fichero correspondiente

    lista_trips = df_paradas_trip['trip_id'].unique()  # Listamos el código de los diferentes trips
    df_paradas_trips_group = df_paradas_trip.groupby('trip_id')

    dict_paradas_trips = {}  # El diccionario que queremos
    for trip in lista_trips:
        lista_stops = df_paradas_trips_group.get_group(trip)['stop_id'].to_list()
        dict_paradas_trips[trip] = lista_stops
    return dict_paradas_trips


def generate_dict_trip_ruta_servicio(dict_paradas_trips: dict) -> Dict:
    """
    Ampliación del diccionario dict_paradas_trips. En éste cada clave (el código de trayecto o trip) se asocia a
    un diccionario que nos da la ruta, su nombre, el tipo de día y las paradas del trip
    :param dict_paradas_trips: El diccionario que usamos como base para ampliarlo
    :return: Diccionario ampliado
    """
    df_trips_rutas = pd.read_csv(os.path.join(files_dir, file_rutas))

    lista_viajes = df_trips_rutas['trip_id'].unique()
    df2_group = df_trips_rutas.groupby('trip_id')
    dict_viaje_ruta_servicio = dict()
    for viaje in lista_viajes:
        item = df2_group.get_group(viaje).iloc[0]
        dict_viaje_ruta_servicio[viaje] = {'ruta': item['ROUTE_ID'], 'nombre': item['SHORT'],
                                           'tipodia': item['Servicio'],
                                           'paradas': dict_paradas_trips[viaje]}
    return dict_viaje_ruta_servicio


def calcular_coordenadas_lineas(dict_viaje_ruta_servicio: Dict, dict_stops_loc: Dict) -> pd.DataFrame:
    """
    Partiendo de dict_viaje_ruta_servicio y dict_stops_loc se compone un dataframe que contiene el nombre de la línea
    de autobus, su código, el tipo de día y la lista de las coordenadas del trayecto
    :param dict_viaje_ruta_servicio:
    :param dict_stops_loc:
    :return: Dataframe descrito
    """
    df_coordenadas_lineas = pd.DataFrame()
    for key in dict_viaje_ruta_servicio.keys():
        row = pd.DataFrame()
        entityid = dict_viaje_ruta_servicio[key]['ruta']
        row['entityid'] = [entityid]
        row['name'] = [dict_viaje_ruta_servicio[key]['nombre']]
        row['tipodia'] = [dict_viaje_ruta_servicio[key]['tipodia']]
        row['zonelist'] = ['']
        row['recorrido'] = [[dict_stops_loc[i] for i in dict_viaje_ruta_servicio[key]['paradas']]]
        df_coordenadas_lineas = pd.concat([df_coordenadas_lineas, row])  # Añadimos la fila al dataframe general
    return df_coordenadas_lineas


def procesar_coordenadas_lineas(df_group_aux: pd.DataFrame.groupby) -> pd.DataFrame:
    """
    A partir de la información completa sobre las líneas de autobús, agrupada por código de línea y tipo de día
     (recibida en df_group_aux), generamos un dataframe ya preparado para almacenarse en csv. Los datos de este
     dataframe se extraen exclusivamente de los registros de df_group_aux referidos a días laborables ('LAB'). Los
     datos de los trayectos de ida y vuelta se añaden como listas de una lista compuesta. Esto se procesará al cargar
     la base de datos PostgreSQL como un objeto MultiLineString de PostGis
    :param df_group_aux: Datos totales agrupados por código de línea y tipo de día
    :return: El dataframe descrito
    """
    timeinstant = datetime.datetime.now()
    timeinstant = timeinstant.replace(hour=0, minute=0, second=0, microsecond=0)  # Fecha de cálculo
    timeinstant = str(timeinstant.isoformat()) # CB needs str on ISO format
    df_coordenadas_multilinea = pd.DataFrame()  # Dataframe resultado

    for item, datos in df_group_aux:

        if item[1] == 'LAB':  # Sólo trabajamos los trayectos laborables, ya que coinciden con el resto de días
            fila = pd.DataFrame()  # Dataframe auxiliar de una sola fila que se irá añadiando a coordenadas_multilinea
            entityid = item[0]
            # fila['timeinstant'] = [pd.to_datetime(timeinstant)]
            fila['timeinstant'] = [timeinstant]
            fila['name'] = datos['name'].iloc[0]
            fila['entityid'] = [entityid]
            fila['entityid'] = fila['entityid'].astype((str))
            fila['sourceref'] = fila['entityid']
            fila['zonelist'] = [datos['zonelist'].iloc[0]]
            fila['entitytype'] = [entitytype]
            fila['fiwarepathservice'] = ['/digitaltwin']
            lista_auxiliar_recorridos = []
            for i in range(len(datos['recorrido'])):  # metemos el recorrido de ida y el de vuelta en una única lista
                lista_auxiliar_recorridos.append(datos['recorrido'].iloc[i])
            fila['location'] = [get_geometry_format(lista_auxiliar_recorridos)]
            fila['zone'] = str(datos['zone'].iloc[0])
            df_coordenadas_multilinea = pd.concat(
                [df_coordenadas_multilinea, fila])  # Añadimos la fila al dataframe general


    return df_coordenadas_multilinea


def generate_dict_distrits_line(dict_viaje_ruta_servicio: Dict, dict_parada_distrito:Dict) -> tuple[Dict, Dict]:
    """
    Partiendo de los datos de distrito de cada parada (en el fichero file_stop_districts) y de los datos de las paradas
    de cada trayecto (contenidos en dict_viaje_ruta_servicio), se compone un diccionario que:
    - Tiene como claves los códigos de las líneas de autobuses
    - Como valores, una lista con los distritos por los que discurre la línea
    También se añade otro diccionario que:
    - Tiene como claves los códigos de las líneas de autobuses
    - Como valores, el distrito en el que hay más paradas de la línea

    :param dict_viaje_ruta_servicio: Datos de las paradas de cada trayecto de línea
    :param dict_parada_distrito: Dictionary that links bus stops and their city district
    :return: Los citados diccionarios
    """

    dict_paradas_linea = {}  # Diccionario auxiliar que relacionará cada línea con sus paradas
    for key, value in dict_viaje_ruta_servicio.items():
        if value['tipodia'] == 'LAB' and key[-1] == 'I':  # Sólo tenemos en cuenta los viajes de ida
            dict_paradas_linea[value['ruta']] = value['paradas']

    # Y ahora componemos los diccionarios finales, que relaciona cada línea con los distritos por los que pasa y cada
    # línea con el distrito en que tiene más paradas
    dict_linea_distritos = {}
    dict_linea_distr_mayoritario = {}

    for key, value in dict_paradas_linea.items():
        full_district_list = [dict_parada_distrito.get(item, '0') for item in value]
        main_district = calculate_main_district(full_district_list)
        district_list_without_repetitions = list(set([dict_parada_distrito.get(item, '0') for item in value]))
        district_list_without_repetitions = [str(x) for x in district_list_without_repetitions if
                                             x != '0']  # Los valores '0' no nos valen
        dict_linea_distritos[key] = district_list_without_repetitions
        dict_linea_distr_mayoritario[key] = main_district  # Distrito con mayor múmero de paradas de la línea

    return dict_linea_distritos, dict_linea_distr_mayoritario


def etl_routeschedule_lastdata() -> pd.DataFrame:
    """
    Basándonos en los diversos ficheros oficiales de información sobre el servicio de autobuses urbanos de Valencia,
    se generará un fichero csv (digitaltwin_emt_lastdata.csv) con el que pueden rellenarse directamente las tablas
    dtwin_routeintensity_lastdata y dtwin_routeschedule_lastdata. Estas tablas dan datos estáticos de las líneas de
    autobús, tales como distritos por los que discurren los trayectos y datos de geolocalizaciónm de los mismos
    (objetos MultiLineString de PostGis)
    :return:
    """
    # Vamos a generar un diccionario que relacione cada parada con su ubicación GPS
    dict_stops_loc = generate_dict_paradas_ubicacion()

    # Ahora generaremos otro que nos dé la lista de paradas de cada trayecto (trip)
    dict_paradas_trips = generate_dict_paradas_trayecto()

    # Por último, compondremos un diccionario que relaciona cada trip con su línea de autobús, tipo de día y paradas
    dict_viaje_ruta_servicio = generate_dict_trip_ruta_servicio(dict_paradas_trips)

    dict_paradas_distrito = generate_dict_paradas_distrito()  # Here the relation stop -> city district

    # Para poder calcular los distritos por los que transcurren las diversas líneas generamos otro dicionario
    dict_distritos_linea, dict_line_main_district = generate_dict_distrits_line(dict_viaje_ruta_servicio,
                                                                                dict_paradas_distrito)

    # Ahora generamos un dataframe con los datos relevantes que luego procesaremos ligeramente para componer
    # el dataframe final que se almacenará an csv y tendrá una estructura similar a las tablas de digitaltwin
    df_coordenadas_lineas = calcular_coordenadas_lineas(dict_viaje_ruta_servicio, dict_stops_loc)
    df_coordenadas_lineas['zonelist'] = df_coordenadas_lineas['entityid'].map(lambda x: dict_distritos_linea[x])
    df_coordenadas_lineas['zone'] = df_coordenadas_lineas['entityid'].map(lambda x: dict_line_main_district[x])

    # Ya tenemos el dataframe con todos los datos relevantes. Ahora hay que reprocesarlo para adaptarlo a la base
    # de datos, que no trabaja con trayectos sino con líneas. Hay que agrupar por entityid y tipodia

    df_group_aux = df_coordenadas_lineas.groupby(['entityid', 'tipodia'])
    df_routeintensity_lastdata = procesar_coordenadas_lineas(df_group_aux)

    # Finally, we add values for columns 'forwardstops' and 'returnstops'
    df_stops = calculo_paradas_linea()
    df_routeintensity_lastdata = pd.merge(df_routeintensity_lastdata, df_stops, how="left", on=["entityid", "name"])
    #df_routeintensity_lastdata['zonelist'] = df_routeintensity_lastdata['zonelist'].map(lambda x: str(x))
    # Ya sólo queda almacenar el resultado en un csv (necesario temporalmente para corregir problemas de formato
    # fichero_salida = os.path.join(files_dir, output_file)
    # df_routeintensity_lastdata.to_csv(fichero_salida, index=False, quotechar='"')
    #
    # # Una pequeña corrección para sustituir los quotes ' por " en las listas de distritos
    # df_routeintensity_lastdata = correccion_de_quotes(fichero_salida)  # Dataframe to be sent to Context Broker
    return df_routeintensity_lastdata


if __name__ == '__main__':

    load_dotenv(os.path.join(os.getcwd(), 'config.env'))  # Loads enviromments variables

    logging.basicConfig(
        level=os.getenv('ETL_LOG_LEVEL', 'DEBUG'),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()])

    logging.info('Start of execution ETL_routeschedule_lastdata')

    df = etl_routeschedule_lastdata()
    if df.empty:
        logging.info('No data obtained from web source')
    else:
        send_data_to_CB(df)  # Send data to Context Broker

    logging.info('End of execution')

