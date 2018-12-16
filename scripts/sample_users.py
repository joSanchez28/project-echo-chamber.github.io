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

# Read dataset (contains posts of the 200 most popular subreddits)
df = spark.read.parquet('filtered_dataset_2016.parquet')

# Get all the users
users = df.select('author','id').groupby('author').agg(count('id').alias('number_of_posts'))
print('users')

# Sample from every user
sampling_ratio = 0.025
users_sampled = users.sample(False,sampling_ratio)
print('sampled users')

# Get a list of the name of all users
all_users = users_sampled.select('author').rdd.map(lambda row : row[0]).collect()
print('all users')

# Obtain the posts from those sampled users.
df = df.filter(df.author.isin(all_users))
print('final filter')

# Save the parquet file.
df.write.mode("overwrite").parquet('final_dataset_2016_user_sampled.parquet')
print('final parquet saved')
