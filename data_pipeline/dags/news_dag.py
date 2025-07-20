import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta


local_tz = pendulum.timezone("America/Chicago")
dynamic_start = pendulum.now(local_tz).subtract(minutes=1)

default_args = {
    'owner': 'news_pipeline',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='kafka_news_fetch_dag',
    default_args=default_args,
    start_date=dynamic_start,
    schedule_interval='* * * * *',
    catchup=False,
) as dag:

    fetch_and_send_news = BashOperator(
        task_id='fetch_news_to_kafka',
        bash_command='python /opt/airflow/kafka/news_producer.py'
    )

    fetch_and_send_news
