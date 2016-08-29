import pymongo
from flask import Flask, g as context, jsonify

app = Flask(__name__)

app.config.update(
  DATABASE_HOST='localhost',
  DATABASE_PORT=27017,
  DATABASE_NAME='reddit_history'
)


def get_db():
  if not hasattr(context, 'mongo_client'):
    context.mongo_client = pymongo.MongoClient(app.config['DATABASE_HOST'], app.config['DATABASE_PORT'])
  db_name = app.config['DATABASE_NAME']
  return context.mongo_client[db_name]


@app.teardown_appcontext
def close_db(error):
  if hasattr(context, 'mongo_client'):
    context.mongo_client.close()


@app.route('/items')
def items():
  db = get_db()
  items = list(db.entries.find())
  return jsonify(items)


if __name__ == '__main__':
  app.run()
