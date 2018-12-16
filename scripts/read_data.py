from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import SQLContext
'''
Script functionality:
With this script we obtain a parquet file containing a sample (10% of the total)
of the sample obtained with the script "read_data_original.py". That is, 1% of
the 2016
'''

spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext

sqlc = SQLContext(sc)

df = spark.read.parquet("hdfs:///user/kamdar/data/sample2016.parquet")
df = df.sample(False,0.1)
df.write.mode("overwrite").parquet("sample2016_1.parquet")
