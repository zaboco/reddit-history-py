from unittest import TestCase

from mock import Mock, call

from fetch.reddit_history import RedditHistory
from tests.support.fakes import make_reddit_item, map_reddit_item
from tests.support.mock_reddit_client import MockRedditClient


class RedditHistoryTest(TestCase):
  def setUp(self):
    past_items = map(make_reddit_item, [u'past'])
    self.mock_reddit_client = MockRedditClient(past_items)
    self.mock_data_store = Mock()
    self.history = RedditHistory(
      reddit_client=self.mock_reddit_client,
      data_store=self.mock_data_store,
      item_mapper=map_reddit_item)

  def test_initially_stores_items_added_after_it_started(self):
    first_new_item = make_reddit_item(u'first_new')
    self.mock_reddit_client.add_item(first_new_item)
    count = self.history.store_latest()
    self.assertEqual(count, 1)
    self.assertInserted([map_reddit_item(first_new_item)])

  def test_stores_only_items_added_while_idle(self):
    self.__store_latest_and_reset_mock()
    new_items = map(make_reddit_item, [u'second_new', u'third_new'])
    for new_item in new_items:
      self.mock_reddit_client.add_item(new_item)
    count = self.history.store_latest()
    self.assertEqual(count, 2)
    self.assertInserted(list(reversed(map(map_reddit_item, new_items))))

  def test_stores_nothing_if_no_new_item_since_last_time(self):
    self.__store_latest_and_reset_mock()
    self.history.store_latest()
    self.mock_data_store.insert_many.assert_not_called()

  def __store_latest_and_reset_mock(self):
    self.mock_reddit_client.add_item(make_reddit_item(u'first_new'))
    self.history.store_latest()
    self.mock_data_store.reset_mock()

  def assertInserted(self, items):
    expected_calls = [call.insert_many(items)]
    self.assertListEqual(self.mock_data_store.mock_calls, expected_calls)
