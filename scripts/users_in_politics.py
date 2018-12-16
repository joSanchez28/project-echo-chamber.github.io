from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql import SparkSession
from pyspark import SparkContext

# Initialize spark
spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext
sqlc = SQLContext(sc)
print('spark initialized')

# Read the datasets, where topics.parquet is the dataframe containing the manually
# added topics for each of the 200 most popular subreddits.
df = spark.read.parquet('final_dataset_2016_user_sampled.parquet')
subreddits_topic = spark.read.parquet('topics.parquet')
print('parquet read')

# Obtain subreddits entierly dedicated to politics.
subreddits_topic = subreddits_topic.filter('topic = "politics"')
print('filter politics')

# Obtain these subreddits in a list format
subreddits_politics = subreddits_topic.select('subreddit').rdd.map(lambda row: row[0]).collect()

# Get the users that posted in any of these 8 subreddits.
users_in_politics = df.filter(df.subreddit.isin(subreddits_politics)) \
                        .select('author','id') \
                        .groupby('author').agg(count('id').alias('number_of_posts')) \
                        .select('author').rdd.map(lambda row: row[0]).collect()

# Obtain the posts for eache of the users above.
df = df.filter(df.author.isin(users_in_politics))
print('filter')

# Save the parquet file.
df.write.mode("overwrite").parquet("final_dataset_2016_user_sampled_politics.parquet")
print('final parquet saved')
