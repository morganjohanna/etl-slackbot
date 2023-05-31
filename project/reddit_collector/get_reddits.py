"""
This script gets reddits titles from the reddit api 
and serve in the first step of the dockerized pipeline.
"""

import sys
import requests
import pymongo
from requests.auth import HTTPBasicAuth
import sys
sys.path.append("./data")
import os

sys.stdout.reconfigure(encoding="utf-8")

basic_auth = HTTPBasicAuth(
    username=os.getenv("CLIENT_ID"),
    password=os.getenv("SECRET")
)

GRANT_INFORMATION = dict(
    grant_type="password",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD")
)

headers = {
    "User-Agent": "Mozilla"
}

POST_URL = "https://www.reddit.com/api/v1/access_token"

access_post_response = requests.post(
    url=POST_URL,
    headers=headers,
    data=GRANT_INFORMATION,
    auth=basic_auth
).json()

headers["Authorization"] = access_post_response["token_type"] + " " + access_post_response["access_token"]

topic = "AmItheAsshole"
URL = f"https://oauth.reddit.com/r/{topic}/hot"

response = requests.get(
    url=URL,
    headers=headers
).json()

full_response = response["data"]["children"]

client = pymongo.MongoClient(host="mongodb", port = 27017)
db = client.reddit
collection = db.posts

for post in full_response:
    _id = post["data"]["id"]
    title = post["data"]["title"]
    body = post["data"]["selftext"]
    mongo_input = {"_id":_id, "title": title, "body": body}
    if _id not in collection.distinct("_id"):
        collection.insert_one(mongo_input)