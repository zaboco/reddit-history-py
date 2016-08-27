from unittest import TestCase
from mock import Mock, call

from fetch.reddit_history import RedditHistory
from tests.support.fakes import make_reddit_item, map_reddit_item
from tests.support.mock_reddit_client import MockRedditClient

START_WITH = 2


class RedditHistoryTest(TestCase):
  def setUp(self):
    items = map(make_reddit_item, [u'first', u'second', u'third'])
    self.mock_reddit_client = MockRedditClient(items)
    self.mock_data_store = Mock()
    self.history = RedditHistory(
      reddit_client=self.mock_reddit_client,
      data_store=self.mock_data_store,
      item_mapper=map_reddit_item,
      start_with=START_WITH)

  def test_initially_stores_the_predefined_number_of_items(self):
    latest_items = self.mock_reddit_client.get_items(limit=START_WITH)
    self.history.store_latest()
    self.assertInserted(map(map_reddit_item, latest_items))

  def test_stores_only_items_added_while_idle(self):
    self.__store_latest_and_reset_mock()
    new_item = make_reddit_item(u'new')
    self.mock_reddit_client.add_item(new_item)
    self.history.store_latest()
    self.assertInserted([map_reddit_item(new_item)])

  def test_stores_nothing_if_no_new_item_since_last_time(self):
    self.__store_latest_and_reset_mock()
    self.history.store_latest()
    self.mock_data_store.assert_not_called()

  def __store_latest_and_reset_mock(self):
    self.history.store_latest()
    self.mock_data_store.reset_mock()

  def assertInserted(self, items):
    expected_calls = [call.insert_many(items)]
    self.assertListEqual(self.mock_data_store.mock_calls, expected_calls)
