from sqlalchemy import create_engine, text
import requests
import os
import time

time.sleep(20)

webhook_url=os.getenv("WEBHOOK")

pg_client = create_engine(f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@postgresdb:5432/{os.getenv("POSTGRES_DB")}', echo = True)
pg_client_connect = pg_client.connect()

query = text("SELECT * FROM posts;")

with pg_client_connect as conn:
    data_pull = conn.execute(query).fetchall()
    for i in range(len(data_pull)):
        post = data_pull[i]
        title = post[0]
        score = float(post[1])
        data = { "text": f"Reddit post \"{title}\" has a sentiment score of {score}"} 
        requests.post(url = webhook_url, json = data)
        time.sleep(3600)