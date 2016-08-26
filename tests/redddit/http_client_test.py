import os
from unittest import skipIf

from fetch.http_reddit_client import HttpRedditClient
from tests.redddit.reddit_client_test import Base

@skipIf(not os.environ.get('EXTERNAL_TEST'), 'external')
class HttpRedditClientTest(Base.RedditClientTest):
  @staticmethod
  def make_client():
    reddit_user_agent = '[test] reddit-feed-py (by /u/zaboco)'
    subreddit_name = 'python'
    return HttpRedditClient(user_agent=reddit_user_agent, subreddit=subreddit_name)
