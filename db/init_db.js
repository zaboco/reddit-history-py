#!/usr/local/bin/mongo

conn = new Mongo()
db = conn.getDB("reddit_history")

db.items.createIndex({created_at: -1})
db.items.createIndex({text: 'text'})

print('Created indexes:')
printjson(db.items.getIndexes())
