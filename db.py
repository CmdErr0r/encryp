from pymongo import MongoClient
uri = "mongodb://localhost:27017"
client = MongoClient(uri)
client = MongoClient(uri, server_api=pymongo.server_api.ServerApi(version="1", strict=True, deprecation_errors=True))   

try:
    client.admin.command("ping")
    print("try")
    client.close()

except Exception as e:
    raise Exception("The following error occurred: ", e)