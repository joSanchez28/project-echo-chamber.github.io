from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min

from pyspark.sql import SparkSession
from pyspark import SparkContext

# Necessary in my case when submitting script to the cluster with the nltk and
# six egg files
import sys
sys.path.append("/home/kamdar")

# Import vader sentiment intensity analyzer.
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

print("nltk import works")

# Initializing spark environnment
spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext
sqlc = SQLContext(sc)

# Defina analyzer
analyzer = SentimentIntensityAnalyzer()
print("analyzer defined")

# Obtain the dataset
df_spark = spark.read.parquet("hdfs:///user/kamdar/full_reduced_dataset_2016.parquet")
print("parquet file read")

# Necessary to define udfs (user defined functions) in order to append columns
# to a spark dataframe
sentiment_pos = udf(lambda x: analyzer.polarity_scores(x)['pos'])
sentiment_neg = udf(lambda x: analyzer.polarity_scores(x)['neg'])
sentiment_neut = udf(lambda x: analyzer.polarity_scores(x)['neu'])
sentiment_compound = udf(lambda x: analyzer.polarity_scores(x)['compound'])
print("udf functions defined")

# Perform sentiment analysis and append results to the dataframe
df_spark = df_spark.withColumn('pos_sent',sentiment_pos(df_spark.body))
df_spark = df_spark.withColumn('neg_sent',sentiment_neg(df_spark.body))
df_spark = df_spark.withColumn('neut_sent',sentiment_neut(df_spark.body))
df_spark = df_spark.withColumn('compound_sent',sentiment_compound(df_spark.body))
print("sentiment columns added")

# Save the resulting dataset to a parquet file
df_spark.write.mode('overwrite').parquet("full_reduced_sentiment_dataset_2016.parquet")
print("parquet saved")
