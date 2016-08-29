from unittest import TestCase

import pymongo
from flask import json

import history_api

PAST_TIMESTAMP, FUTURE_TIMESTAMP = 0.0, 9999999999.0
DEFAULT_SUBREDDIT = u'some_subreddit'
DEFAULT_TEXT = u'Some text'


def fake_item(index, subreddit=DEFAULT_SUBREDDIT, created_at=PAST_TIMESTAMP + 1, text=DEFAULT_TEXT):
  base_item = {
    '_id': u't3_4zu59' + `index`,
    'author': u'author_name',
    'created_at': created_at,
    'kind': u'submission',
    'permalink': u'/r/subreddit/comments/4zu59x/title/',
    'score': 2,
    'text': text
  }
  return dict(base_item, subreddit=subreddit)


class ApiTest(TestCase):
  @classmethod
  def setUpClass(cls):
    history_api.app.testing = True
    history_api.app.config.update(DATABASE_NAME='test')
    cls.client = history_api.app.test_client()
    with history_api.app.app_context():
      cls.data_source = history_api.get_data_store()

  def setUp(self):
    init_data_source(self.data_source)

  @classmethod
  def tearDownClass(cls):
    clean_data_store(cls.data_source)

  def test_can_filter_by_subreddit(self):
    wanted_subreddit = u'wanted_subreddit'
    wanted_subreddit_items = [fake_item(i, subreddit=wanted_subreddit) for i in range(2)]
    self.data_source.insert_many([
      wanted_subreddit_items[0],
      fake_item(100, u'other_subreddit'),
      wanted_subreddit_items[1]
    ])
    response = self.client.get('/items?'
                               'subreddit=' + wanted_subreddit +
                               '&from=' + `PAST_TIMESTAMP` +
                               '&to=' + `FUTURE_TIMESTAMP`)
    items = json.loads(response.data)
    self.assertEqual(items, wanted_subreddit_items)

  def test_can_filter_by_time_range(self):
    lower_timestamp = 1472303229.0
    upper_timestamp = lower_timestamp + 10
    wanted_items = [fake_item(i, created_at=upper_timestamp - i) for i in range(2)]
    self.data_source.insert_many([
      wanted_items[0],
      fake_item(101, created_at=lower_timestamp - 1000),
      wanted_items[1],
      fake_item(102, created_at=upper_timestamp + 1000),
    ])
    response = self.client.get('/items?'
                               'subreddit=' + DEFAULT_SUBREDDIT +
                               '&from=' + `lower_timestamp` +
                               '&to=' + `upper_timestamp`)
    items = json.loads(response.data)
    self.assertEqual(items, wanted_items)

  def test_items_are_sorted_in_reverse_chronological_order(self):
    latest_timestamp = 1472303229.0
    wanted_items = [fake_item(i, created_at=latest_timestamp - i) for i in range(3)]
    self.data_source.insert_many([
      wanted_items[1],
      wanted_items[0],
      wanted_items[2]
    ])
    response = self.client.get('/items?'
                               'subreddit=' + DEFAULT_SUBREDDIT +
                               '&from=' + `PAST_TIMESTAMP` +
                               '&to=' + `FUTURE_TIMESTAMP`)
    items = json.loads(response.data)
    self.assertEqual(items, wanted_items)

  def test_server_responds_with_error_if_any_query_params_missing(self):
    without_subreddit = self.client.get('/items?from=' + `PAST_TIMESTAMP` + '&to=' + `FUTURE_TIMESTAMP`)
    without_from = self.client.get('/items?subreddit=' + DEFAULT_SUBREDDIT + '&to=' + `FUTURE_TIMESTAMP`)
    without_to = self.client.get('/items?subreddit=' + DEFAULT_SUBREDDIT + '&from=' + `PAST_TIMESTAMP`)

    for error_response in [without_subreddit, without_from, without_to]:
      self.assertEqual(error_response.status_code, 400)
      self.assertRegexpMatches(error_response.data, 'mandatory\s+params')

  def test_can_also_filter_by_keyword(self):
    wanted_keyword = u'keyword'
    wanted_subreddit_items = [fake_item(i, text=wanted_keyword + ' ' + `i`) for i in range(2)]
    self.data_source.insert_many([
      wanted_subreddit_items[0],
      fake_item(100, text=u'irrelevant text'),
      wanted_subreddit_items[1]
    ])
    response = self.client.get('/items?'
                               'subreddit=' + DEFAULT_SUBREDDIT +
                               '&from=' + `PAST_TIMESTAMP` +
                               '&to=' + `FUTURE_TIMESTAMP` +
                               '&keyword=' + wanted_keyword)
    items = json.loads(response.data)
    self.assertEqual(items, wanted_subreddit_items)


def init_data_source(data_source):
  data_source.drop()
  data_source.create_index([('text', pymongo.TEXT)])


def clean_data_store(data_source):
  data_source.drop()
