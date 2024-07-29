import pandas as pd
from sqlalchemy import create_engine
import datetime
import json
import psycopg2
import warnings
import sys

# Suprimir advertencias de pandas y psycopg2
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

# Bloque 1: frecuencia_paso_data_loader
def frecuencia_paso_data_loader():
    """
    Carga los datos de frecuencia de paso desde un archivo CSV.
    
    Returns:
    DataFrame: Un DataFrame con los datos cargados del archivo CSV.
    """
    filepath = 'frecuencia_paso_EMT.csv'
    frecuencia_df = pd.read_csv(filepath)

    # Limpiar espacios extra en todas las columnas de tipo string
    frecuencia_df = frecuencia_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    return frecuencia_df

# Bloque 2: preparacion_datos_frecuencia_pre_union
def preparacion_datos_frecuencia_pre_union(data):
    """
    Prepara los datos de frecuencia antes de la unión con otros datos.
    
    Parameters:
    data (DataFrame): Datos de frecuencia de paso.
    
    Returns:
    DataFrame: Un DataFrame con los datos preparados.
    """
    df_ida = data[data['trip_id'].str.endswith('I')]
    df_vuelta = data[data['trip_id'].str.endswith('V')]

    # Agrupar y sumar las paradas y los trayectos
    paradas_ida = df_ida.groupby(['SHORT', 'Servicio'])['num_paradas'].sum().reset_index(name='paradas_ida')
    paradas_vuelta = df_vuelta.groupby(['SHORT', 'Servicio'])['num_paradas'].sum().reset_index(name='paradas_vuelta')

    trayectos_ida = df_ida.groupby(['SHORT', 'Servicio'])['trayectos'].sum().reset_index(name='trayectos_ida')
    trayectos_vuelta = df_vuelta.groupby(['SHORT', 'Servicio'])['trayectos'].sum().reset_index(name='trayectos_vuelta')

    # Unir los DataFrames de ida y vuelta
    df_final = pd.merge(paradas_ida, paradas_vuelta, on=['SHORT', 'Servicio'])
    df_final = pd.merge(df_final, trayectos_ida, on=['SHORT', 'Servicio'])
    df_final = pd.merge(df_final, trayectos_vuelta, on=['SHORT', 'Servicio'])

    # Diccionario auxiliar para traducir los nombres del servicio a los tipos de día del proyecto
    dict_dias_servicio = {'LAB': 'Laborable', 'SAB': 'Sábado', 'FES': 'Domingo'}
    
    # Mapear el servicio a los tipos de días usando el diccionario
    df_final['tipodia'] = df_final['Servicio'].map(dict_dias_servicio)

    return df_final

# Bloque 3: autobuses_data_loader
def autobuses_data_loader(db_config, config):
    """
    Carga los datos de los autobuses desde una base de datos PostgreSQL.
    
    Parameters:
    db_config (dict): Configuración de la base de datos.
    config (dict): Configuración general del sistema.
    
    Returns:
    DataFrame: Un DataFrame con los datos cargados de la base de datos.
    """
    query = """
    WITH total_diario AS (
    SELECT sliceanddice1, sliceanddicevalue1, DATE_TRUNC('day', calculationperiod) AS dia, 
        CASE 
            WHEN diasemana IN ('L', 'M', 'X', 'J') THEN 'Laborable'
            WHEN diasemana = 'V' THEN 'Viernes'
            WHEN diasemana = 'S' THEN 'Sábado'
            WHEN diasemana = 'D' THEN 'Domingo'
        END AS tipo_dia, 
        SUM(kpivalue) AS kpivalue, COUNT(kpivalue) AS muestras,
        CASE 
            WHEN EXTRACT(MONTH FROM calculationperiod) = ANY(%(meses_alta)s) THEN 'Alta'
            ELSE 'Baja'
        END AS estacionalidad
        FROM vlci2.t_datos_cb_emt_kpi
        WHERE sliceanddice1 = 'Ruta' AND kpivalue >= 0
        GROUP BY 1, 2, 3, 4, 7
    )
    SELECT sliceanddice1, sliceanddicevalue1, tipo_dia, estacionalidad,
        AVG(kpivalue) AS total_kpivalue, 
        COUNT(kpiValue) AS cuentaViajeros, SUM(kpivalue) AS sumaViajeros, SUM(muestras) AS sumaMuestras
    FROM total_diario
    GROUP BY 1, 2, 3, 4
    ORDER BY sliceanddicevalue1, tipo_dia;
    """

    # Conexión a la base de datos PostgreSQL
    conn = psycopg2.connect(
        dbname=db_config['dbname'], 
        user=db_config['user'], 
        password=db_config['password'], 
        host=db_config['host'], 
        port=db_config['port']
    )
    
    # Obtener los meses de estacionalidad alta del archivo de configuración
    meses_alta = config['estacionalidad']['Alta']
    
    df_buses = pd.read_sql_query(query, conn, params={'meses_alta': meses_alta})
    conn.close()
    return df_buses

# Bloque 4: union_df_autobuses
def union_df_autobuses(df_buses, frecuencia_df):
    """
    Realiza la unión de los datos de los autobuses con los datos de frecuencia de paso.
    
    Parameters:
    df_buses (DataFrame): Datos de los autobuses.
    frecuencia_df (DataFrame): Datos de frecuencia de paso preparados.
    
    Returns:
    DataFrame: Un DataFrame con los datos fusionados.
    """
    # Realizar la fusión teniendo en cuenta tanto la línea como el tipo de día
    merged_df = pd.merge(
        df_buses, 
        frecuencia_df, 
        how='left', 
        left_on=['sliceanddicevalue1', 'tipo_dia'], 
        right_on=['SHORT', 'tipodia']
    )

    return merged_df

# Bloque 5: df_emt_viajeros
def df_emt_viajeros(data, fecha):
    """
    Prepara el DataFrame final con los datos de viajeros de EMT.
    
    Parameters:
    data (DataFrame): Datos fusionados de autobuses y frecuencia.
    fecha (str): Fecha en formato de string DD/MM/YYYY.
    
    Returns:
    DataFrame: Un DataFrame con los datos finales listos para exportar.
    """
    fecha = pd.to_datetime(fecha, dayfirst=True)

    # Creación del DataFrame
    df_emt_viajeros = pd.DataFrame({
        'timeinstant': fecha,
        'sourceref': data['sliceanddicevalue1'],
        'sceneref': 'N/A',
        'trend': data['estacionalidad'],
        'daytype': data['tipo_dia'],
        'forwardtrips': pd.to_numeric(data['trayectos_ida'], errors='coerce').astype('Int64'),
        'returntrips': pd.to_numeric(data['trayectos_vuelta'], errors='coerce').astype('Int64'),
        'forwardstops': pd.to_numeric(data['paradas_ida'], errors='coerce').astype('Int64'),
        'returnstops': pd.to_numeric(data['paradas_vuelta'], errors='coerce').astype('Int64'),
        'recvtime': fecha,
        'intensity': data['total_kpivalue'],
        'entityid': data['sliceanddicevalue1'],
        'entitytype': 'RouteSchedule',
        'recvtime': fecha,
        'fiwareservicepath': '/digitaltwin'
    })

    return df_emt_viajeros

# Bloque 6: emt_viajeros_data_exporter
def emt_viajeros_data_exporter(df: pd.DataFrame, db_config):
    """
    Exporta los datos de viajeros de EMT a una base de datos PostgreSQL.
    
    Parameters:
    df (DataFrame): Datos finales para exportar.
    db_config (dict): Configuración de la base de datos de destino.
    """
    engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    df.to_sql(
        'dtwin_routeintensity',
        engine,
        schema=db_config['schema'],
        if_exists='append',
        index=False
    )

# Función principal para ejecutar todos los bloques
def main(fecha):
    """
    Función principal para ejecutar la carga, transformación, fusión y exportación de datos.
    
    Parameters:
    fecha (str): Fecha en formato de string DD/MM/YYYY.
    """
    config = load_config('config.json')
    db_config = config['frecuencia_paso_data_loader']

    # Bloque 1: Cargar datos del CSV
    df_frecuencia = frecuencia_paso_data_loader()
    

    # Bloque 2: Transformar datos para pre-unión
    frecuencia_df = preparacion_datos_frecuencia_pre_union(df_frecuencia)
    

    # Bloque 3: Cargar datos de autobuses desde PostgreSQL
    df_buses = autobuses_data_loader(db_config['source_db'], config)
    print("Datos Cargados")

    # Bloque 4: Fusionar datos
    merged_df = union_df_autobuses(df_buses, frecuencia_df)
    

    # Bloque 5: Preparar DataFrame final
    final_df = df_emt_viajeros(merged_df, fecha)
    print("Datos Transformados")

    # Bloque 6: Exportar datos a PostgreSQL
    emt_viajeros_data_exporter(final_df, db_config['destination_db'])
    print("Datos Exportados")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <fecha>")
        sys.exit(1)
    
    fecha = sys.argv[1]
    main(fecha)
