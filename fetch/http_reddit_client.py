import requests

REDDIT_API_URL = 'https://api.reddit.com/r/'

class HttpRedditClient:
  def __init__(self, user_agent, subreddit, debug=False):
    base_url = REDDIT_API_URL + subreddit
    headers = {'user-agent': user_agent}
    self.client = HttpClient(base_url, headers)

  def get_submissions(self, limit=100, before=None):
    before = before['name'] if before else None
    response = self.client.get('/new.json', params={'limit': limit, 'before': before})
    return map(extract_submission, response['data']['children'])


def extract_submission(submission_data):
  submission = submission_data['data']
  keys = ['title', 'name', 'author', 'created_utc', 'score', 'url', 'subreddit']
  return {key: submission[key] for key in keys}


class HttpClient:
  def __init__(self, base_url, headers=None):
    self.base_url = base_url
    self.headers = headers

  def get(self, endpoint, params=None):
    return requests.get(self.base_url + endpoint, params=params, headers=self.headers).json()
