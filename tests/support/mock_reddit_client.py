from itertools import takewhile

from tests.support.fakes import make_submission


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
