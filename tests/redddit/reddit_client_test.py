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

class Base:
  class RedditClientTest(TestCase):
    @staticmethod
    def make_client():
      raise NotImplementedError()

    def setUp(self):
      self.client = self.make_client()

    def test_can_fetch_multiple_submissions(self):
      submissions = self.client.get_submissions(limit=2)
      self.assertEqual(len(submissions), 2)

    def test_new_submission_contains_required_fields(self):
      submission = self.__get_first_submission()
      self.assertSchema(submission, SUBMISSION_FIELD_TYPES)

    def test_can_fetch_submissions_before(self):
      first, second = self.client.get_submissions(limit=2)
      submissions_before_second = self.client.get_submissions(before=second)
      self.assertListEqual(submissions_before_second, [first])

    def assertSchema(self, object, schema):
      self.assertSetEqual(set(object.keys()), set(schema.keys()))
      for field, type in schema.items():
        self.assertIsInstance(object[field], type)

    def __get_first_submission(self):
      return self.client.get_submissions(limit=1)[0]