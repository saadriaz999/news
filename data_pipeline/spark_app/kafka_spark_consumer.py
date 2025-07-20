from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType

spark = SparkSession.builder \
    .appName("KafkaNewsConsumer") \
    .master("local[*]") \
    .getOrCreate()

schema = StructType() \
    .add("title", StringType()) \
    .add("content", StringType()) \
    .add("source", StringType()) \
    .add("published_at", StringType()) \
    .add("pushed_at", StringType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "raw_news") \
    .option("startingOffsets", "earliest") \
    .option("kafka.group.id", "spark-news-consumer-group") \
    .load()

parsed = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

query = parsed.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
