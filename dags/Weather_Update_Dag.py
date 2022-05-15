from airflow import DAG
from datetime import datetime, timedelta
# from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.contrib.sensors.file_sensor import FileSensor

from collect_data import get_data


default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2022, 5, 15,6,00),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('Weather_Update_Dag',default_args=default_args,schedule_interval="0 6 * * *", template_searchpath=['/usr/local/airflow/sql_files'], catchup=False) as dag:

    t0 = PythonOperator(task_id='gather_data', python_callable=get_data)
    # t1=BashOperator(task_id='check_file_exists', bash_command='shasum ~/store_files_airflow/result_many_city.csv', retries=2, retry_delay=timedelta(seconds=15))
    t1 = FileSensor(
        task_id='check_file_exists',
        filepath='/usr/local/airflow/store_files_airflow/result_many_city.csv',
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=150,
        soft_fail=True
    )
    
    t3 = PostgresOperator(task_id='create_mysql_table', postgres_conn_id ="postgres_conn", sql="create_table.sql")

    t4 = PostgresOperator(task_id='insert_into_table', postgres_conn_id ="postgres_conn", sql="insert_into_table.sql")

    
    t0 >> t1 >> t3 >> t4
    
