# Instrucciones para ejecutar el proyecto.

Para la ejecucion del proyecto seguir los siguientes pasos:

1. **Crear objetos SQL en Snowflake:** Antes de comenzar, asegúrate de crear los objetos SQL necesarios en tu entorno Snowflake.
2. **Editar archivos .config:** Abre y edita los archivos con extensión .config para especificar los valores requeridos según tus necesidades.
3. **Transferir archivos:** Mueve los archivos ubicados dentro de la carpeta "orquestador-etl-sp500" al directorio que contiene los Directed Acyclic Graphs (DAGs) en tu servidor de Airflow.
4. **Iniciar la ejecución del DAG:** Una vez completados los pasos anteriores, procede a iniciar la ejecución del DAG para poner en marcha el proceso.

# Descripcion de la arquitectura.

Para este proyecto, se optó por implementar un esquema copo de nieve con miras al futuro, con la idea de no limitarnos solo al análisis de empresas pertenecientes al índice S&P500, sino también de poder agregar más empresas de diversos índices. Esta elección facilita la escalabilidad de la solución de manera más sencilla.

![Arquitectura general](./Arquitectura%20General.png)

La arquitectura general se plantea de la siguiente manera: inicialmente, los datos provendrán de APIs, bases de datos relacionales e información recopilada mediante web scraping. Para integrar estos datos, tenemos dos opciones:

1. Integración de datos utilizando Python (Pandas, Polars, SQLalchemy, etc.) y Airflow para orquestar estos procesos.
2. Integración de datos utilizando Azure Data Factory (ADF) y Airflow para orquestar los pipelines desarrollados en ADF (se incluyó un DAG que muestra cómo se ejecutaría desde Airflow).

Una vez que los datos estén integrados en Azure Cloud, toda la información llegará a nuestro lago de datos, que en este caso será un Blob Storage configurado como lago de datos.

Para la integración con nuestro Data Warehouse, tenemos dos opciones:

1. Realizar la integración directamente tomando los datos de nuestro lago de datos y utilizando Azure Data Factory.
2. Utilizar Python (Pandas, Polars, SQLalchemy) para realizar inserciones de datos en Snowflake.

Finalmente, tendremos nuestros informes elaborados en Power BI, los cuales estarán conectados a nuestro Data Warehouse para obtener la información necesaria.

# Desiciones tecnicas.

Las desiciones tecnicas en este oproyecto fueron las siguientes:

1. Se optó por utilizar el esquema de copo de nieve debido a su facilidad de escalabilidad sin afectar de manera invasiva nuestra solución, lo que evita el deterioro del rendimiento.

2. Se decidió utilizar Python (Pandas, Polars, SQLalchemy, etc.) principalmente porque actualmente no cuento con un entorno en Azure Data Factory para crear pipelines. Por lo tanto, en todo el proceso, hago uso de estas librerías para limpiar y transformar los datos mediante Dataframes y posteriormente integro la información directamente hacia Snowflake.

