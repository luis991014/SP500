from datetime import datetime
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from ETL_SP500.classes.Orquestador import Orquestador_copiado
import configparser


config = configparser.ConfigParser()
config.read('/opt/airflow/dags/ETL_SP500/config/AFJ_SP500_PD.config')

orquestador = Orquestador_copiado(id_conexion_snowflake=config['conexiones']['id_conexion_snowflake'])

default_args = {
    'owner': 'airflow'
    ,'start_date': datetime(2024, 5, 10)
    ,'email': ['luis@gmail.com']
    ,'email_on_failure': True
    ,'email_on_retry': False
    ,'retries': 3,
}


with DAG(
    'AFJ_SP500_PD'
    ,default_args=default_args
    ,description='Proceso ETL para obtener la informacion de las empresas del S&P500.'
    ,schedule_interval='@daily'
    ,catchup=False
    ,tags=["ETL", "S&P500"]
    ) as dag:
    
    py_descargar_informacion = PythonOperator(
        task_id = 'descargar_informacion'
        ,python_callable=orquestador.descargar_informacion
    )

    py_limpiar_csvs = PythonOperator(
        task_id = 'limpiar_csvs'
        ,python_callable=orquestador.limpiar_csvs
    )

    py_ingestar_datos = PythonOperator(
        task_id = 'ingestar_datos'
        ,python_callable=orquestador.ingestar_datos
    )

    py_descargar_informacion >> py_limpiar_csvs >> py_ingestar_datos