import csv
import pandas as pd
from clean_tweet import clean_tweet
from util import listify

@listify
def read_data(tweet_file_location):
	tweets = open(tweet_file_location,'rt')
	reader = csv.reader(tweets)
	for each_row in reader:
		sentiment = each_row[0]
		preprocess_tweet = clean_tweet(each_row[5].lower())
		yield list(preprocess_tweet)
