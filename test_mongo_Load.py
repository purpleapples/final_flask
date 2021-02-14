from pymongo import MongoClient

client = MongoClient("mongodb://backip", 27017)
db = client.admin
collection = db.visual_compParts
#print(dir(db))
print(list(collection.find({})))
db.grantRolesToUser( "issueWriter", [{"role": "dbAdminAnyDatabase", "db": "admin"}, {"role": "readWriteAnyDatabase","db": "admin"} ])
{"role": "dbAdminAnyDatabase", "db": "admin"}, {"role": "readWriteAnyDatabase","db": "admin"}
