#!/bin/bash
spark-submit \
  --master local[*] \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 \
  --jars /opt/spark/jars/hadoop-client-api-3.3.2.jar,/opt/spark/jars/hadoop-client-runtime-3.3.2.jar,/opt/spark/jars/kafka-clients-3.3.2.jar \
  /opt/spark/app/kafka_spark_consumer.py



#manually downloading some spark jar files
#spark-submit \
#  --master local[*] \
#  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 \
#  --jars /opt/spark/jars/hadoop-client-api-3.3.2.jar,/opt/spark/jars/hadoop-client-runtime-3.3.2.jar,/opt/spark/jars/kafka-clients-3.3.2.jar \
#  /opt/spark/app/kafka_spark_consumer.py
