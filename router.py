import pymongo
import os

client = pymongo.MongoClient("mongodb://localhost:21017")

folder = client["folder"]
file = folder["file"]

print("okay")
print(client.list_database_names())
print("okay")


print(folder.list_collection_names())

# with open("test/")

# bytes(, 'utf-8')

# def sync()
