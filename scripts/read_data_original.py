from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql import SparkSession
from pyspark import SparkContext
'''
Script functionality:
With this script we obtain a parquet file containing all data from 2016 and 2017
'''

spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext

sqlc = SQLContext(sc)

# features to keep
to_keep = ['author', 'subreddit_id', 'body', 'created_utc', 'score', 'controversiality', 'gilded', 'post_id', 'parent_id', 'link_id']

# 2016
df_2016 = sqlc.read.json('hdfs:///datasets/reddit_data/2016/RC_2016-*.bz2')

df_2016_reduced = df_2016.select(*to_keep)

df_2016_reduced.write.mode('overwrite').parquet("full_dataset_2016.parquet")

# 2017
df_2017 = sqlc.read.json('hdfs:///datasets/reddit_data/2017/RC_2017-*.bz2')

df_2017_reduced = df_2017.select(*to_keep)

df_2017_reduced.write.mode('overwrite').parquet("full_dataset_2017.parquet")

# union
df_final = df_2016_reduced.union(df_2017_reduced)

df_final.write.mode('overwrite').parquet("full_reduced_dataset.parquet")
