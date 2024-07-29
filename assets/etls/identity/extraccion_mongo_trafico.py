import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta
from datetime import datetime
import json
import sys

def load_config():
    """
    Carga el archivo de configuración en formato JSON.
    
    Returns:
    dict: Un diccionario con la configuración cargada.
    """
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def trafico_roads_mongo_data_loader(execution_date, config, estacionalidad_config):
    """
    Carga los datos de tráfico desde una base de datos MongoDB.
    
    Parameters:
    execution_date (datetime): Fecha de ejecución para filtrar los datos.
    config (dict): Configuración de la base de datos MongoDB.
    estacionalidad_config (dict): Configuración de estacionalidad.
    
    Returns:
    DataFrame: Un DataFrame con los datos cargados de MongoDB.
    """
    # Conexión a la base de datos MongoDB
    client = MongoClient(f"mongodb://{config['source_db']['user']}:{config['source_db']['password']}@{config['source_db']['host']}:{config['source_db']['port']}/{config['source_db']['dbname']}")
    db = client[config['source_db']['dbname']]
    collection = db[config['source_db']['collection_name']]

    # Definir el rango de fechas
    fecha_fin = execution_date.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha_inicio = fecha_fin - relativedelta(months=12)

    print(f"Fecha de inicio = {fecha_inicio} y fecha final = {fecha_fin}")

    # Definir el pipeline de agregación de MongoDB
    aggregate = [
        {
            "$match": {
                "$and": [
                    {"estadoForzado": {'$in': [1, 2, 6, 7, "1", "2", "6", "7"]}},
                    {"recvTime": {"$gte": fecha_inicio, "$lte": fecha_fin}},
                    {"fechaHora": {"$type": "date"}},
                ]
            }
        },
        {
            "$project": {
                "entityId": 1,
                "diasemana": {
                    "$switch": {
                        "branches": [
                            {"case": {"$eq": [{"$dayOfWeek": "$fechaHora"}, 1]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$fechaHora"}, 2]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$fechaHora"}, 3]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$fechaHora"}, 4]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$fechaHora"}, 5]}, "then": "Viernes"},
                            {"case": {"$eq": [{"$dayOfWeek": "$fechaHora"}, 6]}, "then": "Sábado"},
                            {"case": {"$eq": [{"$dayOfWeek": "$fechaHora"}, 7]}, "then": "Domingo"}
                        ],
                        "default": "No definido"
                    }
                },
                "anyo": {"$year": "$fechaHora"},
                "mes":  {"$month": "$fechaHora"},
                "dia":  {"$dayOfMonth": "$fechaHora"},
                "hora": {"$hour": "$fechaHora"},
                "minuto": {
                    "$subtract": [
                        {"$minute": "$fechaHora"},
                        {"$mod": [{"$minute": "$fechaHora"}, 10]}
                    ]
                }
            }
        },
        {
            "$addFields": {
                "estacionalidad": {
                    "$switch": {
                        "branches": [
                            {"case": {"$in": ["$mes", estacionalidad_config["Alta"]]}, "then": "Alta"},
                            {"case": {"$in": ["$mes", estacionalidad_config["Baja"]]}, "then": "Baja"}
                        ],
                        "default": "No definido"
                    }
                }
            }
        },
        {
            "$group": {
                "_id": { 
                    "entityId": "$entityId",
                    "diasemana": "$diasemana",
                    "anyo": "$anyo",
                    "mes": "$mes",
                    "dia": "$dia",
                    "hora": "$hora",
                    "minuto": "$minuto",
                    "estacionalidad": "$estacionalidad"
                }
            }   
        },
        {
            "$group": {
                "_id": { 
                    "entityId": "$_id.entityId",
                    "diasemana": "$_id.diasemana",
                    "hora": "$_id.hora",
                    "minuto": "$_id.minuto",
                    "estacionalidad": "$_id.estacionalidad"
                },
                "medidas": {
                    "$sum": 1
                }
            }   
        },
        {
            "$project": {
                "entityId": "$_id.entityId",
                "diasemana": "$_id.diasemana",
                "hora": "$_id.hora",
                "minuto": "$_id.minuto",
                "medidas": 1,
                "estacionalidad": "$_id.estacionalidad",
            }
        }
    ]
    
    cursor = collection.aggregate(aggregate)
    df_mongo = pd.DataFrame(list(cursor))
    
    return df_mongo

def trafico_roads_calculo_congestion(df_mongo, execution_date, estacionalidad_config):
    """
    Calcula la congestión del tráfico a partir de los datos cargados de MongoDB.
    
    Parameters:
    df_mongo (DataFrame): Datos cargados de MongoDB.
    execution_date (datetime): Fecha de ejecución.
    estacionalidad_config (dict): Configuración de estacionalidad.
    
    Returns:
    DataFrame: Un DataFrame con los datos de congestión calculados.
    """
    df_frecuencia = df_mongo.sort_values(by='medidas', ascending=False)

    data_to = execution_date.replace(hour=0, minute=0, second=0, microsecond=0)
    data_from = data_to - relativedelta(months=12)

    # Crear un rango de fechas y horas
    date_range = pd.date_range(data_from, data_to, freq='D')
    hours = list(range(24))
    decenas_minutos = list(range(0, 60, 10))

    # Generar un DataFrame completo con todas las combinaciones de día, hora y minutos
    date_range_full = pd.DataFrame([
        {'dia': dia, 'hora': hora, 'minuto': minuto}
        for dia in date_range
        for hora in hours
        for minuto in decenas_minutos
    ])

    # Asignar los nombres de los días de la semana
    day_names = {0: 'Laborable', 1: 'Laborable', 2: 'Laborable', 3: 'Laborable', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'}
    date_range_full['diasemana'] = date_range_full['dia'].dt.dayofweek.map(day_names)

    # Asignar la estacionalidad
    date_range_full['estacionalidad'] = date_range_full['dia'].dt.month.apply(
        lambda x: 'Alta' if x in estacionalidad_config['Alta'] else 'Baja'
    )

    # Agrupar por días de la semana, hora, minuto y estacionalidad
    date_range_grouped = date_range_full.groupby(['diasemana', 'hora', 'minuto', 'estacionalidad']).size().reset_index(name='medidas')

    # Fusionar los datos de frecuencia con el rango de fechas agrupado
    df_probabilidad = pd.merge(df_frecuencia, date_range_grouped, on=['diasemana', 'hora', 'minuto', 'estacionalidad'], how='left')
    df_probabilidad.loc[:, 'medidas_y'] = df_probabilidad['medidas_y'].fillna(0)

    # Calcular la congestión
    df_probabilidad['congestion'] = df_probabilidad.apply(
        lambda row: row['medidas_x'] / row['medidas_y'] if row['medidas_y'] != 0 else 0,
        axis=1
    )

    return df_probabilidad

def trafico_roads_preparacion_datos_congestion(df_probabilidad, execution_date):
    """
    Prepara el DataFrame final con los datos de congestión del tráfico.
    
    Parameters:
    df_probabilidad (DataFrame): Datos de congestión calculados.
    execution_date (datetime): Fecha de ejecución.
    
    Returns:
    DataFrame: Un DataFrame con los datos listos para exportar.
    """
    fecha = pd.to_datetime(execution_date)

    # Crear el DataFrame final con los datos necesarios
    final_df = pd.DataFrame({
        'timeinstant': fecha,
        'sourceref': df_probabilidad['entityId'],
        'sceneref': 'N/A',
        'trend': df_probabilidad['estacionalidad'],
        'daytype': df_probabilidad['diasemana'],
        'hour': df_probabilidad['hora'],
        'minute': df_probabilidad['minuto'],
        'congestion': df_probabilidad['congestion'],
        'entityId': df_probabilidad['entityId'],      
        'entitytype': 'TrafficCongestion',
        'recvtime': fecha,
        'fiwareservicepath': '/digitaltwin'
    })
    
    return final_df

def trafico_roads_table_exporter(final_df, config):
    """
    Exporta los datos de congestión a una base de datos PostgreSQL.
    
    Parameters:
    final_df (DataFrame): Datos finales para exportar.
    config (dict): Configuración de la base de datos de destino.
    """
    db_config = config['destination_db']

    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    # Exportar los datos al esquema especificado en la base de datos
    final_df.to_sql(
        'dtwin_trafficcongestion',
        engine,
        schema=db_config['schema'],
        if_exists='append',
        index=False
    )

def main(execution_date_str):
    """
    Función principal para ejecutar la carga, transformación y exportación de datos.
    
    Parameters:
    execution_date_str (str): Fecha de ejecución en formato de string (DD/MM/YYYY).
    """
    execution_date = pd.to_datetime(execution_date_str, dayfirst=True)

    # Cargar configuraciones desde config.json
    config = load_config()
    trafico_roads_config = config['trafico_roads']
    estacionalidad_config = config['estacionalidad']
    trafico_roads_config['source_db']['collection_name'] = 'sth_/trafico_road'

    # Cargar datos desde MongoDB
    df_mongo = trafico_roads_mongo_data_loader(execution_date, trafico_roads_config, estacionalidad_config)
    print("Datos Cargados")

    # Transformar datos
    df_probabilidad = trafico_roads_calculo_congestion(df_mongo, execution_date, estacionalidad_config)
    

    # Preparar datos para exportar
    final_df = trafico_roads_preparacion_datos_congestion(df_probabilidad, execution_date)
    print("Datos Transformados")

    # Exportar datos a PostgreSQL
    trafico_roads_table_exporter(final_df, trafico_roads_config)
    print("Datos Exportados")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <execution_date>")
        sys.exit(1)
    
    execution_date_str = sys.argv[1]
    main(execution_date_str)
