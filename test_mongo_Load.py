from pymongo import MongoClient

client = MongoClient("mongodb://db:final@121.138.83.113", 27017)
db = client.admin
collection = db.visual_compParts
#print(dir(db))
print(list(collection.find({})))
db.grantRolesToUser( "issueWriter", [{"role": "dbAdminAnyDatabase", "db": "admin"}, {"role": "readWriteAnyDatabase","db": "admin"} ])
{"role": "dbAdminAnyDatabase", "db": "admin"}, {"role": "readWriteAnyDatabase","db": "admin"}
