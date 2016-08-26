from tests.redddit.reddit_client_test import Base
from tests.support import fake
from tests.support.mock_reddit_client import MockRedditClient


class MockRedditClientTest(Base.RedditClientTest):
  @staticmethod
  def make_client():
    return MockRedditClient(map(fake.submission, [u'first', u'second', u'third']))

  def test_adds_submission_in_front(self):
    prev_submissions = self.client.get_submissions()
    new_submission = fake.submission(u'new')
    self.client.add_submission(new_submission)
    updated_submissions = self.client.get_submissions()
    self.assertListEqual(updated_submissions, [new_submission] + prev_submissions)
