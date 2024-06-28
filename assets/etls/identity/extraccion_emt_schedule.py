import pandas as pd
from sqlalchemy import create_engine
import datetime
import json
import warnings
import sys

# Suprimir advertencias de pandas
warnings.filterwarnings('ignore', category=FutureWarning)

def load_config(filename):
    """
    Carga el archivo de configuración en formato JSON.
    
    Parameters:
    filename (str): La ruta al archivo de configuración.
    
    Returns:
    dict: Un diccionario con la configuración cargada.
    """
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

def frecuencia_paso_data_loader():
    """
    Carga los datos de frecuencia de paso desde un archivo CSV.
    
    Returns:
    DataFrame: Un DataFrame con los datos cargados del archivo CSV.
    """
    filepath = 'frecuencia_paso_EMT.csv'
    frecuencia_df = pd.read_csv(filepath)

    # Limpiar espacios extra en todas las columnas de tipo string
    frecuencia_df = frecuencia_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    return frecuencia_df

def dataframe_emt_schedule(df: pd.DataFrame, fecha) -> pd.DataFrame:
    """
    Prepara los datos de horarios de EMT para su procesamiento.
    
    Parameters:
    df (DataFrame): Datos de frecuencia de paso.
    fecha (str): Fecha en formato de string DD/MM/YYYY.
    
    Returns:
    DataFrame: Un DataFrame con los datos preparados y organizados.
    """
    dict_dias_servicio = {'LAB': 'Laborable', 'SAB': 'Sabado', 'FES': 'Domingo'}

    sched_emt_ida = pd.DataFrame()
    sched_emt_vuelta = pd.DataFrame()

    ahora = pd.to_datetime(fecha, dayfirst=True)
    lista_lineas = df['ROUTE_ID'].unique()

    for linea in lista_lineas:
        datos_linea = df[df['ROUTE_ID'] == linea]
        
        entityid = linea
        nombre_linea = datos_linea.iloc[0]['SHORT']

        lista_trips = datos_linea['trip_id'].unique()
        df_trip_ida = pd.DataFrame()
        df_trip_vuelta = pd.DataFrame()

        for trip in lista_trips:
            datos_trip = datos_linea[datos_linea['trip_id'] == trip]
            tipodia = datos_trip.iloc[0]['Servicio']
            if trip[-1] == 'I':  # Viajes de ida
                paradas_ida = datos_trip.iloc[0]['num_paradas']
                df_trip_ida['hora'] = [i for i in range(24)]
                df_trip_ida['entityid'] = entityid
                df_trip_ida['nombre_linea'] = nombre_linea
                df_trip_ida['timeinstant'] = ahora
                df_trip_ida['tipodia'] = dict_dias_servicio[tipodia]
                df_trip_ida['paradas_ida'] = paradas_ida
                num_viajes = calcular_viajes_por_hora(datos_trip)
                df_trip_ida['trayectos_ida'] = [num_viajes[hora] for hora in range(24)]
                sched_emt_ida = pd.concat([sched_emt_ida, df_trip_ida])

            else:  # Viajes de vuelta
                paradas_vuelta = datos_trip.iloc[0]['num_paradas']
                df_trip_vuelta['hora'] = [i for i in range(24)]
                df_trip_vuelta['entityid'] = entityid
                df_trip_vuelta['nombre_linea'] = nombre_linea
                df_trip_vuelta['timeinstant'] = ahora
                df_trip_vuelta['tipodia'] = dict_dias_servicio[tipodia]
                df_trip_vuelta['paradas_vuelta'] = paradas_vuelta
                num_viajes = calcular_viajes_por_hora(datos_trip)
                df_trip_vuelta['trayectos_vuelta'] = [num_viajes[hora] for hora in range(24)]
                sched_emt_vuelta = pd.concat([sched_emt_vuelta, df_trip_vuelta])

    # Unir datos de ida y vuelta
    sched_emt = pd.merge(sched_emt_ida, sched_emt_vuelta, how='outer')

    return sched_emt

def calcular_viajes_por_hora(datos: pd.DataFrame) -> dict:
    """
    Calcula el número de viajes por hora.
    
    Parameters:
    datos (DataFrame): Datos de viajes.
    
    Returns:
    dict: Un diccionario con el número de viajes por cada hora del día.
    """
    datos = datos.copy()
    datos['start_time'] = pd.to_datetime(datos['start_time'], format='%H:%M:%S').dt.time
    datos['end_time'] = pd.to_datetime(datos['end_time'], format='%H:%M:%S').dt.time
    datos['headway_secs'] = datos['headway_secs'].astype(int)

    horas = [i for i in range(24)]
    viajes = [0 for i in range(24)]
    num_viajes = dict(zip(horas, viajes))

    franja_horaria = 0
    first_trip_time = datos.iloc[franja_horaria]['start_time']
    num_viajes[first_trip_time.hour] += 1
    lista_start = datos['start_time'].to_list()
    lista_end = datos['end_time'].to_list()
    lista_interval = datos['headway_secs'].to_list()
    ultimo_viaje = datetime.datetime.combine(datetime.date.today(), first_trip_time)

    while franja_horaria < len(lista_start):
        comienzo_franja = datetime.datetime.combine(datetime.date.today(), lista_start[franja_horaria])
        final_franja = datetime.datetime.combine(datetime.date.today(), lista_end[franja_horaria])

        if comienzo_franja > final_franja:
            final_franja = final_franja + datetime.timedelta(days=1)

        next_trip = ultimo_viaje + datetime.timedelta(seconds=lista_interval[franja_horaria])
        num_viajes[next_trip.hour] += 1

        if next_trip >= final_franja:
            franja_horaria += 1
        ultimo_viaje = next_trip

    return num_viajes

def df_emt_schedule(data, fecha):
    """
    Genera el DataFrame final con los horarios de EMT.
    
    Parameters:
    data (DataFrame): Datos preparados de horarios.
    fecha (str): Fecha en formato de string DD/MM/YYYY.
    
    Returns:
    DataFrame: Un DataFrame con los datos finales listos para exportar.
    """
    # Agrupar y agregar datos
    data = data.groupby(['entityid', 'nombre_linea', 'hora', 'tipodia', 'timeinstant']).agg({
        'paradas_ida': 'mean',
        'paradas_vuelta': 'mean',
        'trayectos_ida': 'sum',
        'trayectos_vuelta': 'sum'
    }).reset_index()

    # Redondear y convertir tipos de datos
    data['paradas_ida'] = data['paradas_ida'].round().astype(int)
    data['paradas_vuelta'] = data['paradas_vuelta'].round().astype(int)
    data['trayectos_ida'] = data['trayectos_ida'].astype(int)
    data['trayectos_vuelta'] = data['trayectos_vuelta'].astype(int)

    # Crear un duplicado de datos para el día viernes
    viernes_data = data[data['tipodia'] == 'Laborable'].copy()
    viernes_data.loc[:, 'tipodia'] = 'Viernes'

    # Concatenar datos originales con los del día viernes
    data = pd.concat([data, viernes_data], ignore_index=True)

    fecha = pd.to_datetime(fecha, dayfirst=True)

    # Crear el DataFrame base con los datos preparados
    df_emt_schedule_base = pd.DataFrame({
        'timeinstant': fecha,
        'sourceref': data['entityid'],
        'sceneref': 'N/A',
        'daytype': data['tipodia'],
        'hour': data['hora'],
        'forwardtrips': pd.to_numeric(data['trayectos_ida'], errors='coerce').astype('Int64'),
        'returntrips': pd.to_numeric(data['trayectos_vuelta'], errors='coerce').astype('Int64'),
        'forwardstops': pd.to_numeric(data['paradas_ida'], errors='coerce').astype('Int64'),
        'returnstops': pd.to_numeric(data['paradas_vuelta'], errors='coerce').astype('Int64'),
        'entityid': data['entityid'],
        'entitytype': 'RouteSchedule',
        'recvtime': fecha,
        'fiwareservicepath': '/digitaltwin'
    })

    # Crear dos copias del DataFrame base para las tendencias "Alta" y "Baja"
    df_emt_schedule_alta = df_emt_schedule_base.copy()
    df_emt_schedule_alta['trend'] = 'Alta'

    df_emt_schedule_baja = df_emt_schedule_base.copy()
    df_emt_schedule_baja['trend'] = 'Baja'

    # Concatenar las dos tendencias en un solo DataFrame final
    df_emt_schedule = pd.concat([df_emt_schedule_alta, df_emt_schedule_baja], ignore_index=True)

    return df_emt_schedule

def emt_schedule_data_exporter(df: pd.DataFrame, db_config: dict):
    """
    Exporta los datos de horarios de EMT a una base de datos PostgreSQL.
    
    Parameters:
    df (DataFrame): Datos finales para exportar.
    db_config (dict): Configuración de la base de datos de destino.
    """
    destination_db = db_config['destination_db']

    # Crear conexión al motor de la base de datos de destino
    engine = create_engine(f"postgresql://{destination_db['user']}:{destination_db['password']}@{destination_db['host']}:{destination_db['port']}/{destination_db['database']}")

    # Exportar los datos al esquema especificado en la base de datos
    df.to_sql(
        'dtwin_routeschedule', 
        engine, 
        schema=destination_db['schema'], 
        if_exists='append', 
        index=False
    )

def main(fecha):
    """
    Función principal para ejecutar la carga, preparación, generación y exportación de datos.
    
    Parameters:
    fecha (str): Fecha en formato de string DD/MM/YYYY.
    """
    config = load_config('config.json')
    db_config = config['frecuencia_paso_data_loader']

    # Paso 1: Cargar datos
    data = frecuencia_paso_data_loader()
    print("Datos Cargados")

    # Paso 2: Preparar datos
    emt_schedule = dataframe_emt_schedule(data, fecha)

    # Paso 3: Generar DataFrame final
    df_schedule = df_emt_schedule(emt_schedule, fecha)
    print("Datos Transformados")

    # Paso 4: Exportar datos a PostgreSQL
    emt_schedule_data_exporter(df_schedule, db_config)
    print("Datos Exportados")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python frecuencia_paso.py <fecha>")
        sys.exit(1)
    
    fecha = sys.argv[1]
    main(fecha)
