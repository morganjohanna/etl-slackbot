import pymongo
from sqlalchemy import create_engine, text
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

client = pymongo.MongoClient(host = "mongodb", port = 27017)
time.sleep(10)
db = client.reddit
docs = db.posts.find()

pg_client = create_engine(f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@postgresdb:5432/{os.getenv("POSTGRES_DB")}', echo = True)
pg_client_connect = pg_client.connect()
create_table = text(
    """
    CREATE TABLE IF NOT EXISTS posts (
    title VARCHAR(500),
    sentiment NUMERIC
);
""")

pg_client_connect.execute(create_table)
pg_client_connect.commit()

analyzer = SentimentIntensityAnalyzer()

for doc in docs:
    title = doc['title'].replace("'", " ")
    body = doc['body']
    sentiment = analyzer.polarity_scores(body)
    score = sentiment["compound"]
    insert = text(f"INSERT INTO posts VALUES ('{title}', {score});")
    pg_client_connect.execute(insert)
    pg_client_connect.commit()

pg_client_connect.close()