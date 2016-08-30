import os
import signal
import sys
import time

import yaml

from data_db_info import get_db_info
from history.http_reddit_client import HttpRedditClient
from history.mappers import map_submission, map_comment
from history.reddit_descriptors import submissions_descriptor, comments_descriptor
from history.reddit_history import RedditHistory


REDDIT_USER_AGENT = 'reddit-feed-py (by /u/zaboco)'
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

with open('config.yml', 'r') as config_file:
  config = yaml.load(config_file)
  SUBREDDIT_NAME = '+'.join(config['app']['subreddits'])
  POOLING_INTERVAL = config['app']['pooling_interval']


def build_reddit_history(reddit_descriptor, data_mapper, data_store):
  reddit_client = HttpRedditClient(REDDIT_USER_AGENT, SUBREDDIT_NAME, reddit_descriptor)
  return RedditHistory(data_store=data_store, reddit_client=reddit_client, item_mapper=data_mapper)


data_store, mongo_client = get_db_info(MONGO_HOST, MONGO_DATABASE, MONGO_COLLECTION)
submissions_history = build_reddit_history(submissions_descriptor, map_submission, data_store)
comments_history = build_reddit_history(comments_descriptor, map_comment, data_store)


def cleanup_and_exit(_signum, _frame):
  print '\nQuiting...'
  mongo_client.close()
  sys.exit(0)


signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

print 'Monitoring %s each %d seconds' % (SUBREDDIT_NAME, POOLING_INTERVAL)
while True:
  print 'Fetching data from Reddit API...'
  submissions_count = submissions_history.store_latest()
  comments_count = comments_history.store_latest()
  print 'Stored: %d submissions, %d comments\n' % (submissions_count, comments_count)
  time.sleep(POOLING_INTERVAL)
