from pymongo import MongoClient

from fetch.http_reddit_client import HttpRedditClient
from fetch.reddit_history import RedditHistory

client = MongoClient()
db = client.reddit_history

reddit_user_agent = 'reddit-feed-py (by /u/zaboco)'
subreddit_name = 'python'
http_reddit_client = HttpRedditClient(reddit_user_agent, subreddit_name)

history = RedditHistory(data_store=db.entries, reddit_client=http_reddit_client, start_with=5)
history.store_latest()
