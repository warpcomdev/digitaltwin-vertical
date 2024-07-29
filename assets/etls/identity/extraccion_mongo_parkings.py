import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import json
import sys

# Cargar configuraciones desde config.json
with open('config.json') as config_file:
    config = json.load(config_file)
    mongo_config = config['offstreetparking']['source_db']
    postgres_config = config['offstreetparking']['destination_db']
    estacionalidad_config = config['estacionalidad']

# Bloque 1: Funciones de carga de datos desde MongoDB
def mongo_data_loader(collection_name, execution_date, config, estacionalidad_config):
    """
    Carga los datos de aparcamiento desde una base de datos MongoDB.
    
    Parameters:
    collection_name (str): Nombre de la colección de MongoDB.
    execution_date (datetime): Fecha de ejecución para filtrar los datos.
    config (dict): Configuración de la base de datos MongoDB.
    estacionalidad_config (dict): Configuración de estacionalidad.
    
    Returns:
    DataFrame: Un DataFrame con los datos cargados de MongoDB.
    """
    client = MongoClient(f"mongodb://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}")
    db = client[config['dbname']]
    collection = db[collection_name]
    
    # Definir el rango de fechas
    fecha_fin = execution_date.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha_inicio = fecha_fin - relativedelta(months=12)

    print(f"Fecha de inicio = {fecha_inicio} y fecha final = {fecha_fin}")
    
    # Definir el pipeline de agregación de MongoDB
    aggregate = [
        {
            "$match": {
                "recvTime": {"$gte": fecha_inicio, "$lte": fecha_fin},
                "TimeInstant": {"$type": "date"}
            }
        },
        {
            "$project": {
                "_id": 1,  # Mantener el _id original
                "entityId": 1,
                "entityType": 1,
                "availableSpotNumber": {"$toInt": "$availableSpotNumber"},
                "totalSpotNumber": {"$toInt": "$totalSpotNumber"},
                "availableSpotPercentage": 1,
                "idAparcamiento": 1,
                "TimeInstant": 1,  # Mantener el TimeInstant original para su uso
                "year": {"$year": "$TimeInstant"},
                "month": {"$month": "$TimeInstant"},
                "day": {"$dayOfMonth": "$TimeInstant"},
                "hour": {"$hour": "$TimeInstant"},
                "tipodia": {
                    "$switch": {
                        "branches": [
                            {"case": {"$eq": [{"$dayOfWeek": "$TimeInstant"}, 1]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$TimeInstant"}, 2]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$TimeInstant"}, 3]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$TimeInstant"}, 4]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$TimeInstant"}, 5]}, "then": "Laborable"},
                            {"case": {"$eq": [{"$dayOfWeek": "$TimeInstant"}, 6]}, "then": "Sábado"},
                            {"case": {"$eq": [{"$dayOfWeek": "$TimeInstant"}, 7]}, "then": "Domingo"}
                        ],
                        "default": "No definido"
                    }
                }
            }
        },
        {
            "$addFields": { # Estacionalidad 
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
                    "entityType": "$entityType",
                    "idAparcamiento": "$idAparcamiento",
                    "tipodia": "$tipodia",
                    "hour": "$hour",
                    "totalSpotNumber": "$totalSpotNumber",
                    "estacionalidad": "$estacionalidad"
                },
                "avgOcupacion": {
                    "$avg": {
                        "$divide": [
                            {"$subtract": ["$totalSpotNumber", "$availableSpotNumber"]},
                            "$totalSpotNumber"
                        ]
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "entityId": "$_id.entityId",
                "entityType": "$_id.entityType",
                "idAparcamiento": "$_id.idAparcamiento",
                "tipodia": "$_id.tipodia",
                "hour": "$_id.hour",
                "totalSpotNumber": "$_id.totalSpotNumber",
                "estacionalidad": "$_id.estacionalidad",
                "avgOcupacion": {
                    "$round": [
                        {"$multiply": ["$avgOcupacion", 100]},
                        2
                    ]
                }
            }
        }
    ]
    
    # Ejecutar la agregación y convertir los resultados a un DataFrame
    cursor = collection.aggregate(aggregate)
    data = pd.DataFrame(list(cursor))
    
    return data

# Bloque 2: Funciones de transformación de datos
def transform_parking_data(df, execution_date):
    """
    Transforma los datos de aparcamiento cargados desde MongoDB.
    
    Parameters:
    df (DataFrame): Datos de aparcamiento cargados.
    execution_date (datetime): Fecha de ejecución.
    
    Returns:
    DataFrame: Un DataFrame con los datos transformados.
    """
    fecha = pd.to_datetime(execution_date)

    # Seleccionar solo los campos necesarios
    final_df = pd.DataFrame({
        'entityid': df['entityId'],
        'timeinstant': fecha,          
        'capacidad': df['totalSpotNumber'],
        'hora': df['hour'],
        'tipodia': df['tipodia'],
        'ocupacion': df["avgOcupacion"],
        'estacionalidad': df['estacionalidad'],
    })
    
    return final_df

# Bloque 3: Preparación de datos para el DataFrame final
def tranformacion_datos(final_df):
    """
    Realiza la transformación final de los datos para su exportación.
    
    Parameters:
    final_df (DataFrame): Datos transformados de aparcamiento.
    
    Returns:
    DataFrame: Un DataFrame con los datos listos para exportar.
    """
    # Asegurar tipos de datos y crear campo ocupacion_absoluta
    final_df['timeinstant'] = pd.to_datetime(final_df['timeinstant'], utc=True)
    final_df['capacidad'] = final_df['capacidad'].astype(int)
    final_df['hora'] = final_df['hora'].astype(int)
    final_df['ocupacion'] = final_df['ocupacion'].astype(float)
    final_df['ocupacion_absoluta'] = (final_df['capacidad'] * final_df['ocupacion']) / 100
    
    # Copiar los datos de 'Laborable' y cambiar el valor de 'tipodia' a 'Viernes'
    viernes_data = final_df[final_df['tipodia'] == 'Laborable'].copy()
    viernes_data['tipodia'] = 'Viernes'

    # Concatenar los datos de 'Viernes' con el DataFrame original
    final_df = pd.concat([final_df, viernes_data], ignore_index=True)

    # Crear el DataFrame final con los datos necesarios
    final_df = pd.DataFrame({
        'timeinstant': final_df['timeinstant'],
        'sourceref': final_df['entityid'],
        'sceneref': 'N/A',
        'trend': final_df['estacionalidad'],
        'daytype': final_df['tipodia'],
        'hour': final_df['hora'],
        'capacity': final_df['capacidad'],
        'occupationpercent': final_df['ocupacion'],
        'occupation': final_df['ocupacion_absoluta'],
        'entityid': final_df['entityid'],        
        'entitytype': 'OffStreetParking',
        'recvtime': final_df['timeinstant'],
        'fiwareservicepath': '/digitaltwin'
    })

    return final_df

# Bloque 4: Función de exportación de datos a PostgreSQL
def data_exporter(final_df, config):
    """
    Exporta los datos de aparcamiento a una base de datos PostgreSQL.
    
    Parameters:
    final_df (DataFrame): Datos finales para exportar.
    config (dict): Configuración de la base de datos de destino.
    """
    engine = create_engine(f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}")
    
    # Exportar los datos al esquema especificado en la base de datos
    final_df.to_sql(
        'dtwin_offstreetparking',
        engine,
        schema=config['schema'],
        if_exists='append',
        index=False
    )

# Función principal
def main(execution_date_str):
    """
    Función principal para ejecutar la carga, transformación y exportación de datos.
    
    Parameters:
    execution_date_str (str): Fecha de ejecución en formato de string (DD/MM/YYYY).
    """
    execution_date = pd.to_datetime(execution_date_str, dayfirst=True)
    
    # Bloque 1: Cargar datos de aparcamientos desde MongoDB
    df_parking = mongo_data_loader(mongo_config['collection_name_parking'], execution_date, mongo_config, estacionalidad_config)
    print("Datos Cargados")
    
    # Bloque 2: Transformar datos de aparcamientos
    df_transformed_parking = transform_parking_data(df_parking, execution_date)
    
    # Bloque 3: Preparar datos para el DataFrame final
    final_df = tranformacion_datos(df_transformed_parking)
    print("Datos Transformados")

    # Bloque 4: Exportar datos a PostgreSQL
    data_exporter(final_df, postgres_config)
    print("Datos Exportados")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <execution_date>")
        sys.exit(1)
    
    execution_date_str = sys.argv[1]
    main(execution_date_str)
