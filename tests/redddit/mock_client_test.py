from tests.redddit.reddit_client_test import Base
from tests.support.mock_reddit_client import MockRedditClient


class MockRedditClientTest(Base.RedditClientTest):
  @staticmethod
  def make_client():
    return MockRedditClient(map(fake_item, ['first', 'second', 'third']))

  @staticmethod
  def item_schema():
    return {'name': str}

  def test_adds_item_in_front(self):
    prev_items = self.client.get_items()
    new_item = fake_item(u'new')
    self.client.add_item(new_item)
    updated_items = self.client.get_items()
    self.assertListEqual(updated_items, [new_item] + prev_items)


def fake_item(name):
  return {'name': name}
