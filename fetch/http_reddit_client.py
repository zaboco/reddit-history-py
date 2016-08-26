import requests

REDDIT_API_URL = 'https://api.reddit.com/r/'


class HttpRedditClient:
  def __init__(self, user_agent, subreddit, descriptor):
    base_url = REDDIT_API_URL + subreddit
    headers = {'user-agent': user_agent}
    self.client = HttpClient(base_url, headers)
    self.descriptor = descriptor

  def get_items(self, limit=100, before=None):
    before = before['name'] if before else None
    response = self.client.get(self.descriptor.url, params={'limit': limit, 'before': before})
    return map(self.descriptor.extract_from_response, response['data']['children'])


class HttpClient:
  def __init__(self, base_url, headers=None):
    self.base_url = base_url
    self.headers = headers

  def get(self, endpoint, params=None):
    return requests.get(self.base_url + endpoint, params=params, headers=self.headers).json()
