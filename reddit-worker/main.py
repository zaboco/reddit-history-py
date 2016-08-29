import sys
import time

import yaml
from history.http_reddit_client import HttpRedditClient
from history.mappers import map_submission, map_comment
from history.reddit_descriptors import submissions_descriptor, comments_descriptor
from history.reddit_history import RedditHistory
from pymongo import MongoClient


with open('config.yml', 'r') as config_file:
  config = yaml.load(config_file)
  REDDIT_USER_AGENT = config['app']['reddit_user_agent']
  SUBREDDIT_NAME = '+'.join(config['app']['subreddits'])
  POOLING_INTERVAL = config['app']['pooling_interval']
  MONGO_CONFIG = config['mongo']


def build_reddit_history(reddit_descriptor, data_mapper, data_store):
  reddit_client = HttpRedditClient(REDDIT_USER_AGENT, SUBREDDIT_NAME, reddit_descriptor)
  return RedditHistory(data_store=data_store, reddit_client=reddit_client, item_mapper=data_mapper)


mongo_client = MongoClient(MONGO_CONFIG['host'], MONGO_CONFIG['port'])
data_store = mongo_client[MONGO_CONFIG['database']][MONGO_CONFIG['collection']]
submissions_history = build_reddit_history(submissions_descriptor, map_submission, data_store)
comments_history = build_reddit_history(comments_descriptor, map_comment, data_store)

print 'Monitoring %s each %d seconds' % (SUBREDDIT_NAME, POOLING_INTERVAL)
while True:
  try:
    print 'Fetching data from Reddit API...'
    submissions_count = submissions_history.store_latest()
    comments_count = comments_history.store_latest()
    print 'Stored: %d submissions, %d comments\n' % (submissions_count, comments_count)
    time.sleep(POOLING_INTERVAL)
  except KeyboardInterrupt:
    print '\nQuiting...'
    mongo_client.close()
    sys.exit(0)
