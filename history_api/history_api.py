import os
import signal
import sys

import pymongo
from flask import Flask, g as context, jsonify, request

app = Flask(__name__)

app.config.update(
  DATABASE_HOST=os.getenv('MONGO_HOST', 'localhost'),
  DATABASE_PORT=27017,
  DATABASE_NAME=os.getenv('MONGO_DATABASE', 'reddit_history'),
  DATABASE_COLLECTION=os.getenv('MONGO_COLLECTION', 'items')
)

REQUIRED_PARAMS = ['from', 'to', 'subreddit']


def get_data_store():
  if not hasattr(context, 'mongo_client'):
    context.mongo_client = pymongo.MongoClient(app.config['DATABASE_HOST'], app.config['DATABASE_PORT'])
  db_name, db_collection = app.config['DATABASE_NAME'], app.config['DATABASE_COLLECTION']
  return context.mongo_client[db_name][db_collection]


@app.teardown_appcontext
def close_db(error):
  if hasattr(context, 'mongo_client'):
    context.mongo_client.close()


@app.route('/items')
def items():
  params = parse_params(request.args)
  if not params:
    return params_missing_error()
  else:
    return jsonify(fetch_items(params))


def parse_params(args):
  if all(args.has_key(key) for key in REQUIRED_PARAMS):
    return {
      'from': float(args.get('from')),
      'to': float(args.get('to')),
      'subreddit': args.get('subreddit'),
      'keyword': args.get('keyword')
    }
  else:
    return None


def fetch_items(params):
  query = {
    'subreddit': params['subreddit'],
    'created_at': {'$gte': params['from'], '$lte': params['to']}
  }
  if (params['keyword']):
    query.update({
      '$text': {'$search': params['keyword']}
    })
  items = get_data_store().find(query).sort('created_at', pymongo.DESCENDING)
  return list(items)


def params_missing_error():
  response = {
    'message': 'Query takes mandatory params: ' + `REQUIRED_PARAMS`
  }
  return jsonify(response), 400


if __name__ == '__main__':
  def cleanup_and_exit(_signum, _frame):
    print '\nQuiting...'
    close_db(None)
    sys.exit(0)


  signal.signal(signal.SIGINT, cleanup_and_exit)
  signal.signal(signal.SIGTERM, cleanup_and_exit)
  app.run(host='0.0.0.0')
