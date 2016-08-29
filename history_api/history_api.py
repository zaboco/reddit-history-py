import pymongo
from flask import Flask, g as context, jsonify, request

app = Flask(__name__)

app.config.update(
  DATABASE_HOST='localhost',
  DATABASE_PORT=27017,
  DATABASE_NAME='reddit_history',
  DATABASE_COLLECTION='items'
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
      'subreddit': args.get('subreddit')
    }
  else:
    return None


def fetch_items(params):
  items = get_data_store().find({
    'subreddit': params['subreddit'],
    'created_at': {
      '$gte': params['from'],
      '$lte': params['to']
    }
  }).sort('created_at', pymongo.DESCENDING)
  return list(items)


def params_missing_error():
  response = {
    'message': 'Query takes mandatory params: ' + `REQUIRED_PARAMS`
  }
  return jsonify(response), 400


if __name__ == '__main__':
  app.run()
