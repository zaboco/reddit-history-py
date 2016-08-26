def submission(name):
  base_submission = {
    'title': u'sample submission',
    'author': u'me',
    'created_utc': 1472158286.0,
    'score': 10,
    'permalink': u'/r/subreddit/comments/4zibaf/title/',
    'subreddit': u'subreddit'
  }
  return dict(base_submission, name=name)
