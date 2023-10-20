
**

# DataFlowUtil

**


**DataFlowUtil** es una libreria que facilita la interacción con los servicios de Google Cloud Platform (GCP). A través de una serie de módulos y funciones, proporciona funcionalidades para conectarse y trabajar con diferentes servicios de GCP, Adicionalmente, **DataFlowUtil** ofrece capacidades de procesamiento y verificación de datos para garantizar la calidad y utilidad de la información manejada.

![](https://drive.google.com/uc?id=1HaEUXeOgPo0so8GQBf7S_t6xqXMv43Ef)

## Actualmente Soporta
* Conexión a Buckets de GCP
* Conexión a BigQuery GCP:
* Conexión a Google Sheets API
* Procesamiento de Datos
* Comprobación de Datos


## Importacion de Clases
Las clases que posee la libreria son:
```python
from dataflowutil.config import extra_var as extra_v
from dataflowutil.libs import app_struct as app
```

## Funciones de la Libreria
```python
load_data(db,reduce_memory=False)
get_load_data()
get_load_data_local()
get_only_data(tag="")
get_only_data_local(tag="")
get_data_compare(tag="")
get_list_blobs()
upload_data_buckets()
upload_load_data()
start_check_historic(tag="")
start_check_new(tag="")
run_routine(name_project,dataset,procedure)
run_transfer(project_number,location,transfer_config_id)
select_query(query)
```

## Explicación Funciones

* **load_data :** Encargada en la carga de datos, el cual recibe 2 argumentos: '**db**' y '**reduce_memory**', cuando **reduce_memory** esta en **TRUE** evitara guardar todas las bases en memoria lo cual procede a cargar la base y subirla a bigquery directamente. reduciendo el consumo de memoria.

###### **IMPORTANTE** Las funciones mencionadas a continuacion funcionan unicamente si el reduce_memory estan en FALSE

* **get_load_data :** Devuelve una lista con las datas obtenidas del bucket.

* **get_load_data_local :** Devuelve una lista con las datas obtenidas de nuestra maquina local

* **get_only_data :** Devuelve unicamente 1 data del bucket basada en el tag otorgado

* **get_only_data_local :** Devuelve unicamente 1 data local basada en el tag otorgado

* **get_data_compare :** Devuelve 2 elementos, data local y data bucket la cual nos ayuda a hacer comparaciones de las 2 datas

* **get_list_blobs :** Devuelve una lista de las rutas y archivos .xlsx y .csv que tenemos en nuestro bucket.

* **upload_data_buckets :** Se encarga de almacenar la data local al bucket

* **upload_load_data :** Se encarga de obtener la data del bucket y subirla a bigquery

* **start_check_historic :** Es la encargada de hacer comprobaciones de correracion , dtype, nulos, entre otras verificaciones entre la data del bucket y nuestra data local. (unicamente comprobaciones con datos historicos.)
*  **start_check_new:** Se encarga en comprobar los nuevos registros de la data, verificando unicamente los nuevos registros, dejando a un lado datos historicos
*  **run_routine:** Esta funciona se conecta  al cuenta de servicios y se encarga en correr rutinas de BigQuery.
*  **run_transfer:** Es la encarga de correr el servicio de trasferencia de datos de BigQuery
*  **select_query:** Esta funcion realiza consultas sql que se envian a bigquery. 


## Configuracion y Creacion Del Proyecto
Para la creacion y configuracion de un nuevo proyecto es necesito ciertos pasos para el funcionamiento de la libreria.

###### Se necesita configurar el proyecto con los siguientes pasos mencionados:

* Adentro del siguiente **repositorio** se encontraran 2 subfolders 
    1.**files_configuration**: el cual posee los 2 spreadsheet de configuracion que estaran ubicados en el google drive.

    2.**project_template**: los archivos de esta carpeta son esenciales a la hora de crear un nuevo proyecto, en esta carpeta se encuentran 
    - Carpetas: **Credentials**, **Upload**
    - Py: **main_process_1** , **main_process_2**,**main_process_comprobation** , **data**

<div align="center">

[Link Repositorio](https://github.com/WorldArdFelipe/dataflowutil_proyect)

</div>

### Configuracion SpreadSheets

##### Estos archivos van ubicados en google drive.

* En la carpeta **files_configuration** estara 2 spreadsheets llamados **DataFlowUtil Production.xlsx** y **DataFlowUtil Production.xlsx** los cuales tienen la misma estructura solo que uno se usa para produccion y el otro para testing. Estos archivos contienen 3 Hojas, las cuales son : 

##### <p align="center"> DATA_LOCAL_TO_BUCKET </p>
Se encarga de configurar el upload de nuestra data local al bucket:
![](https://drive.google.com/uc?id=1buANxjUvbxzCfLcyS9ShXIf0CpXxEDtZ)

##### <p align="center"> DATA_BUCKET_TO_BIGQUERY </p>
Se encarga de configurar el upload de nuestra data bucket a bigquery

![](https://drive.google.com/uc?id=1-4RUZG14AJ2CBHDHXNbMpiKZd3okyEAa)

##### <p align="center"> DATA_COMPARE</p>
Se encarga de comparar la data del bucket con la data local

![](https://drive.google.com/uc?id=1ZB2TXL3ADCN26uSMBszXMVi2zB8NgqX_)

* ***PATH_LOCAL :*** Esta variable tendra la dirrecion y el nombre de la data que esta ubicada en la carpeta **upload** 

* ***PATH_BUCKET :*** Esta variable tendra la ruta donde el proceso envia la data local al bucket.

* ***UPDATE :*** Esta variable esta basada en 2 status , status 0 / 1 , cuando el status es 0 quiere decir que el proceso solo aplicara cambios a esa data no a todas, y si status es 1 el proceso no tomara esa data.

* ***TAG/DB_NAME :*** Esta variable se encarga de otorgarle un tag a esa data , la cual tomara como refenrencia y a la hora de subir la data a bigquery creara la tabla basado en ese tag

* ***SHEET_PAGE :*** Se define en que pagina del excel esta la data que se quiere carga a bigquery, si se quiere concatenar 2 paginas en 1 , el valor seria ejemplo : 0-3, quiere decir que va a concatenar la pagina 0 y la pagina 3 y creara 1 dataframe.

### Configuracion Carpeta Credentials
* En la carpeta **credentials** se encontrara 2 archivos llamados **connection_testing.ini** y **connection_production.ini** los cuales se encargan en la configuracion de las conexiones de BigQuery, Buckets, Google Sheets. Y dentro de esa misma carpeta es necesario colocar las **cuentas de servicio** de google.

Ejemplo:
![](https://drive.google.com/uc?id=1u_T3t8weAsIqSTV0QuspNv72H9DaMCb3)

* Los archivos **connection_testing.ini** y **connection_production.ini** manejan la misma estructura lo unico que cambia son las conexiones a las cuales van dirigidas.


##### Estructura:
```ini
[Config.Credentials]
credentials_path = cuenta_servicio_production.json

[Config.Bucket]
bucket_path = gs://bucket_path/
bucket_name = bucket_name

[Config.BigQuery]
project_id = project_id_bigquery
name_db_bigquery = name_db_bigquery

[Config.SpreadSheets]
id_spread_sheets = 0000000
page_sheet_local_to_bucket = DATA_LOCAL_TO_BUCKET
page_sheet_bucket_to_bigquery = DATA_BUCKET_TO_BIGQUERY
page_sheet_data_compare = DATA_COMPARE

```

### Configuracion Carpeta Upload

* Adentro de la carpeta **upload** van nuestras bases de datos locales, ya sea **.xlsx** o **.csv** las cuales se van a subir a nuestro bucket

### Configuracion Archivos Python
* En la carpeta encontraran 3 archivos python los cuales son:  
    * **main_process_1** 
    * **main_process_2** 
    * **main_process_comprobation** 
    * **data**


######  Importante:  antes de ejecutar los siguientes procesos se tiene que tener configurado las credenciales en el proyecto y los spreedsheet ubicados en google drive

##### Nota: Todos estos procesos va de la mano con los spreedsheet de configuracion. 

### <p align="center"> Main_Process_1 </p>

###### SpreedSheet de configuracion: DATA_LOCAL_TO_BUCKET
Este proceso sera el encargado de detectar la data que esta guardada en la carpeta upload y subirla a nuestro bucket

### <p align="center"> Main_Process_2 </p>

######SpreedSheet de configuracion: DATA_BUCKET_TO_BIGQUERY
Este proceso sera el encargado de detectar la data que esta guardada en bucket y subirla a bigquery

### <p align="center"> Main_Process_Comprobation </p>

######SpreedSheet de configuracion: DATA_COMPARE
Este proceso sera el encargado mediante diferente funciones de hacer comprobaciones de correacion, entre la data local y la data del bucket, garantizando un upload de data al bucket sin errores.

### <p align="center"> data </p>

Este .py va en conjunto con los procesos mencionados anteriormente, este archivo sera el encargado de hacerle transformaciones a la data cargada.   

La estructura default de este archivo sera:

![](https://drive.google.com/uc?id=1algENuDlPWsUJXftLb0za2573XSflGSU)


Si queremos hacerle un ETL a una data antes de subirla a bigquery, lo podemos hacer teniendo de referencia el ***TAG/DB_NAME** mencionado anteriormente, Teniendo ya nuesto ***TAG/DB_NAME** ubicado, procedemos a crear el ETL, en este caso se usara el tag ***new_data_kpis***, los pasos seran los siguientes: 

###### Importante: Estos pasos se adaptaran a cualquier otra data, Solo cambiaria el ***TAG/DB_NAME**


* Creamos un **self** con el nombre del ***TAG/DB_NAME**, nos quedaria , **self.new_data_kpis()**

* Copiamos la plantilla del def y editamos lo que dice **name_data** por el nombre de nuestro ***TAG/DB_NAME** 

    Antes: 

    ```python

        @dp.DataProcessing.transformation(name_tag="name_data")
        def name_data(self, data):
            # Var "data" is dataframe variable
            # use var "data" for transformations

            return data
    ```

    Despues: 

    ```python

        @dp.DataProcessing.transformation(name_tag="new_data_kpis")
        def new_data_kpis(self, data):
            # Var "data" is dataframe variable
            # use var "data" for transformations

            return data
    ```
* Teniendo nuestra funcion creada procedemos a hacerle el ETL correspondiente, en este caso vamos a agregarle 3 columnas nuevas llamadas **kpi1** , **kpi2** y **sum** donde el def nos quedaria de la siguiente manera:

    ```python

        @dp.DataProcessing.transformation(name_tag="new_data_kpis")
        def new_data_kpis(self, data):
            # Var "data" is dataframe variable
            # use var "data" for transformations

            data["kpi1"] = 1
            data["kpi2"] = 10

            data["sum"] = data["kpi1"]+data["kpi2"]

            return data
    ```

* Nuestro codigo final nos quedaria de esta manera:

    ![](https://drive.google.com/uc?id=1WBZ0HHXCwODoIUM1L8nBTe5i7s7LFa5T)

* Si queremos agregar otra data para hacerle un ETL especifico , el codigo final nos quedaria de la siguiente manera:
    
    ![](https://drive.google.com/uc?id=10kbUsLziYT9IeAjcZBnPm9qlluMqX1_w)