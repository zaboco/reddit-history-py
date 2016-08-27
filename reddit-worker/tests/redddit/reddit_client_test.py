from types import UnicodeType
from unittest import TestCase

SUBMISSION_FIELD_TYPES = {
  'title': UnicodeType,
  'name': UnicodeType,
  'author': UnicodeType,
  'created_utc': float,
  'score': int,
  'permalink': UnicodeType,
  'subreddit': UnicodeType
}

COMMENT_FIELD_TYPES = {
  'body': UnicodeType,
  'name': UnicodeType,
  'author': UnicodeType,
  'created_utc': float,
  'score': int,
  'link_id': UnicodeType,
  'subreddit': UnicodeType
}


class Base:
  class RedditClientTest(TestCase):
    @staticmethod
    def make_client(): raise NotImplementedError()

    @staticmethod
    def item_schema(): raise NotImplementedError()

    def setUp(self):
      self.client = self.make_client()

    def test_can_fetch_multiple_submissions(self):
      submissions = self.client.get_items(limit=2)
      self.assertEqual(len(submissions), 2)

    def test_new_submission_contains_required_fields(self):
      submission = self.__get_first_submission()
      self.assertValidSchema(submission)

    def test_can_fetch_submissions_before(self):
      first, second = self.client.get_items(limit=2)
      submissions_before_second = self.client.get_items(before=second)
      self.assertListEqual(submissions_before_second, [first])

    def test_returns_empty_list_if_nothing_before(self):
      [first] = self.client.get_items(limit=1)
      submissions_before_first = self.client.get_items(before=first)
      self.assertListEqual(submissions_before_first, [])

    def assertValidSchema(self, object):
      self.assertSetEqual(set(object.keys()), set(self.item_schema().keys()))
      for field, type in self.item_schema().items():
        self.assertIsInstance(object[field], type)

    def __get_first_submission(self):
      return self.client.get_items(limit=1)[0]

    def __get_first_comment(self):
      return self.client.get_comments(limit=1)[0]
