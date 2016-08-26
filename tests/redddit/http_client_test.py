import os
from unittest import skipIf

from fetch.http_reddit_client import HttpRedditClient
from fetch.reddit_descriptors import submissions_descriptor, comments_descriptor
from tests.redddit.reddit_client_test import Base


REDDIT_USER_AGENT = '[test] reddit-feed-py (by /u/zaboco)'
SUBREDDIT_NAME = 'python'


@skipIf(not os.environ.get('EXTERNAL_TEST'), 'external')
class HttpSubmissionsClientTest(Base.RedditClientTest):
  @staticmethod
  def make_client():
    return HttpRedditClient(
      user_agent=REDDIT_USER_AGENT,
      subreddit=SUBREDDIT_NAME,
      descriptor=submissions_descriptor)

  @staticmethod
  def item_schema():
    return submissions_descriptor.item_schema


@skipIf(not os.environ.get('EXTERNAL_TEST'), 'external')
class HttpCommentsClientTest(Base.RedditClientTest):
  @staticmethod
  def make_client():
    return HttpRedditClient(
      user_agent=REDDIT_USER_AGENT,
      subreddit=SUBREDDIT_NAME,
      descriptor=comments_descriptor)

  @staticmethod
  def item_schema():
    return comments_descriptor.item_schema
