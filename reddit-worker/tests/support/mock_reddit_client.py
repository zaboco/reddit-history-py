from itertools import takewhile


class MockRedditClient:
  def __init__(self, items):
    self.items = items

  def get_items(self, limit=100, before=None):
    if before:
      return list(takewhile(lambda s: s != before, self.items))
    else:
      return self.items[:limit]

  def add_item(self, submission):
    self.items.insert(0, submission)
