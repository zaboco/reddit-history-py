from tests.redddit.reddit_client_test import Base
from tests.support.mock_reddit_client import MockRedditClient


class MockRedditClientTest(Base.RedditClientTest):
  @staticmethod
  def make_client():
    return MockRedditClient([u'first', u'second', u'third'])

  def test_adds_submission_in_front(self):
    prev_submissions = self.client.get_submissions()
    new_submission = self.client.add_submission(u'new')
    updated_submissions = self.client.get_submissions()
    self.assertListEqual(updated_submissions, [new_submission] + prev_submissions)
