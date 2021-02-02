from pymongo import MongoClient


client = MongoClient("mongodb://issueWriter:final@18.191.252.101", 27017)
db = client.issue_writer
collection = db.visual_data

#collection.insert_one()