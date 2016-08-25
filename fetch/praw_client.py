from itertools import imap

import praw

class PrawClient:
  def __init__(self, user_agent, subreddit):
    praw_client = praw.Reddit(user_agent=user_agent)
    self.subreddit = praw_client.get_subreddit(subreddit)

  def get_submissions(self, limit):
    return imap(normalize_submission, self.subreddit.get_new(limit=limit))

def normalize_submission(submission):
  keys = ['title', 'name', 'author', 'created_utc', 'score', 'url', 'subreddit']
  return {key: submission.__dict__[key] for key in keys}
