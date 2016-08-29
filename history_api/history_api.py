import pymongo
from flask import Flask, g as context, jsonify, request

app = Flask(__name__)

app.config.update(
  DATABASE_HOST='localhost',
  DATABASE_PORT=27017,
  DATABASE_NAME='reddit_history',
  DATABASE_COLLECTION='items'
)


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
  data_source = get_data_store()
  args = request.args
  items = data_source.find({
    'subreddit': args.get('subreddit'),
    'created_at': {
      '$gte': float(args.get('from')),
      '$lte': float(args.get('to'))
    }
  }).sort('created_at', pymongo.DESCENDING)
  return jsonify(list(items))


if __name__ == '__main__':
  app.run()
