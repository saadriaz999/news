from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StructType, StringType
import requests

# Django API URLs
DJANGO_SUMMARY_URL = "http://django:8000/articles/generate-summary/"
DJANGO_EMBEDDING_URL = "http://django:8000/articles/generate-embedding/"

# Create Spark session
spark = SparkSession.builder \
    .appName("KafkaNewsConsumer") \
    .master("local[*]") \
    .getOrCreate()

# Schema matches the new producer payload
schema = StructType() \
    .add("article_id", StringType()) \
    .add("pushed_at", StringType())

# Function to process each row (call Django APIs)
def process_article(article_id):
    if not article_id:
        return "Invalid ID"

    # Generate Summary
    try:
        summary_res = requests.post(DJANGO_SUMMARY_URL, json={"article_id": int(article_id)})
        if summary_res.status_code != 201:
            return f"Summary failed: {summary_res.text}"
    except Exception as e:
        return f"Summary exception: {str(e)}"

    # Generate Embedding
    try:
        embed_res = requests.post(DJANGO_EMBEDDING_URL, json={"article_id": int(article_id)})
        if embed_res.status_code != 201:
            return f"Embedding failed: {embed_res.text}"
    except Exception as e:
        return f"Embedding exception: {str(e)}"

    return f"Processed article_id={article_id}"

# Register as a UDF so Spark can call it
process_udf = udf(process_article, StringType())

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "raw_news") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .option("kafka.group.id", "spark-news-debug-group") \
    .load()

# Parse JSON payload
parsed = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Apply processing
processed = parsed.withColumn("result", process_udf(col("article_id")))

# Output to console (for debugging/logging)
query = processed.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
