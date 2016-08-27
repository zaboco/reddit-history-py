class RedditHistory:
  def __init__(self, reddit_client, data_store, item_mapper):
    self.reddit_client, self.data_store, self.item_mapper = [reddit_client, data_store, item_mapper]
    [self.latest_item] = self.reddit_client.get_items(limit=1)

  def store_latest(self):
    new_items = self.reddit_client.get_items(before=self.latest_item)
    if len(new_items) > 0:
      self.latest_item = new_items[0]
      mapped_items = map(self.item_mapper, new_items)
      self.data_store.insert_many(mapped_items)
    return len(new_items)
