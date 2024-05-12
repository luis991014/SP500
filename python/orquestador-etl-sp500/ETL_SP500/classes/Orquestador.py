import pandas as pd
import glob
import sqlalchemy as sql
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine
import configparser


config = configparser.ConfigParser()
config.read('/opt/airflow/dags/CopiadoKPI/config/AFJ_SP500_PD.config')


class Orquestador_copiado():

    def __init__(self, id_conexion_snowflake) -> None:
        self.id_conexion_snowflake = id_conexion_snowflake


    def descargar_informacion(self) -> None:

        """
            Funcion para descargar la informacion de las empresas en csv.

            Returns:
                None
        """

        # En este caso no se usara esta funcion. Ya que la informacion ya la tenemos descargada.

        pass


    def limpiar_csvs(self):

        try:

            index_name = 'S&P500'
            archivos_csv = glob.glob(f"{config['rutas']['ruta_archivos_raw']}/*.csv")

            df_stocks = self.ejecuta_consulta_sql_snowflake(consulta_sql=config['consultas']['consulta_cat_stock_names'])
            df_indexes = self.ejecuta_consulta_sql_snowflake(consulta_sql=config['consultas']['consulta_cat_indexes'])
            df_dates = self.ejecuta_consulta_sql_snowflake(consulta_sql=config['consultas']['consulta_cat_dates'])
            df_dates['date'] = pd.to_datetime(df_dates['date'])

            for archivo in archivos_csv:

                df_empresa = pd.read_csv(filepath_or_buffer=archivo
                                        ,header=0)
                
                stock_name = df_empresa['Name'].iloc[0]

                id_stock = df_stocks.loc[df_stocks['stock_name'] == df_empresa['Name'].iloc[0]]['id'].iloc[0]
                id_index = df_indexes.loc[df_indexes['index_name'] == index_name]['id'].iloc[0]

                df_empresa['id_stock'] = [id_stock] * len(df_empresa)
                df_empresa['id_index'] = [id_index] * len(df_empresa)
                df_empresa.insert(0, 'id_date', [0] * len(df_empresa))
                
                for date in df_empresa['date']:

                    id_date = df_dates.loc[df_dates['date'] == pd.to_datetime(date)]['id'].iloc[0]
                    df_empresa.loc[df_empresa['date'] == date, 'id_date'] = id_date

                df_empresa = df_empresa.drop(columns=['Name'])
                df_empresa = df_empresa.drop(columns=['date'])

                df_empresa.to_csv(path_or_buf=f"{config['rutas']['ruta_archivos_clean']}/{stock_name}.csv"
                                ,header=True
                                ,index=False)
                
        except:
            raise Exception('Error: limpiar_csvs')


    def ingestar_datos(self):

        try:

            conn = BaseHook.get_connection(self.id_conexion_snowflake)
            cadena_conexion = f'snowflake://{conn.login}:{conn.password}@{conn.host}/{conn.schema}/public'
            engine = create_engine(cadena_conexion)

            archivos_csv = glob.glob(f"{config['rutas']['ruta_archivos_clean']}\\*.csv")

            for archivo in archivos_csv:

                df = pd.read_csv(archivo, header=0)

                df.to_sql(name='his_stocks'
                        ,con=engine
                        ,schema='public'
                        ,if_exists='append'
                        ,index=False)
                
        except:
            raise Exception('Error: ingestar_datos')


    def ejecuta_consulta_sql_snowflake(self, consulta_sql:str):

        """
            Funcion para ejecutar consultas sql en SnowFlake.

            Returns:
                None
        """

        try:
            conn = BaseHook.get_connection(self.id_conexion_snowflake)
            cadena_conexion = f'snowflake://{conn.login}:{conn.password}@{conn.host}/{conn.schema}/public'

            engine = sql.create_engine(cadena_conexion)
            with engine.connect() as conn:
                df = pd.read_sql_query(consulta_sql, con=conn)

            return df
        
        except:
            raise Exception('Error: ejecuta_consulta_sql')
        
        finally:
            engine.dispose()

