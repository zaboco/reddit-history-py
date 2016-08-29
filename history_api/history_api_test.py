from unittest import TestCase

from flask import json

import history_api


TEST_ITEMS = [
  {
    '_id': u't3_4zu59x',
    'author': u'author_name',
    'created_at': 1472303229.0,
    'kind': u'submission',
    'permalink': u'/r/subreddit/comments/4zu59x/title/',
    'score': 2,
    'subreddit': u'subreddit',
    'text': u'Some text'
  }
]


class ApiTest(TestCase):
  @classmethod
  def setUpClass(cls):
    history_api.app.testing = True
    history_api.app.config.update(DATABASE_NAME='test')
    cls.client = history_api.app.test_client()
    with history_api.app.app_context():
      init_data_store(history_api.get_data_store())

  @classmethod
  def tearDownClass(cls):
    with history_api.app.app_context():
      clean_data_store(history_api.get_data_store())

  def test_ok(self):
    response = self.client.get('/items')
    items = json.loads(response.data)
    self.assertEqual(items, TEST_ITEMS)


def init_data_store(data_source):
  data_source.drop()
  data_source.insert_many(TEST_ITEMS)


def clean_data_store(data_source):
  data_source.drop()
