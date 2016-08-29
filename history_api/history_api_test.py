from unittest import TestCase

from flask import json

import history_api


def fake_item(index, subreddit):
  base_item = {
    '_id': u't3_4zu59' + `index`,
    'author': u'author_name',
    'created_at': 1472303229.0,
    'kind': u'submission',
    'permalink': u'/r/subreddit/comments/4zu59x/title/',
    'score': 2,
    'text': u'Some text'
  }
  return dict(base_item, subreddit=subreddit)


WANTED_SUBREDDIT = u'wanted_subreddit'
WANTED_SUBREDDIT_ITEMS = [fake_item(i, WANTED_SUBREDDIT) for i in range(2)]

TEST_ITEMS = [
  WANTED_SUBREDDIT_ITEMS[0],
  fake_item(100, u'other_subreddit'),
  WANTED_SUBREDDIT_ITEMS[1]
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

  def test_can_filter_by_subreddit(self):
    response = self.client.get('/items?subreddit=' + WANTED_SUBREDDIT)
    items = json.loads(response.data)
    self.assertEqual(items, WANTED_SUBREDDIT_ITEMS)


def init_data_store(data_source):
  data_source.drop()
  data_source.insert_many(TEST_ITEMS)


def clean_data_store(data_source):
  data_source.drop()
