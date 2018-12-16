from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql import SparkSession
from pyspark import SparkContext

spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext
sqlc = SQLContext(sc)

print('spark initialized')

df = spark.read.parquet('final_dataset_2016_user_sampled_2.parquet')

get_len = udf(lambda x: len(x))

df = df.withColumn('post_length', get_len(df.body)).filter('post_length > 2')

df.write.mode("overwrite").parquet('final_dataset_2016_user_sampled_post_filtered.parquet')
