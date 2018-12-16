# Imports working with the cluster
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import lit
import pyspark.sql.functions as F

'''
Script functionality:
With this script we have obtained the stats we talk present in the notebook.
(Every query is explained with comments)
'''

# Spark configurations
spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext

sqlc = SQLContext(sc)

# Read a 10% sample of the 2016 reddit comments
df_spark = spark.read.parquet("sampled_reduced_col_2016.parquet")

# Text file to write down the stats (create empty stats.txt file first)
f = open('/home/kamdar/stats.txt','w+')

# STATS ON THE DATASET

# Total number of comments
total_n_comments = df_spark.count()
print("Total number of comments: {}".format(str(total_n_comments)))
f.write("Total number of comments: {} \n".format(str(total_n_comments)))

# Number of deleted comments (body of comment == '[deleted]')
n_deleted_comments = df_spark.filter('body = "[deleted]"').count()
print("Number of deleted comments: {}".format(str(n_deleted_comments)))
f.write("Number of deleted comments: {} \n".format(str(n_deleted_comments)))

# Percentage of comments that are deleted
percentage_deleted_comments = 100 * n_deleted_comments  / total_n_comments
print("% of deleted comments: {}".format(str(percentage_deleted_comments)))
f.write("% of deleted comments: {} \n".format(str(percentage_deleted_comments)))

# Number of comments removed by users (author == '[deleted]')
comments_by_removed_users = df_spark.filter('author = "[deleted]"').count()
print("Number of comments by removed users: {}".format(str(comments_by_removed_users)))
f.write("Number of comments by removed users: {} \n".format(str(comments_by_removed_users)))

# Percentage of comments that are deleted by users
percentage_by_dl_user = 100 * comments_by_removed_users / total_n_comments
print("% comments by deleted users: {}".format(str(percentage_by_dl_user)))
f.write("% comments by deleted users: {} \n".format(str(percentage_by_dl_user)))

# Number of controversial comments (see Milestone 2.ipynb for definition of controversial comment)
n_controversial_comments = df_spark.filter('controversiality = 1').count()
print("Number of controversial comments: {}".format(str(n_controversial_comments)))
f.write("Number of controversial comments: {} \n".format(str(n_controversial_comments)))

# Percentage of comments that are controversial
perc_controversial_comments = 100 * n_controversial_comments / total_n_comments
print("% of controversial comments: {}".format(str(perc_controversial_comments)))
f.write("% of controversial comments: {} \n".format(str(perc_controversial_comments)))

# Number of subreddits
total_n_subreddits = df_spark[['subreddit']].distinct().count()
print("Number of subreddits: {}".format(str(total_n_subreddits)))
f.write("Number of subreddits: {}".format(str(total_n_subreddits)))

# Close stats.txt
f.close()

# FILTERS ON THE DATASET

# Number of comments per subreddit
df_subreddit_count = df_spark.groupBy('subreddit').agg(count('*')).select('*',F.col('count(1)').alias('Number of comments')).drop('count(1)')#.withColumnRenamed('count(1)', 'Number of comments')
df_subreddit_count.write.mode("overwrite").parquet("df_subreddit_count.parquet")

# Number of controversial comments per subreddit
df_controversial_per_subr_count = df_spark.filter('controversiality = 1').groupBy('subreddit').agg(count('*')).select('*',F.col('count(1)').alias('N_controversial_comments')).drop('count(1)')#.withColumnRenamed('count(1)', 'N controversial comments')
df_controversial_per_subr_count.write.mode("overwrite").parquet("df_controversial_per_subr_count.parquet")

# Just the comments creation 'timestamp' column in dataframe (sorted)
df_created_utc = df_spark[['created_utc','controversiality']]#.orderBy(asc('created_utc'))
df_created_utc_controversial = df_created_utc.filter("controversiality = 1")
df_created_utc_non_controversial = df_created_utc.filter("controversiality = 0")

df_created_utc_controversial = df_created_utc_controversial.withColumn("month",F.from_unixtime(df_created_utc_controversial.created_utc,'MM')).drop('created_utc').groupby("month").count()
df_created_utc_non_controversial = df_created_utc_non_controversial.withColumn("month",F.from_unixtime(df_created_utc_non_controversial.created_utc,'MM')).drop('created_utc').groupby("month").count()


df_created_utc_controversial.write.mode("overwrite").parquet("df_created_utc_controversial.parquet")
df_created_utc_non_controversial.write.mode("overwrite").parquet("df_created_utc_non_controversial.parquet")
