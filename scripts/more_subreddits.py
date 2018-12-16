from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql.functions import lit
from pyspark.sql.functions import rand
from pyspark.sql import SparkSession
from pyspark import SparkContext


spark = SparkSession.builder.getOrCreate()
spark.conf.set('spark.sql.session.timeZone', 'UTC')
sc = spark.sparkContext
sqlc = SQLContext(sc)

print('spark initialized')

df_spark = spark.read.parquet('full_reduced_sentiment_dataset_2016.parquet')
print('parquet read')

df_shuffle = df_spark.select('subreddit','id')

subreddits_to_keep = ["Libertarian", "Anarchism", "socialism", "progressive", \
                        "Conservative", "americanpirateparty", "democrats", \
                        "Liberal", "new_right", "Republican", "egalitarian", \
                        "demsocialist", "LibertarianLeft", "Liberty", "Anarcho_Capitalism", \
                        "alltheleft", "neoprogs", "tea_party", "voluntarism", "labor", \
                        "blackflag", "GreenParty", "democracy", "IIWW", "PirateParty", \
                        "Marxism", "piratenpartei", "Objectivism", "LibertarianSocialism", \
                        "peoplesparty", "Capitalism", "Anarchist", "feminisms", "republicans", \
                        "Egalitarianism", "anarchafeminism", "Communist", "SocialDemocracy", \
                        "Postleftanarchism", "RadicalFeminism", "Anarcho", "Pacifism","conservatives",\
                        "republicanism"]

list_of_ids = df_shuffle.filter(df_shuffle.subreddit.isin(subreddits_to_keep)) \
                    .orderBy(rand()).select('id').rdd.map(lambda row: row[0]).collect()[0:1000000]

df_spark = df_spark.filter(df_spark.id.isin(list_of_ids)) \
                    .select('author','subreddit','score','controversiality','compound_sent')

df_spark.write.mode("overwrite").parquet('more_subreddits.parquet')
