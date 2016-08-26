from itertools import takewhile


class MockRedditClient:
  def __init__(self, names):
    self.submissions = map(make_submission, names)

  def get_submissions(self, limit=100, before=None):
    if before:
      return list(takewhile(lambda s: s != before, self.submissions))
    else:
      return self.submissions[:limit]

  def add_submission(self, name):
    submission = make_submission(name)
    self.submissions.insert(0, submission)
    return submission


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
