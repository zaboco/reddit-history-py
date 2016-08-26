from tests.redddit.reddit_client_test import Base
from tests.support.mock_reddit_client import MockRedditClient

class MockRedditClientTest(Base.RedditClientTest):
  @staticmethod
  def make_client():
    submissions = map(make_submission, [u'first', u'second', u'third'])
    return MockRedditClient(submissions)

  def test_adds_submission_in_front(self):
    new_submission = make_submission(u'new')
    prev_submissions = self.client.get_submissions()
    self.client.add_submission(new_submission)
    new_submissions = self.client.get_submissions()
    self.assertListEqual(new_submissions, [new_submission] + prev_submissions)


def make_submission(name):
  base_submission = {
    'title': u'sample submission',
    'author': u'me',
    'created_utc': 1472158286.0,
    'score': 10,
    'permalink': u'/r/subreddit/comments/4zibaf/title/',
    'subreddit': u'subreddit'
  }
  return dict(base_submission, name=name)
