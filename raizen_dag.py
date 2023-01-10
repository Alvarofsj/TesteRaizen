from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import main

# Start Date - Um dia antes como padrao para inicio imediato
start_date = datetime.now() + timedelta(days=-1)

# Chama funcao principal
def call_raizen():
    
    main.main_call()
    
    return

# Cria DAG
with DAG("TesteRaizen", 
    start_date=start_date,
    schedule_interval="@daily",
    catchup=False) as dag:
    
    fuel_data = PythonOperator(
    task_id="get_fuel_data",
    python_callable=call_raizen
    )
