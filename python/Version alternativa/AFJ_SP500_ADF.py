from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator
from airflow.models.dag import DAG
from datetime import datetime
import configparser


config = configparser.ConfigParser()
config.read('/opt/airflow/dags/ETL_SP500/config/AFJ_SP500_ADF.config')


default_args = {
    'owner': 'airflow'
    ,'start_date': datetime(2024, 5, 10)
    ,'email': ['luis@gmail.com']
    ,'email_on_failure': True
    ,'email_on_retry': False
    ,'retries': 3,
}

with DAG(
    'AFJ_SP500_ADF'
    ,default_args=default_args
    ,description='Proceso ETL para obtener la informacion de las empresas del S&P500.'
    ,schedule_interval='@daily'
    ,catchup=False
    ,tags=["ETL", "SP500"]
    ) as dag:


    ejecutar_pipeline_adf = AzureDataFactoryRunPipelineOperator(
        task_id='run_pipeline',
        azure_data_factory_conn_id=config['conexiones']['id_conexion_adf']
        ,resource_group_name=config['conexiones']['grupo_recursos']
        ,factory_name=config['conexiones']['factory']
        ,pipeline_name=config['conexiones']['pipeline']
    )

    ejecutar_pipeline_adf
