import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import sys

# Suprimir advertencias de pandas y pymongo
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

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

# Bloque 1: imd_trafico_data_loader
def imd_trafico_data_loader(execution_date, config, estacionalidad_config, entity_patterns):
    """
    Carga los datos de tráfico desde una base de datos MongoDB.
    
    Parameters:
    execution_date (datetime): Fecha de ejecución para filtrar los datos.
    config (dict): Configuración de la base de datos MongoDB.
    estacionalidad_config (dict): Configuración de estacionalidad.
    entity_patterns (list): Lista de patrones de entidades a incluir.
    
    Returns:
    DataFrame: Un DataFrame con los datos cargados de MongoDB.
    """
    # Conexión a la base de datos MongoDB
    client = MongoClient(f"mongodb://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}")
    db = client[config['dbname']]
    collection = db[config['collection_name_traffic']]  
    
    # Definir el rango de fechas
    fecha_fin = execution_date.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha_inicio = fecha_fin - relativedelta(months=12)

    print(f"Fecha de inicio = {fecha_inicio} y fecha final = {fecha_fin}")
    
    # Crear patrón regex para filtrar entidades
    regex_pattern = "|".join(f"puntoMedida_{num}_tra" for num in entity_patterns)

    # Definir el pipeline de agregación de MongoDB
    aggregate = [
        {
            "$match": {
                "$and": [
                    {"intensity": {"$nin": ['0', '-1', 0, -1]}},
                    {"recvTime": {"$gte": fecha_inicio, "$lte": fecha_fin}},
                    {"dateObserved": {"$type": "date"}},
                    {"entityId": {"$regex": regex_pattern}},
                    {"$expr": {"$eq": [{"$substr": ["$entityId", 0, 12]}, "puntoMedida_"]}}
                ]
            }
        },
        {
            "$project": {
                "entityId": 1,
                "laneID": "$laneID",
                "name": "$laneID",
                "intensity": {"$toInt": "$intensity"},
                "hour": {"$hour": "$dateObserved"},
                "month": {"$month": "$dateObserved"},
                "dayOfWeek": {
                    "$switch": {
                        "branches": [
                            {"case": {"$eq": [{"$dayOfWeek": "$dateObserved"}, 1]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$dateObserved"}, 2]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$dateObserved"}, 3]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$dateObserved"}, 4]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$dateObserved"}, 5]}, "then": "Viernes"},
                            {"case": {"$eq": [{"$dayOfWeek": "$dateObserved"}, 6]}, "then": "Sábado"},
                            {"case": {"$eq": [{"$dayOfWeek": "$dateObserved"}, 7]}, "then": "Domingo"}
                        ],
                        "default": "No definido"
                    }
                }
            }
        },
        {
            "$addFields": {
                "estacionalidad": {
                    "$switch": {
                        "branches": [
                            {"case": {"$in": ["$month", estacionalidad_config["Alta"]]}, "then": "Alta"},
                            {"case": {"$in": ["$month", estacionalidad_config["Baja"]]}, "then": "Baja"}
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
                    "hour": "$hour",
                    "dayOfWeek": "$dayOfWeek",
                    "estacionalidad": "$estacionalidad"
                },
                "laneID": {"$first": "$laneID"},
                "name": {"$first": "$name"},
                "sumIntensity": {"$sum": "$intensity"},
                "avgIntensity": {"$avg": "$intensity"},
                "countIntensity": {"$sum": 1}
            }
        },
        {
            "$project": {
                "entityId": "$_id.entityId",
                "laneID": 1,
                "name": "$_id.name",
                "dayOfWeek": "$_id.dayOfWeek",
                "hour": "$_id.hour",
                "estacionalidad": "$_id.estacionalidad",
                "sumIntensity": 1,
                "avgIntensity": 1,
                "countIntensity": 1
            }
        }
    ]
    
    # Ejecutar la agregación y convertir los resultados a un DataFrame
    cursor = collection.aggregate(aggregate)
    data = pd.DataFrame(list(cursor))

    return data

# Bloque 2: imd_preparacion_df_trafico
def imd_preparacion_df_trafico(df, execution_date):
    """
    Prepara el DataFrame final con los datos de tráfico transformados.
    
    Parameters:
    df (DataFrame): Datos de tráfico transformados.
    execution_date (datetime): Fecha de ejecución.
    
    Returns:
    DataFrame: Un DataFrame con los datos finales listos para exportar.
    """
    fecha = pd.to_datetime(execution_date, dayfirst=True)

    # Verificar y ajustar los nombres de las columnas
    column_mapping = {
        'entityId': 'entityId',
        '_id.entityId': 'entityId',
        'estacionalidad': 'estacionalidad',
        '_id.estacionalidad': 'estacionalidad',
        'dayOfWeek': 'dayOfWeek',
        '_id.dayOfWeek': 'dayOfWeek',
        'hour': 'hour',
        '_id.hour': 'hour',
        'avgIntensity': 'avgIntensity'
    }

    # Renombrar columnas si es necesario
    df = df.rename(columns={old: new for old, new in column_mapping.items() if old in df.columns})

    # Crear el DataFrame final con los datos necesarios
    final_df = pd.DataFrame({
        'timeinstant': fecha,
        'sourceref': df['entityId'],
        'sceneref': 'N/A',
        'trend': df['estacionalidad'],
        'daytype': df['dayOfWeek'],
        'hour': df['hour'],
        'intensity': df['avgIntensity'],
        'entityid': df['entityId'],
        'entitytype': 'TrafficIntensity',
        'recvtime': fecha,
        'fiwareservicepath': '/digitaltwin'
    })

    return final_df

# Bloque 3: imd_trafico_table_exporter
def imd_trafico_table_exporter(final_df, db_config):
    """
    Exporta los datos de tráfico a una base de datos PostgreSQL.
    
    Parameters:
    final_df (DataFrame): Datos finales para exportar.
    db_config (dict): Configuración de la base de datos de destino.
    """
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    # Exportar los datos al esquema especificado en la base de datos
    final_df.to_sql(
        'dtwin_trafficintensity',
        engine,
        schema=db_config['schema'],
        if_exists='append',
        index=False
    )

# Función principal para ejecutar todos los bloques
def main(execution_date_str):
    """
    Función principal para ejecutar la carga, transformación y exportación de datos.
    
    Parameters:
    execution_date_str (str): Fecha de ejecución en formato de string (DD/MM/YYYY).
    """
    config = load_config('config.json')
    db_config = config['offstreetparking'] 
    estacionalidad_config = config['estacionalidad']
    entity_patterns = db_config['entity_patterns']
    execution_date = pd.to_datetime(execution_date_str, dayfirst=True)

    # Bloque 1: Cargar datos desde MongoDB
    df_mongo = imd_trafico_data_loader(execution_date, db_config['source_db'], estacionalidad_config, entity_patterns)
    print("Datos Cargados")

    # Bloque 2: Preparar DataFrame final
    final_df = imd_preparacion_df_trafico(df_mongo, execution_date)
    print("DataFrame Final Preparado")

    # Bloque 3: Exportar datos a PostgreSQL
    imd_trafico_table_exporter(final_df, db_config['destination_db'])
    print("Datos Exportados")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <execution_date>")
        sys.exit(1)
    
    execution_date_str = sys.argv[1]
    main(execution_date_str)