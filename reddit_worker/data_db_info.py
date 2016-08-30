import sys

import pymongo


def get_db_info(host, database, collection):
  mongo_client = _get_client(host)
  data_source = mongo_client[database][collection]
  _create_indexes(data_source)
  return data_source, mongo_client

def _get_client(host):
  try:
    connection_timeout = 1
    mongo_client = pymongo.MongoClient(host=host, serverSelectionTimeoutMS=connection_timeout)
    mongo_client.server_info()
    return mongo_client
  except pymongo.errors.ServerSelectionTimeoutError as e:
    print('Wrong mongo config: ' + e.message)
    sys.exit(1)

def _create_indexes(data_source):
  data_source.create_index([('created_at', pymongo.DESCENDING)])
  data_source.create_index([('text', pymongo.TEXT)])
