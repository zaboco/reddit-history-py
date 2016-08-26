from fetch.mappers import map_submission


class RedditHistory:
  def __init__(self, reddit_client, data_store, start_with):
    self.reddit_client, self.data_store, self.start_with = [reddit_client, data_store, start_with]

  def store_latest(self):
    submissions = self.reddit_client.get_submissions(limit=self.start_with)
    mapped_submissions = map(map_submission, submissions)
    self.data_store.insert_many(mapped_submissions)
