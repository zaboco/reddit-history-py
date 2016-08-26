from unittest import TestCase
from mock import Mock, call

from fetch.mappers import map_submission
from fetch.reddit_history import RedditHistory
from tests.support.mock_reddit_client import MockRedditClient


class RedditHistoryTest(TestCase):
  def setUp(self):
    pass
    self.mock_reddit_client = MockRedditClient([u'first', u'second', u'third'])
    self.mock_data_store = Mock()
    self.start_with = 1
    self.history = RedditHistory(
      reddit_client=self.mock_reddit_client,
      data_store=self.mock_data_store,
      start_with=self.start_with)

  def test_initially_stores_the_predefined_number_of_submissions(self):
    [latest_submission] = self.mock_reddit_client.get_submissions(limit=self.start_with)
    self.history.store_latest()
    self.assertInserted([map_submission(latest_submission)])

  def test_stores_only_submissions_added_while_idle(self):
    self.__store_latest_and_rest_mock()
    new_submission = self.mock_reddit_client.add_submission(u'new')
    self.history.store_latest()
    self.assertInserted([map_submission(new_submission)])

  def test_stores_nothing_if_no_new_submission_since_last_time(self):
    self.__store_latest_and_rest_mock()
    self.history.store_latest()
    self.mock_data_store.assert_not_called()

  def __store_latest_and_rest_mock(self):
    self.history.store_latest()
    self.mock_data_store.reset_mock()

  def assertInserted(self, submissions):
    expected_calls = [call.insert_many(submissions)]
    self.assertListEqual(self.mock_data_store.mock_calls, expected_calls)
