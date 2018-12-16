from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql.functions import lit
from pyspark.sql import SparkSession
from pyspark import SparkContext

# Initialize spark
spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext
sqlc = SQLContext(sc)
print('spark initialized')

# Read dataset
df_spark = spark.read.parquet('full_reduced_sentiment_dataset_2016.parquet')
print('parquet read')

# Select appropriate columns
df_spark = df_spark.select('id','author','subreddit','body','score','controversiality','compound_sent')
print('columns selected')

# Obtain the comments of the 4 political subreddits
df_republican = df_spark.filter('subreddit = "Republican"')
df_conservative = df_spark.filter('subreddit = "Conservative"')
df_democrat = df_spark.filter('subreddit = "democrats"')
df_liberal = df_spark.filter('subreddit = "Liberal"')
print('subreddit filtered')

# Select the comments with the highest scores for each of the subreddits.
republican_post_ids = df_republican.orderBy(desc('score')).select('id').rdd.map(lambda row: row[0]).collect()[0:25000]
conservative_post_ids = df_conservative.orderBy(desc('score')).select('id').rdd.map(lambda row: row[0]).collect()[0:25000]
democrat_post_ids = df_democrat.orderBy(desc('score')).select('id').rdd.map(lambda row: row[0]).collect()[0:25000]
liberal_post_ids = df_liberal.orderBy(desc('score')).select('id').rdd.map(lambda row: row[0]).collect()[0:25000]
print('ids obtained')

df_republican = df_republican.filter(df_republican.id.isin(republican_post_ids))
df_conservative = df_conservative.filter(df_conservative.id.isin(conservative_post_ids))
df_democrat = df_democrat.filter(df_democrat.id.isin(democrat_post_ids))
df_liberal = df_liberal.filter(df_liberal.id.isin(liberal_post_ids))
print('top 25000 selected')

# Add a column with the appropriate label
df_republican = df_republican.withColumn('category',lit(1))
df_conservative = df_conservative.withColumn('category',lit(1))
df_democrat = df_democrat.withColumn('category',lit(-1))
df_liberal = df_liberal.withColumn('category',lit(-1))
print('data categorized')

# Merge everything into a single dataframe
df_final = df_republican.union(df_conservative)
df_final = df_final.union(df_democrat)
df_final = df_final.union(df_liberal)
print('final union')

# Save the training set
df_final.write.mode("overwrite").parquet('training_data.parquet')
print('parquet saved')
