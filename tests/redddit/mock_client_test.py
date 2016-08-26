from tests.redddit.reddit_client_test import Base
from tests.support.mock_reddit_client import MockRedditClient

class MockRedditClientTest(Base.RedditClientTest):
  @staticmethod
  def make_client():
    base_submission = {
      'title': u'sample submission',
      'author': u'me',
      'created_utc': 1472158286.0,
      'score': 10,
      'permalink': u'/r/subreddit/comments/4zibaf/title/',
      'subreddit': u'subreddit'
    }
    return MockRedditClient([
      dict(base_submission, name=u'first'),
      dict(base_submission, name=u'second'),
      dict(base_submission, name=u'third')
    ])
