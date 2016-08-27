class RedditHistory:
  def __init__(self, reddit_client, data_store, item_mapper, start_with=1):
    self.reddit_client, self.data_store, self.item_mapper = [reddit_client, data_store, item_mapper]
    self.start_with = start_with
    self.latest_item = None

  def store_latest(self):
    items = self.__fetch_latest()
    mapped_items = map(self.item_mapper, items)
    self.data_store.insert_many(mapped_items)

  def __fetch_latest(self):
    query = {'before': self.latest_item} if self.latest_item else {'limit': self.start_with}
    new_items = self.reddit_client.get_items(**query)
    if len(new_items) > 0:
      self.latest_item = new_items[0]
    return new_items
