from unittest import TestCase

from fetch.praw_client import PrawClient

SUBREDDIT_NAME = 'python'

class RedditClientTest(object):
  @staticmethod
  def make_client():
    raise NotImplementedError()

  def setUp(self):
    self.client = self.make_client()


class PrawTest(RedditClientTest, TestCase):
  @staticmethod
  def make_client():
    reddit_user_agent = '[test] reddit-feed-py (by /u/zaboco)'
    return PrawClient(user_agent=reddit_user_agent, subreddit=SUBREDDIT_NAME)

  def test_new_submission_contains_required_fields(self):
    expected_fields = {'title', 'name', 'author', 'created_utc', 'score', 'url', 'subreddit'}
    submission = next(self.client.get_submissions(limit=1))
    self.assertSetEqual(set(submission.keys()), expected_fields)
