from types import UnicodeType
from unittest import TestCase
from fetch.praw_client import PrawClient

SUBREDDIT_NAME = 'python'

SUBMISSION_FIELD_TYPES = {
  'title': UnicodeType,
  'name': UnicodeType,
  'author': UnicodeType,
  'created_utc': float,
  'score': int,
  'url': UnicodeType,
  'subreddit': UnicodeType
}

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
    expected_fields = set(SUBMISSION_FIELD_TYPES.keys())
    submission = next(self.client.get_submissions(limit=1))
    self.assertSetEqual(set(submission.keys()), expected_fields)

  def test_new_submission_fields_have_the_right_types(self):
    submission = next(self.client.get_submissions(limit=1))
    for field, type in SUBMISSION_FIELD_TYPES.items():
      self.assertIsInstance(submission[field], type)
