from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql import SparkSession
from pyspark import SparkContext

# Initializing spark environnment
spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext
sqlc = SQLContext(sc)
print('spark initialized')

# Read dataset
df = spark.read.parquet('hdfs:///user/kamdar/full_reduced_sentiment_dataset_2016.parquet')
print('dataframe read')

# Select columns
df = df.select('author','subreddit','id','body','created_utc','score','controversiality','pos_sent','neg_sent','neut_sent','compound_sent')
print('columns selected')

# Remove posts where the author or the body or both are deleted
df = df.filter('author != "[deleted]"').filter('body != "[deleted]"')
print('dataframe filtered 1')

# Obtain the subreddits removing AskReddit and counting, sorted by decreasing
# number of posts.
subreddits = df.select('subreddit','id').groupby('subreddit') \
                                        .agg(count('id').alias('number_of_posts')) \
                                        .filter('subreddit != "AskReddit"') \
                                        .filter('subreddit != "counting"') \
                                        .orderBy(desc('number_of_posts'))
print('subreddits')

# Save the subreddits
subreddits.write.mode("overwrite").parquet('subreddits_2016.parquet')
print('parquet 2 saved')

# Obtain in a list the names of the 200 most popular subreddits.
top_200_subbreddits = subreddits.select('subreddit').rdd.map(lambda row : row[0]).collect()[0:200]
print('top 200 subreddits')

# Select posts that were made in these subreddits
df = df.filter(df.subreddit.isin(top_200_subbreddits))
print('dataframe filtered 2')

# Save the posts from the 200 most popular subreddits.
df.write.mode("overwrite").parquet('filtered_dataset_2016.parquet')
print('parquet 3 saved')
