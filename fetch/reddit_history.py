from fetch.mappers import map_submission


class RedditHistory:
  def __init__(self, reddit_client, data_store, start_with):
    self.reddit_client, self.data_store, self.start_with = [reddit_client, data_store, start_with]
    self.latest_submission = None

  def store_latest(self):
    submissions = self.__fetch_latest()
    mapped_submissions = map(map_submission, submissions)
    self.data_store.insert_many(mapped_submissions)

  def __fetch_latest(self):
    query = {'before': self.latest_submission} if self.latest_submission else {'limit': self.start_with}
    new_submissions = self.reddit_client.get_submissions(**query)
    if len(new_submissions) > 0:
      self.latest_submission = new_submissions[0]
    return new_submissions
