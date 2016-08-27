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


def make_reddit_item(name):
  return dict(name=name)


def map_reddit_item(item):
  return dict(_id=item['name'])
