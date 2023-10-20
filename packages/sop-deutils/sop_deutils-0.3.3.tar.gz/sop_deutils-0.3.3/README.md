# Yes4All SOP Utils Packages

This is a utils package served for SOP Data Analytics team at **Yes4All**. It contains various modules to work with **PostgreSQL, MinIO, Google API, Airflow, Telegram...**

---
<img  src="https://lh3.googleusercontent.com/drive-viewer/AK7aPaCxUGMFDqsjfE2pz3I5DdEupNwPVjPkoLd_6ifiMPt5harMEBNBUuJTh812_KmI_p1cWZpEMQRtSZ8O8-uyhdGmIc7Wxg=s1600"  alt="liuliukiki"  width="200"  />

## Contents Overview
### [Install package](#install-package-1)
### [Modules usage](#modules-usage-1)
1. #### [Airflow](#airflow-1)
2. #### [GoogleSheet](#googlesheet-1)
	##### [initialize module](#21-initialize)
	##### [```create_spread_sheet```](#22-create_spread_sheet)
	##### [```list_all_work_sheets```](#23-list_all_work_sheets)
	##### [```delete_work_sheet```](#24-delete_work_sheet)
	##### [```clear_work_sheet```](#25-clear_work_sheet)
	##### [```get_data```](#26-get_data)
	##### [```insert_data```](#27-insert_data)
	##### [```update_data```](#28-update_data)
	##### [```remove_data```](#29-remove_data)
3. #### [MinIO](#minio-1)
	##### [initialize module](#31-initialize)
	##### [```data_exist```](#32-data_exist)
	##### [```get_data_value_exist```](#33-get_data_value_exist)
	##### [```load_data```](#34-load_data)
	##### [```get_data```](#35-get_data)
	##### [```get_data_wildcard```](#36-get_data_wildcard)
4. #### [PostgreSQL](#postgresql-1)
	##### [initialize module](#41-initialize)
	##### [```read_sql_file```](#42-read_sql_file)
	##### [```insert_data```](#43-insert_data)
	##### [```bulk_insert_data```](#44-bulk_insert_data)
	##### [```upsert_data```](#45-upsert_data)
	##### [```bulk_upsert_data```](#46-bulk_upsert_data)
	##### [```update_table```](#47-update_table)
	##### [```get_data```](#48-get_data)
	##### [```select_distinct```](#49-select_distinct)
	##### [```show_columns```](#410-show_columns)
	##### [```execute```](#411-execute)
	##### [```add_column```](#412-add_column)
	##### [```create_table```](#413-create_table)
	##### [```grant_table```](#414-grant_table)
	##### [```truncate_table```](#415-truncate_table)
	##### [```table_exists```](#416-table_exists)
5. #### [Telegram](#telegram-1)
6. #### [DAConfig](#all-in-one-daconfig)
6. #### [Workflow Example](#workflow-example-1)


## User Guide Documentation

### Install package

```bash
$ pip install --upgrade sop-deutils
```

---

### Modules usage

#### Airflow

***Use case:*** when having a new scheduled task file on Airflow.

***Functional:***

Auto naming DAG ID and alerting failed DAG to Telegram:
- Sample code of base config Airflow  ```dag``` file: 

	```python
	from airflow import DAG
	from airflow.decorators import task
	from sop_deutils.y4a_airflow import auto_dag_id, telegram_alert

	default_args = {
	    "retries":  20,			# number times to retry when the task is failed
	    "retry_delay": timedelta(minutes=7),			# time delay among retries
	    "start_date": datetime(2023, 7, 14, 0, 0, 0),			# date that the DAG start to run 
	    "owner": 'duikha',			# account name of DAG owner
	    "on_failure_callback": telegram_alert,			# this contains function to alert to Telegram when the DAG/task is failed
	    "execution_timeout": timedelta(hours=4),			# limit time the DAG run
	}

	dag = DAG(
	    dag_id=auto_dag_id(),			# this contains function to name the DAG based on the file directory
	    description='Sample DAG',			# description about the DAG
	    default_args=default_args,			# default arguments contains dictionary of predefined params above
	    catchup=False,			# If True, the DAG will backfill tasks from the start_date to current date
	)

	with dag:
	    @task
	    def function_1():
	        ...

	    @task
	    def function_2():
	        ...

	    function_1() >> function_2()
	```

- List of account name can be found [here](https://docs.google.com/document/d/1jMouKkrJsqcGlxkgB1aJldGI-Osr3PYt3K1bwUM3I5c/edit?usp=sharing).

---

#### GoogleSheet

***Use case:*** when interacting with Google Sheet.

***Functional:***

##### 2.1 initialize
Firstly, import GoogleSheet utils module class. If want to use personal credentials, provide the dictionary of credentials as value of parameter ```user_creds```.

```python
from sop_deutils.gg_api.y4a_sheet import GGSheetUtils

sheet_utils = GGSheetUtils(
    user_creds=None,
)
```

##### 2.2 ```create_spread_sheet```
To create a new spread sheet, using ```create_spread_sheet``` method, it has three parameters:
- ```sheet_name``` (required): name of the sheet to create. ***(str)***
- ```folder_id``` (optional): id of the folder contains spreadsheet. The default value is ```None```. ***(str)***
- ```share_to``` (optional): list of email to share the spreadsheet. The default value is ```[]```. ***(list)***

	The method will return the created spreadsheet id.

	```python
	spread_sheet_id = sheet_utils.create_spread_sheet(
	    sheet_name='my-sheet-name',
	    folder_id='my-folder-id',
	    share_to=['longnc@yes4all.com'],
	)

	print(spread_sheet_id)
	```
	Output:
	```bash
	1vTjZOcRfd5eiF5Qo8DCha29Vdt0zvYP11XPbq54eCMg
	```

##### 2.3 ```list_all_work_sheets```
To get all available worksheet of spreadsheet, using ```list_all_work_sheets``` method, it has one parameter:
- ```sheet_id``` (required): spreadsheet id. ***(str)***

	The method will return list all worksheets of spreadsheet.

	```python
	work_sheets = sheet_utils.list_all_work_sheets(
	    sheet_id='my-sheet-id',
	)

	print(work_sheets)
	```
	Output:
	```bash
	['Sheet1']
	```

##### 2.4 ```delete_work_sheet```
To delete specific worksheet of spreadsheet, using ```delete_work_sheet``` method, it has two parameters:
- ```sheet_id``` (required): spreadsheet id. ***(str)***
- ```sheet_name``` (optional): worksheet name. The default value is ```'Sheet1'```. ***(str)***

	```python
	sheet_utils.delete_work_sheet(
	    sheet_id='my-sheet-id',
	    sheet_name='my-sheet-name',
	)
	```

##### 2.5 ```clear_work_sheet```
To clear all data of specific worksheet of spreadsheet, using ```clear_work_sheet``` method, it has two parameters:
- ```sheet_id``` (required): spreadsheet id. ***(str)***
- ```sheet_name``` (optional): worksheet name. The default value is ```'Sheet1'```. ***(str)***

	```python
	sheet_utils.clear_work_sheet(
	    sheet_id='my-sheet-id',
	    sheet_name='my-sheet-name',
	)
	```

##### 2.6 ```get_data```
To get data from the given sheet, using ```get_data``` method, it has five parameters:
- ```sheet_id``` (required): spreadsheet id. ***(str)***
- ```sheet_name``` (optional): worksheet name. The default value is ```'Sheet1'```. ***(str)***
- ```range_from``` (optional): the begining of the range of data from sheet to get. The default value is ```'A'```. ***(str)***
- ```range_to``` (optional):  the end of the range of data from sheet to get. The default value is ```'Z'```. ***(str)***
- ```columns_first_row``` (optional): whether to convert the first row to columns. The default value is ```False```. ***(bool)***

	```python
	df = sheet_utils.get_data(
	    sheet_id='my-sheet-id',
	    columns_first_row=True,
	)

	print(df)
	```
	Output:
	```bash
	| Column1 Header | Column2 Header | Column3 Header |
	| ---------------| ---------------| ---------------|
	| Row1 Value1    | Row1 Value2    | Row1 Value3    |
	| Row2 Value1    | Row2 Value2    | Row2 Value3    |
	| Row3 Value1    | Row3 Value2    | Row3 Value3    |
	```

##### 2.7 ```insert_data```
To insert data to the given sheet, using ```insert_data``` method, it has five parameters:
- ```data``` (required): dataframe contains data to insert. ***(pd.DataFrame)***
- ```sheet_id``` (required): spreadsheet id. ***(str)***
- ```sheet_name``` (optional): worksheet name. The default value is ```'Sheet1'```. ***(str)***
- ```from_row_index``` (optional):  the index of the row beginning to insert. The default value is ```1```. ***(int)***
- ```insert_column_names``` (optional): whether to insert column names. The default value is ```False```. ***(bool)***

	```python
	sheet_utils.insert_data(
	    data=df,
	    sheet_id='my-sheet-id',
	    from_row_index=2,
	    insert_column_names=False,
	)
	```

##### 2.8 ```update_data```
To update data of the given sheet, using ```update_data``` method, it has five parameters:
- ```data``` (required): dataframe contains data to update. ***(pd.DataFrame)***
- ```sheet_id``` (required): spreadsheet id. ***(str)***
- ```sheet_name``` (optional): worksheet name. The default value is ```'Sheet1'```. ***(str)***
- ```range_from``` (optional): the begining of the range of data from sheet to update. The default value is ```'A'```. ***(str)***
- ```range_to``` (optional):  the end of the range of data from sheet to update. The default value is ```'Z'```. ***(str)***

	```python
	sheet_utils.update_data(
	    data=new_df,
	    sheet_id='my-sheet-id',
	    range_from='A4',
	    range_to='E7',
	)
	```

##### 2.9 ```remove_data```
To remove data from specific range of the given sheet, using ```remove_data``` method, it has three parameters:
- ```sheet_id``` (required): spreadsheet id. ***(str)***
- ```sheet_name``` (optional): worksheet name. The default value is ```'Sheet1'```. ***(str)***
- ```list_range``` (optional): list of data ranges to remove. The default value is ```['A1:Z1', 'A4:Z4']```. ***(list)***

	```python
	sheet_utils.remove_data(
	    sheet_id='my-sheet-id',
	    list_range=[
	        'A2:D5',
	        'E5:G6',
	    ],
	)
	```

---

#### MinIO

MinIO is an object storage, it is API compatible with the Amazon S3 cloud storage service. MinIO can be used as a **datalake** to store unstructured data (photos, videos, log files, backups, and container images) and structured data.

***Use case:*** when need to store raw data or get raw data from datalake. Notes that the stored data extension must be ```.parquet``` .

***Notes about how to determine the*** ```file_path``` ***parameter in minIO when using this module:***

![minIO file path](https://lh3.googleusercontent.com/drive-viewer/AK7aPaCoN6qQ0K5BuEHT_7c0CznHRpJu2LpxyqTpIY9_lNVOk7f_eB9kAVx_wl6iiOB9ia9vbiSJ6WtmvRXX6FDb8g7VU8Sy=s1600)

> For example, if the directory to the data file in minIO is as above, then the ```file_path``` is ```"/scraping/amazon_vendor/avc_bulk_buy_request/2023/9/24/batch_1695525619"``` (after removing bucket name, data storage mode, and data file extension).


***Functional:*** 

##### 3.1 initialize
Firstly, import minIO utils module class.

```python
from sop_deutils.datalake.y4a_minio import MinioUtils

minio_utils = MinioUtils()
```

##### 3.2 ```data_exist```
To check whether data exists in a storage directory, using ```data_exist``` method, it has three parameters:
- ```mode``` (required): the data storage mode, the value must be either ```'prod'``` or ```'stag'```. ***(str)***
- ```file_path``` (required): the data directory to check. ***(str)***
- ```bucket_name``` (optional): the name of the bucket to check. The default value is ```'sop-bucket'```. ***(str)***
	
	The method will return ```True``` if data exists otherwise ```False```.

	```python
	minio_utils.data_exist(
	    mode='stag',
	    file_path='your-data-path',
	)
	```
	Output:
	```bash
	True
	```

##### 3.3 ```get_data_value_exist```
To get the distinct values of a specified column of data in a data directory, using ```get_data_value_exist``` method, it has four parameters:
- ```mode``` (required): the data storage mode, the value must be either ```'prod'``` or ```'stag'```. ***(str)***
- ```file_path``` (required): the data directory to get distinct values. ***(str)***
- ```column_key``` (required): the column name to get distinct values. ***(str)***
- ```bucket_name``` (optional): the name of the bucket to get distinct values.  The default value is ```'sop-bucket'```. ***(str)***

	The method will return list of distinct values.

	```python
	minio_utils.get_data_value_exist(
	    mode='stag',
	    file_path='your-data-path',
	    column_key='your-chosen-column',
	)
	```
	Output:
	```bash
	['value_1', 'value_2']
	```

##### 3.4 ```load_data```
To load data from dataframe to storage, using ```load_data``` method, it has four parameters:
- ```data``` (required): dataframe contains data to load. ***(pd.DataFrame)***
- ```mode``` (required): the data storage mode, the value must be either ```'prod'``` or ```'stag'```. ***(str)***
- ```file_path``` (required): the directory to load the data. ***(str)***
- ```bucket_name``` (optional): the name of the bucket to load the data.  The default value is ```'sop-bucket'```. ***(str)***

	```python
	minio_utils.load_data(
	    data=df,
	    mode='stag',
	    file_path='your-data-path',
	)
	```

##### 3.5 ```get_data```
To get data from a single file of directory of storage, using ```get_data``` method, it has three parameters:
- ```mode``` (required): the data storage mode, the value must be either ```'prod'``` or ```'stag'```. ***(str)***
- ```file_path``` (required): the data directory to get data. ***(str)***
- ```bucket_name``` (optional): the name of the bucket to get data.  The default value is ```'sop-bucket'```. ***(str)***

	The method will return dataframe contains data to get.

	```python
	df = minio_utils.get_data(
	    mode='stag',
	    file_path='your-data-path',
	)

	print(df)
	```
	Output:
	```bash
	| Column1 Header | Column2 Header | Column3 Header |
	| ---------------| ---------------| ---------------|
	| Row1 Value1    | Row1 Value2    | Row1 Value3    |
	| Row2 Value1    | Row2 Value2    | Row2 Value3    |
	| Row3 Value1    | Row3 Value2    | Row3 Value3    |
	```

##### 3.6 ```get_data_wildcard```
To get data from multiple files of directories of storage,  using ```get_data_wildcard``` method, it has three parameters:
- ```mode``` (required): the data storage mode, the value must be either ```'prod'``` or ```'stag'```. ***(str)***
- ```file_path``` (required): the parent data directory to get the data. ***(str)***
- ```bucket_name``` (optional): the name of the bucket to get data.  The default value is ```'sop-bucket'```. ***(str)***

	The method will return dataframe contains data to get.

	```python
	df = minio_utils.get_data_wildcard(
	    mode='stag',
	    file_path='your-parent-data-path',
	)

	print(df)
	```
	Output:
	```bash
	| Column1 Header | Column2 Header | Column3 Header |
	| ---------------| ---------------| ---------------|
	| Row1 Value1    | Row1 Value2    | Row1 Value3    |
	| Row2 Value1    | Row2 Value2    | Row2 Value3    |
	| Row3 Value1    | Row3 Value2    | Row3 Value3    |
	```

---

#### PostgreSQL

***Use case:*** when interacting with Postgres database.

***Functional:***

##### 4.1 initialize
Firstly, import PostgreSQL utils module class. This class has four parameters:
- ```account_name```: the shortcode of client account name to connect to PostgreSQL. The value can be used as DA member name. The default value is ```None```. If not provide, must use params ```pg_account``` and ```pg_password```. List of account name can be found [here](https://docs.google.com/document/d/1jMouKkrJsqcGlxkgB1aJldGI-Osr3PYt3K1bwUM3I5c/edit?usp=sharing). ***(str)***
- ```pg_name```: PostgreSQL db name to connect. Accepted values are ```'raw_master'```, ```'raw_repl'```, ```'serving_master'```, ```'serving_repl'```. ***(str)***
- ```pg_account```: the client account to connect to PostgreSQL. The default value is ```None```. ***(str)***
- ```pg_password```: the client password to connect to PostgreSQL. The default value is ```None```. ***(str)***


	```python
	from sop_deutils.sql.y4a_postgresql import PostgreSQLUtils

	pg_utils = PostgreSQLUtils(
	    pg_name='serving_master',
	    account_name='user1',
	)

	# or

	pg_utils = PostgreSQLUtils(
	    pg_name='serving_master',
	    pg_account='y4a_sop_user1',
	    pg_password='password-of-user1',
	)

	# đều được
	```

##### 4.2 ```read_sql_file```
To get the SQL query given by SQL file, using ```read_sql_file``` method, it has one parameter:
- ```sql_file_path``` (required): the located path of SQL file. ***(str)***

	The method will return the string of SQL query.

	```python
	sql = pg_utils.read_sql_file(
	    sql_file_path='your-path/select_all.sql',
	)

	print(sql)
	```
	Output:
	```bash
	"SELECT * FROM your_schema.your_table"
	```	

##### 4.3 ```insert_data```
To insert data to PostgreSQL table, using ```insert_data``` method, it has six parameters:
- ```data``` (required): a dataframe contains data to insert. ***(pd.DataFrame)***
- ```schema``` (required): schema contains table to insert. ***(str)***
- ```table``` (required): table name to insert. ***(str)***
- ```ignore_errors``` (optional): whether to ignore errors when inserting data. The default value is ```False```. ***(bool)***
- ```commit_every``` (optional): number rows of data to commit each time. The default value is ```1000```. ***(int)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	```python
	pg_utils.insert_data(
	    data=your_df,
	    schema='your-schema',
	    table='your-table',
	)
	```

##### 4.4 ```bulk_insert_data```
To insert large data to PostgreSQL table, using ```bulk_insert_data``` method, it has five parameters:
- ```data``` (required): a dataframe contains data to insert. ***(pd.DataFrame)***
- ```schema``` (required): schema contains table to insert. ***(str)***
- ```table``` (required): table name to insert. ***(str)***
- ```commit_every``` (optional): number rows of data to commit each time. The default value is ```1000```. ***(int)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	```python
	pg_utils.bulk_insert_data(
	    data=your_df,
	    schema='your-schema',
	    table='your-table',
	)
	```

##### 4.5 ```upsert_data```
To upsert data to PostgreSQL table, using ```upsert_data``` method, it has six parameters:
- ```data``` (required): a dataframe contains data to upsert. Notes that if dataframe contains duplicated rows, it will be dropped. ***(pd.DataFrame)***
- ```schema``` (required): schema contains table to upsert. ***(str)***
- ```table``` (required): table name to upsert. ***(str)***
- ```where_conditions``` (optional): string of query that use conditions to update. The default value is ```None```. ***(str)***
- ```commit_every``` (optional): number rows of data to commit each time. The default value is ```1000```. ***(int)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	```python
	pg_utils.upsert_data(
	    data=your_df,
	    schema='your-schema',
	    table='your-table',
	)
	```

##### 4.6 ```bulk_upsert_data```
To upsert large data to PostgreSQL table, using ```bulk_upsert_data``` method, it has six parameters:
- ```data``` (required): a dataframe contains data to upsert. Notes that if dataframe contains duplicated rows, it will be dropped. ***(pd.DataFrame)***
- ```schema``` (required): schema contains table to upsert. ***(str)***
- ```table``` (required): table name to upsert. ***(str)***
- ```where_conditions``` (optional): string of query that use conditions to update. The default value is ```None```. ***(str)***
- ```commit_every``` (optional): number rows of data to commit each time. The default value is ```1000```. ***(int)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	```python
	pg_utils.bulk_upsert_data(
	    data=your_df,
	    schema='your-schema',
	    table='your-table',
	)
	```

##### 4.7 ```update_table```
To update new data of specific columns in the table based on primary keys, using ```update_table``` method, it has six parameters:
- ```data``` (required): a dataframe contains data to update, including primary keys and columns to update. ***(pd.DataFrame)***
- ```schema``` (required): schema contains table to update data. ***(str)***
- ```table``` (required): table to update data. ***(str)***
- ```columns``` (required): list of column names to update data. ***(list)***
- ```commit_every``` (optional): number rows of data to commit each time. The default value is ```1000```. ***(int)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	```python
	pg_utils.update_table(
	    data=your_df,
	    schema='your-schema',
	    table='your-table',
	    columns=['col1', 'col2'],
	)
	```

##### 4.8 ```get_data```
To get data from PostgreSQL database given by a SQL query, using ```get_data``` method, it has two parameters:
- ```sql``` (required): SQL query to get data. ***(str)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	The method will return dataframe contains data extracted by the given SQL query.

	```python
	df = pg_utils.get_data(
	    sql='your-query',
	)

	print(df)
	```
	Output:
	```bash
	| Column1 Header | Column2 Header | Column3 Header |
	| ---------------| ---------------| ---------------|
	| Row1 Value1    | Row1 Value2    | Row1 Value3    |
	| Row2 Value1    | Row2 Value2    | Row2 Value3    |
	| Row3 Value1    | Row3 Value2    | Row3 Value3    |
	```

##### 4.9 ```select_distinct```
To get the distinct values of a specified column in a PostgreSQL table, using ```select_distinct``` method, it has four parameters:
- ```col``` (required): column name to get the distinct data. ***(str)***
- ```schema``` (required): schema contains table to get data. ***(str)***
- ```table``` (required): table to get data. ***(str)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	The method will return list of distinct values.

	```python
	distinct_values = pg_utils.select_distinct(
	    col='chosen-column',
	    schema='your-schema',
	    table='your-table',
	)

	print(distinct_values)
	```
	Output:
	```bash
	['val1', 'val2', 'val3']
	```

##### 4.10 ```show_columns```
To get list of columns name of a specific PostgreSQL table, using ```show_columns``` method, it has three parameters:
- ```schema``` (required): schema contains table to get columns. ***(str)***
- ```table``` (required): table to get columns. ***(str)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	The method will return list of column names of the table.

	```python
	col_names = pg_utils.show_columns(
	    schema='your-schema',
	    table='your-table',
	)

	print(col_names)
	```
	Output:
	```bash
	['col1', 'col2', 'col3']
	```

##### 4.11 ```execute```
To execute the given SQL query, using ```execute``` method, it has three parameters:
- ```sql``` (required): SQL query to execute. ***(str)***
- ```fetch_output``` (optional): whether to fetch the results of the query. The default value is ```False```. ***(bool)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	The method will return list of query output if ```fetch_output``` is ```True```, otherwise ```None```.
	
	```python
	sql = """
	    UPDATE
	        sales_order_avc_di o,
	        (
	            SELECT
	                DISTINCT po_name, 
	                asin,
	                CASE
	                    WHEN o.status LIKE '%cancel%' AND a.status IS NULL THEN ''
	                    WHEN o.status LIKE '%cancel%' THEN CONCAT(a.status,' ',cancel_date) 
	                    ELSE o.status END po_asin_amazon_status
	            FROM
	                sales_order_avc_order_status o
	                LEFT JOIN
	                    sales_order_avc_order_asin_status a USING (updated_at, po_name)
	            WHERE updated_at > DATE_SUB(NOW(), INTERVAL 1 DAY)
	        ) s
	    SET
	        o.po_asin_amazon_status = s.po_asin_amazon_status
	    WHERE
	        o.po_name = s.po_name
	        AND o.asin = s.asin
	"""

	pg_utils.execute(
	    sql=sql,
	)
	```

##### 4.12 ```add_column```
To create new column for a specific PostgreSQL table, using ```add_column``` method, it has six parameters:
- ```schema``` (required): schema contains table to create column. ***(str)***
- ```table``` (required): table to create column. ***(str)***
- ```column_name``` (optional): name of the column to create available when creating single column. The default value is ```None``` ***(str)***
- ```dtype``` (optional): data type of the column to create available when creating single column. The default value is ```None``` ***(str)***
- ```muliple_columns``` (optional): dictionary contains columns name as key and data type of columns as value respectively. The default value is ```{}``` ***(dict)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	```python
	pg_utils.add_column(
	    schema='my-schema',
	    table='my-table',
	    muliple_columns={
	        'col1': 'int',
	        'col2': 'varchar(50)',
	    },
	)
	```

##### 4.13 ```create_table```
To create new table in PostgreSQL database, using ```create_table``` method, it has seven parameters:
- ```schema``` (required): schema contains table to create. ***(str)***
- ```table``` (required): table name to create. ***(str)***
- ```columns_with_dtype``` (required): dictionary contains column names as key and the data type of column as value respectively. ***(dict)***
- ```columns_primary_key``` (optional): list of columns to set primary keys. The default value is ```[]```. ***(list)***
- ```columns_not_null``` (optional): list of columns to set constraints not null. The default value is ```[]```.  ***(list)***
- ```columns_with_default``` (optional): dictionary contains column names as key and the default value of column as value respectively. The default value is ```{}```. ***(dict)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	```python
	pg_utils.create_table(
	    schema='my-schema',
	    table='my-new-table',
	    columns_with_dtype={
	        'col1': 'int',
	        'col2': 'varchar(50)',
	        'col3': 'varchar(10)',
	    },
	    columns_primary_key=[
	        'col1',
	    ],
	    columns_not_null=[
	        'col2',
	    ],
	    columns_with_default={
	        'col3': 'USA',
	    },
	)
	```

##### 4.14 ```grant_table```
To grant table privileges to users in PostgreSQL, using ```grant_table``` method, it has five parameters:
- ```schema``` (required): schema contains table to grant. ***(str)***
- ```table``` (required): table name to grant. ***(str)***
- ```list_users``` (required): list of users to grant. If want to grant for all members of DA team, provide ```['da']```. ***(list)***
- ```privileges``` (optional): list of privileges to grant. The default value is ```['SELECT']```. The accepted values in privileges list are ```'SELECT'```, ```'INSERT'```, ```'UPDATE'```, ```'DELETE'```, ```'TRUNCATE'```, ```'REFERENCES'```, ```'TRIGGER'```. ***(list)***
- ```all_privileges``` (optional): whether to grant all privileges. The default value is ```False```.  ***(bool)***

**THIS METHOD IS TEMPORARY UNAVAILABLE NOW**

	```python
	pg_utils.grant_table(
	    schema='my-schema',
	    table='my-new-table',
	    list_users=[
	        'linhvk',
	        'trieuna',
	    ],
	    privileges=[
	        'SELECT',
	        'INSERT',
	        'UPDATE',
	    ],
	)
	```

##### 4.15 ```truncate_table```
To remove all the data of PostgreSQL table, using ```truncate_table``` method, it has four parameters:
- ```schema``` (required): schema contains table to truncate. ***(str)***
- ```table``` (required): table name to truncate. ***(str)***
- ```reset_identity``` (optional): whether to reset identity of the table. The defaults value is ```False```. ***(bool)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	```python
	pg_utils.truncate_table(
	    schema='my-schema',
	    table='my-table',
	)
	```

##### 4.16 ```table_exists```
To check if the PostgreSQL table exists in database, using ```table_exists``` method, it has three parameters:
- ```schema``` (required): schema contains table to check. ***(str)***
- ```table``` (required): table name to check. ***(str)***
- ```db_pool_conn``` (optional): connection pool to connect to database. The default value is ```None```. If the value is ```None```, a new connection will be created and automatically closed after being used.  ***(callable)***

	The method will return ```True``` if table exists and ```False``` if not.

	```python
	pg_utils.table_exists(
	    schema='my-schema',
	    table='my-exists-table',
	)
	```
	Output:
	```bash
	True
	```

---

#### Telegram

***Use case:*** when need to send messages to Telegram by using bot

***Functional:***

To send messages to Telegram, using ```send_message``` method, it has three parameters:
- ```text``` (required): message to send. ***(str)***
- ```bot_token``` (optional): token of the bot which send the message. The default value is ```None```. If the value is ```None```, the bot ```sleep at 9pm``` will be used to send messages. ***(str)***
- ```chat_id``` (optional): id of group chat where the message is sent. The default value is ```None```. If the value is ```None```, the group chat ```Airflow Status Alert``` will be used.  ***(str)***

	```python
	from sop_deutils.y4a_telegram import send_message

	send_message(
	    text='Hello liuliukiki'
	)
	```

---

#### All in one (DAConfig)

***Use case:*** so far, there are a lot of platforms that needs to access frequently, in order not to import lots of modules, users can inherit all of above modules as simplest way.

***Functional:***

Firstly, import ```DAConfig``` class. This class requires one parameters:
- ```account_name```: the client account name to access platforms. The value can be used as DA member name. List of account name can be found [here](https://docs.google.com/document/d/1jMouKkrJsqcGlxkgB1aJldGI-Osr3PYt3K1bwUM3I5c/edit?usp=sharing). ***(str)***

	```python
	from sop_deutils.base.y4a_da_cfg import DAConfig

	da_cfg = DAConfig(
	    account_name='your-account-name',
	)
	```

This class will have its attributes as all above modules (PostgreSQL, MinIO, Google API, Airflow, Telegram) that users don't need to import and config to connect individually to each platform, each platform attributes will have the its own methods that listed above. List of attributes are:
- ```minio_utils``` 
- ```pg_raw_r_utils``` (connected to PostgreSQL raw read - repl)
- ```pg_raw_w_utils``` (connected to PostgreSQL raw write - master)
- ```pg_serving_r_utils``` (connected to PostgreSQL serving read - repl)
- ```pg_serving_w_utils``` (connected to PostgreSQL serving write - master)
- ```sheet_utils```

	```python
	print(da_cfg.minio_utils)
	print(da_cfg.pg_raw_r_utils)
	print(da_cfg.pg_raw_w_utils)
	print(da_cfg.pg_serving_r_utils)
	print(da_cfg.pg_serving_w_utils)
	print(da_cfg.sheet_utils)
	```

	Output:
	```bash
	<sop_deutils.datalake.y4a_minio.MinioUtils object at 0x7fe6e704d6f0>
	<sop_deutils.sql.y4a_postgresql.PostgreSQLUtils object at 0x7fe6e704d9f0>
	<sop_deutils.sql.y4a_postgresql.PostgreSQLUtils object at 0x7fe6e704dae0>
	<sop_deutils.sql.y4a_postgresql.PostgreSQLUtils object at 0x7fe6e704e170>
	<sop_deutils.sql.y4a_postgresql.PostgreSQLUtils object at 0x7fe6e704e0b0>
	<sop_deutils.gg_api.y4a_sheet.GGSheetUtils object at 0x7fe72c65e1d0>
	```

---

### Workflow example

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
import pandas as pd
from sop_deutils.y4a_airflow import auto_dag_id, telegram_alert
from sop_deutils.base.y4a_da_cfg import DAConfig

owner = 'linhvu'

cfg = DAConfig(owner)

default_args = {
    "retries":  20,			# number times to retry when the task is failed
    "retry_delay": timedelta(minutes=7),			# time delay among retries
    "start_date": datetime(2023, 7, 14, 0, 0, 0),			# date that the DAG start to run 
    "owner": owner,			# account name of DAG owner
    "on_failure_callback": telegram_alert,			# this contains function to alert to Telegram when the DAG/task is failed
    "execution_timeout": timedelta(hours=4),			# limit time the DAG run
}
dag = DAG(
    dag_id=auto_dag_id(),			# this contains function to name the DAG based on the file directory
    description='Sample DAG',			# description about the DAG
    default_args=default_args,			# default arguments contains dictionary of predefined params above
    catchup=False,			# If True, the DAG will backfill tasks from the start_date to current date
)

with dag:
    @task
    def create_spreadsheet():
        spread_sheet_id = cfg.sheet_utils.create_spread_sheet(
            sheet_name='test_sheet_231020',
            share_to=['longnc@yes4all.com'],
        )

        return spread_sheet_id
    
    @task
    def insert_data_spreadsheet(spread_sheet_id):
        df = pd.DataFrame(
            [[1, 2, 3, 4]]*20,
            columns=['col1', 'col2', 'col3', 'col4']
        )

        cfg.sheet_utils.insert_data(
            data=df,
            sheet_id=spread_sheet_id,
            from_row_index=1,
            insert_column_names=True,
        )
    
    @task
    def process_data_spreadsheet(spread_sheet_id):
        cfg.sheet_utils.remove_data(
            sheet_id=spread_sheet_id,
            list_range=[
                'A3:D3',
                'A15:D15',
            ],
        )
    
    @task
    def etl_from_sheet_to_db(spread_sheet_id):
        df_from_sheet = cfg.sheet_utils.get_data(
            sheet_id=spread_sheet_id,
            columns_first_row=True,
        )

        df_from_sheet['total'] = df_from_sheet['col1'] + df_from_sheet['col2']\
            + df_from_sheet['col3'] + df_from_sheet['col4']
        df_from_sheet.dropna(inplace=True)
        for col in df_from_sheet.columns:
            df_from_sheet[col] = df_from_sheet[col].astype('int')
        
        cfg.pg_serving_w_utils.create_table(
            schema='y4a_sop_analyst',
            table='test_231020',
            columns_with_dtype={
                'col1': 'int',
                'col2': 'int',
                'col3': 'int',
                'col4': 'int',
                'total': 'int',
            },
        )

        cfg.pg_serving_w_utils.insert_data(
            data=df_from_sheet,
            schema='y4a_sop_analyst',
            table='test_231020',
        )
    
    @task
    def execute_query():
        df_from_db = cfg.pg_serving_r_utils.get_data(
            sql='SELECT * FROM y4a_sop_analyst.test_231020',
        )
        print(df_from_db)

        cfg.pg_serving_w_utils.execute(
            sql='TRUNCATE TABLE y4a_sop_analyst.test_231020',
        )

    spread_sheet_id = create_spreadsheet()

    insert_data_spreadsheet(spread_sheet_id) \
        >> process_data_spreadsheet(spread_sheet_id) \
            >>  etl_from_sheet_to_db(spread_sheet_id) \
                >> execute_query()
```

---

> provided by ```liuliukiki```

> and special thank to ```duiikha``` for contributing api method to get and secure account credentials.

---
