from unittest import TestCase

from history.mappers import map_submission
from tests.support.fakes import make_submission


class MappersTest(TestCase):
  def test_submission_mapper(self):
    submission = make_submission(u'unique_name')
    mapped_submission = map_submission(submission)
    self.assertDictEqual(mapped_submission, {
      '_id': submission['name'],
      'text': submission['title'],
      'created_at': submission['created_utc'],
      'author': submission['author'],
      'score': submission['score'],
      'permalink': submission['permalink'],
      'subreddit': submission['subreddit'],
      'kind': 'submission'
    })
