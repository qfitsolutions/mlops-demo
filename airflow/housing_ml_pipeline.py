from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import mysql.connector
from sklearn.ensemble import RandomForestRegressor
import pickle

# MySQL connection details
MYSQL_CONN = {
    'host': 'localhost',
    'user': 'mluser',
    'password': 'mlpassword',
    'database': 'housing_db'
}

def extract_data(**kwargs):
    connection = mysql.connector.connect(**MYSQL_CONN)
    query = "SELECT * FROM housing_data"
    df = pd.read_sql(query, con=connection)
    df.to_csv('/tmp/raw_data.csv', index=False)
    connection.close()

def prepare_data():
    df = pd.read_csv('/tmp/raw_data.csv')
    X = df.drop(columns=['target', 'id'])
    y = df['target']
    X.to_csv('/tmp/X.csv', index=False)
    y.to_csv('/tmp/y.csv', index=False)

def train_model():
    X = pd.read_csv('/tmp/X.csv')
    y = pd.read_csv('/tmp/y.csv')
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    with open('/tmp/housing_model.pkl', 'wb') as file:
        pickle.dump(model, file)

default_args = {
    'owner': 'ravi',
    'start_date': datetime(2023, 1, 1),
    'retries': 1
}

dag = DAG(
    'housing_ml_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

prepare_task = PythonOperator(
    task_id='prepare_data',
    python_callable=prepare_data,
    dag=dag
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

extract_task >> prepare_task >> train_task