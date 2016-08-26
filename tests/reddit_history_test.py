from unittest import TestCase
from mockito import mock, verify

from fetch.mappers import map_submission
from fetch.reddit_history import RedditHistory
from tests.support.mock_reddit_client import MockRedditClient


class RedditHistoryTest(TestCase):
  def test_initially_saves_the_predefined_number_of_submissions(self):
    mock_reddit_client = MockRedditClient([u'first', u'second', u'third'])
    mock_data_store = mock()
    start_with = 1
    [latest_submission] = mock_reddit_client.get_submissions(limit=start_with)
    history = RedditHistory(reddit_client=mock_reddit_client, data_store=mock_data_store, start_with=start_with)
    history.store_latest()
    verify(mock_data_store).insert_many([map_submission(latest_submission)])
