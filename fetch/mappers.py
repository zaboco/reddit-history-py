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

def map_comment(comment):
  return {
    '_id': comment['name'],
    'text': comment['body'],
    'created_at': comment['created_utc'],
    'author': comment['author'],
    'score': comment['score'],
    'link_id': comment['link_id'],
    'subreddit': comment['subreddit'],
    'kind': 'comment'
  }
