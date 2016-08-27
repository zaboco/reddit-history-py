import sys
import time

from pymongo import MongoClient

from fetch.http_reddit_client import HttpRedditClient
from fetch.mappers import map_submission, map_comment
from fetch.reddit_descriptors import submissions_descriptor, comments_descriptor
from fetch.reddit_history import RedditHistory


REDDIT_USER_AGENT = 'reddit-feed-py (by /u/zaboco)'
SUBREDDIT_NAME = 'python+javascript'


def build_reddit_history(reddit_descriptor, data_mapper, data_store):
  reddit_client = HttpRedditClient(REDDIT_USER_AGENT, SUBREDDIT_NAME, reddit_descriptor)
  return RedditHistory(data_store=data_store, reddit_client=reddit_client, item_mapper=data_mapper)


mongo_client = MongoClient()
data_store = mongo_client.reddit_history.entries
submissions_history = build_reddit_history(submissions_descriptor, map_submission, data_store)
comments_history = build_reddit_history(comments_descriptor, map_comment, data_store)

while True:
  try:
    print 'Fetching data from Reddit API...'
    submissions_count = submissions_history.store_latest()
    comments_count = comments_history.store_latest()
    print 'Stored: %d submissions, %d comments\n' % (submissions_count, comments_count)
    time.sleep(2)
  except KeyboardInterrupt:
    print '\nQuiting...'
    mongo_client.close()
    sys.exit(0)
