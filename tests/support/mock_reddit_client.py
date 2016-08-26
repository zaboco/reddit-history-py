from itertools import takewhile

class MockRedditClient:
  def __init__(self, submissions):
    self.submissions = submissions

  def get_submissions(self, limit=0, before=None):
    if before:
      return list(takewhile(lambda s: s != before, self.submissions))
    else:
      return self.submissions[:limit]
