def map_submission(submission):
  return {
    '_id': submission['name'],
    'text': submission['title'],
    'created_at': submission['created_utc'],
    'author': submission['author'],
    'score': submission['score'],
    'permalink': submission['permalink'],
    'subreddit': submission['subreddit'],
    'kind': 'submission'
  }
