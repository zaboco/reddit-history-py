from unittest import TestCase

from flask import json

import history_api


TEST_ENTRIES = [
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
      init_db(history_api.get_db())

  @classmethod
  def tearDownClass(cls):
    with history_api.app.app_context():
      clean_db(history_api.get_db())

  def test_ok(self):
    response = self.client.get('/items')
    items = json.loads(response.data)
    self.assertEqual(items, TEST_ENTRIES)


def init_db(db):
  db.entries.drop()
  db.entries.insert_many(TEST_ENTRIES)


def clean_db(db):
  db.entries.drop()
