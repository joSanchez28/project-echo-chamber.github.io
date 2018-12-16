from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import lit

'''
Script functionality:
In order to filter and reduce even more the size of the datasets we dropped the
columns that mostly have no use for us, namely: author_flair_class,
author_flair_text, distinguished, edited, retrieved_on, stickied and
subreddit_id.
'''

spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext
sqlc = SQLContext(sc)

df_2016 = spark.read.parquet("sample2016.parquet")
to_drop = ['author_flair_css_class','author_flair_text','distinguished','edited','retrieved_on','stickied','subreddit_id']
df_2016_reduced = df_2016.drop(*to_drop)
df_2016_reduced.write.mode("overwrite").parquet("sampled_reduced_col_2016.parquet")
