import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import json
import os
import sys

# Verifica si el archivo de configuración existe
config_path = 'config.json'
if not os.path.exists(config_path):
    raise FileNotFoundError(f"El archivo de configuración {config_path} no se encuentra.")

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

# Carga el archivo de configuración
config = load_config(config_path)

def airquality_observed_data_loader(db_config, estacionalidad_config):
    """
    Carga los datos de calidad del aire desde una base de datos PostgreSQL.
    
    Parameters:
    db_config (dict): Configuración de la base de datos.
    estacionalidad_config (dict): Configuración de estacionalidad.
    
    Returns:
    DataFrame: Un DataFrame con los datos cargados de la base de datos.
    """
    # Consulta SQL para obtener los datos de calidad del aire
    query = """
    SELECT 
        recvtime as timeinstant, 
        entityid, 
        entitytype, 
        no2value, 
        pm25value, 
        pm10value, 
        o3value, 
        fiwareservicepath,
        CASE 
            WHEN EXTRACT(DOW FROM recvtime) IN (1, 2, 3, 4) THEN 'Laborable'
            WHEN EXTRACT(DOW FROM recvtime) = 5 THEN 'Viernes'
            WHEN EXTRACT(DOW FROM recvtime) = 6 THEN 'Sabado'
            WHEN EXTRACT(DOW FROM recvtime) = 0 THEN 'Domingo'
        END as tipodia,
        CASE 
            WHEN EXTRACT(MONTH FROM recvtime) = ANY(%(meses_alta)s) THEN 'Alta'
            ELSE 'Baja'
        END as estacionalidad
    FROM 
        vlci2.t_datos_cb_medioambiente_airqualityobserved
    WHERE 
        no2value IS NOT NULL 
        AND pm10value IS NOT NULL 
        AND pm25value IS NOT NULL 
        AND o3value IS NOT NULL;
    """

    # Conexión a la base de datos
    conn = psycopg2.connect(
        dbname=db_config['dbname'], 
        user=db_config['user'], 
        password=db_config['password'], 
        host=db_config['host'], 
        port=db_config['port']
    )

    # Ejecución de la consulta y carga de datos en un DataFrame
    df = pd.read_sql_query(query, conn, params={'meses_alta': estacionalidad_config['Alta']})
    conn.close()
    return df

def airquality_observed_preparacion_datos(data, fecha):
    """
    Transforma los datos observados de calidad del aire.
    
    Parameters:
    data (DataFrame): Datos de calidad del aire.
    fecha (str): Fecha en formato de string.
    
    Returns:
    DataFrame: Un DataFrame con los datos transformados.
    """
    # Agrupar y agregar los datos
    df_airqualityobserved = data.groupby([
        'entityid', 
        'entitytype', 
        'fiwareservicepath', 
        'tipodia', 
        'estacionalidad'
    ]).agg({
        'no2value': 'mean',
        'pm25value': 'mean',
        'pm10value': 'mean',
        'o3value': 'mean'
    }).reset_index()

    # Redondear los valores a dos decimales
    df_airqualityobserved['no2value'] = df_airqualityobserved['no2value'].round(2)
    df_airqualityobserved['pm25value'] = df_airqualityobserved['pm25value'].round(2)
    df_airqualityobserved['pm10value'] = df_airqualityobserved['pm10value'].round(2)
    df_airqualityobserved['o3value'] = df_airqualityobserved['o3value'].round(2)
    
    # Convertir la fecha de string a Timestamp
    fecha = pd.to_datetime(fecha, dayfirst=True)

    # Reordenar las columnas para mantener el orden deseado
    final_df = pd.DataFrame({
        'timeinstant': fecha,
        'sourceref': df_airqualityobserved['entityid'],
        'sceneref': 'N/A',
        'trend': df_airqualityobserved['estacionalidad'],
        'daytype': df_airqualityobserved['tipodia'],
        'no2': df_airqualityobserved['no2value'],
        'pm25': df_airqualityobserved['pm25value'],
        'pm10': df_airqualityobserved['pm10value'],
        'o3': df_airqualityobserved['o3value'],
        'entityid': df_airqualityobserved['entityid'],
        'entitytype': "AirQualityObserved",
        'recvtime': fecha,
        'fiwareservicepath': '/digitaltwin'
    })

    return final_df

def airquality_observed_data_exporter(final_df, config):
    """
    Exporta los datos transformados a una base de datos PostgreSQL.
    
    Parameters:
    final_df (DataFrame): Datos transformados.
    config (dict): Configuración de la base de datos de destino.
    """
    destination_db = config['destination_db']

    # Crear conexión al motor de la base de datos de destino
    engine = create_engine(f"postgresql://{destination_db['user']}:{destination_db['password']}@{destination_db['host']}:{destination_db['port']}/{destination_db['database']}")

    # Exportar los datos al esquema especificado en la base de datos
    final_df.to_sql(
        'dtwin_airqualityobserved',
        engine,
        schema=destination_db['schema'],
        if_exists='append',
        index=False
    )

def main(fecha):
    """
    Función principal para ejecutar la carga, transformación y exportación de datos.
    
    Parameters:
    fecha (str): Fecha en formato de string DD/MM/YYYY.
    """
    config = load_config(config_path)
    db_config = config['extraccion_airqualityobserved']
    estacionalidad_config = config['estacionalidad']

    # Cargar datos
    df = airquality_observed_data_loader(db_config['source_db'], estacionalidad_config)
    print("Datos Cargados")

    # Transformar datos
    transformed_df = airquality_observed_preparacion_datos(df, fecha)
    print("Datos Transformados")

    # Exportar datos
    airquality_observed_data_exporter(transformed_df, db_config)
    print("Datos Exportados")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extraccion_airqualityobserved.py <fecha>")
        sys.exit(1)
    
    fecha = sys.argv[1]
    main(fecha)
