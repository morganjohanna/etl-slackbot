# ETL "Slackbot"
*An ETL pipeline built with Docker to scrape posts from Reddit into a Mongo database, perform a basic sentiment analysis and transform them into a PostgreSQL database, and post them to Slack via webhook*

This repo contains the following directories/modules, all in the **project** directory:
<pre>
├── compose.yml
├── .env
├── etl_job
│   ├── Dockerfile
│   ├── etl.py
│   └── requirements.txt
├── reddit_collector
│   ├── Dockerfile
│   ├── get_reddits.py
│   └── requirements.txt
└── slackbot
    ├── Dockerfile
    ├── post_reddit.py
    └── requirements.txt
</pre>
## Important Security Note
Please note that the .env file included here is a dummy and .gitignore has been accordingly modified to enable it to be added to this repository. In a functioning environment, this file contains real password and authentication data. If you choose to fork or otherwise use this repo, ensure you FIRST uncomment the .env line in .gitignore (line 123) and THEN replace the .env file information. Never upload real authentication data to GitHub!

## Process
The process begins with the initial command "docker-compose up" which creates 5 Docker containers and runs the associated code as follows:
1. **reddit_collector** extracts "hot" Reddit posts from the subreddit AmItheAsshole and writes them into a MongoDB collection it creates in **mongodb**
2. **mongodb** contains posts in a single collection including the post ID, title, and body text, all of which came directly from Reddit
3. **etl_job** runs the simple VADER Sentiment Intensity Analyzer on the body text of each post and writes this and the title into a PostgreSQL database table it creates in **postgresdb**
4. **postgresdb** contains posts in a single table including the post title and VADER score
5. **slackbot** automatically spams a Slack channel with a single post containing the Reddit post title and its VADER score

## Next
* Docker logs can be difficult to navigate, so cleaning up the logs produced when running the compose file would enable better troubleshooting
* I explicitly chose r/AmItheAsshole because posts are ascribed a judgment after a period of time, although the Reddit API unfortunately doesn't allow the scraping of historical posts. I'd like to create a subcollection of posts that already have a judgment and run their titles and sentiment scores through a random forest to see if it would be possible to predict which posts would be judged "YTA", "NTA", "ESH", "NAH", or "INFO" (key to the voting guide can be found at https://www.reddit.com/r/AmItheAsshole/)