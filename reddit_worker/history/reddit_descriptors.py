from types import UnicodeType


class __RedditDescriptor:
  def __init__(self, url, item_schema):
    self.url, self.item_schema = [url, item_schema]

  def extract_from_response(self, request_data):
    item = request_data['data']
    keys = self.item_schema.keys()
    return {key: item[key] for key in keys}


submissions_descriptor = __RedditDescriptor('/new.json', {
  'title': UnicodeType,
  'name': UnicodeType,
  'author': UnicodeType,
  'created_utc': float,
  'score': int,
  'permalink': UnicodeType,
  'subreddit': UnicodeType
})

comments_descriptor = __RedditDescriptor('/comments.json', {
  'body': UnicodeType,
  'name': UnicodeType,
  'author': UnicodeType,
  'created_utc': float,
  'score': int,
  'link_id': UnicodeType,
  'subreddit': UnicodeType
})
