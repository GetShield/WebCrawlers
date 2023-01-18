import re
import tweepy
import time
import sqlite3
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

con = sqlite3.connect("data.db")
cur = con.cursor()

load_dotenv()
consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_yoken")
access_token_secret = os.getenv("access_token_secret")
bearer_token = os.getenv("bearer_token")

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)

links = [
    "https://twitter.com/DestroyPhish",
    "https://twitter.com/TAKAMURASANG",
    "https://twitter.com/AtomSpam",
    "https://twitter.com/quicksandphish",
    "https://twitter.com/kioan",
    "https://twitter.com/ecarlesi",
    "https://twitter.com/1c4m3by",
    "https://twitter.com/PhishStats",
    "https://twitter.com/CryptoPhishing",
]

ids = []

patterns = {
    "https://twitter.com/DestroyPhish": r"https?:\/\/([\w,-]*\[\.\])+\w+",
    "https://twitter.com/AtomSpam": r"hxxps?:\/\/([\w,-]*\[\.\])+\w+",
    "https://twitter.com/quicksandphish": r"hxxps?:\/\/([\w,-]*\[\.\])+\w+",
    "https://twitter.com/kioan": r"https?\[:\]\/\/([\w,-]*[\[\.\], .])+\w+",
    "https://twitter.com/ecarlesi": r"(hxxps?:\/\/)?([\w,-]*\[\.\])+\w+",
    "https://twitter.com/1c4m3by": r"\/\/([\w,-]*[\[\.\], .])+\w+",
    "https://twitter.com/PhishStats": r"https?:\/\/([\w,-]*\[\.\])+\w+",
    "https://twitter.com/CryptoPhishing": r"(hxxps?:\/\/)?([\w,-]*\[\.\])+\w+",
}

'''
convert hxxps://www[.]google[.].com -> https://www.google.com
'''
def clean_url(url: str):
    url = url.replace("[", "")
    url = url.replace("]", "")
    url = url.replace("hxxp", "http")
    if url.startswith("//"):
        url = "https:" + url
    return url


def getIds():
    for link in links:
        id = getIdByLink(link)
        ids.append(id)


def getIdByName(name: str):
    res = client.get_user(username=name)
    id = res.data.id
    return id


def getIdByLink(link: str):
    name = link.split("/")[-1]
    id = getIdByName(name)
    return id

'''
return an hour before now, which is  used as tweets start_time
'''
def getDate():
    timestamp = datetime.now(timezone.utc)
    addition = timedelta(hours=1)
    timestamp = timestamp - addition
    return timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_and_store_data(link):
    print("start", link)
    id = getIdByLink(link)
    screen_name = link.split("/")[-1]
    startTime = getDate()
    print(startTime)
    name = screen_name
    username = screen_name
    try:
        response = client.get_users_tweets(
            id=id, exclude=["retweets", "replies"], start_time=startTime
        )
        tweets = response.data
        # print(tweets)
        if not tweets:
            return
        for tweet in tweets:
            # print(tweet)
            status = tweet.id  # tweet_id
            content = tweet.text
            if not content:
                continue
            for li in content.split("\n"):
                # print(li)
                res = re.search(patterns[link], li)
                if not res:
                    continue
                result = res.group()
                lnk = clean_url(result)
                print(lnk)
                print(
                    f"insert into main(tweet_id,username,name,images,tweet_url,link,profile) VALUES('{status}','{username}','{name}','{[]}','{link}','{lnk}','{link}')"
                )
                cur.execute(
                    f"insert into main(tweet_id,username,name,images,tweet_url,link,profile) VALUES('{status}','{username}','{name}','{[]}','{link}','{lnk}','{link}')"
                )
                con.commit()

    except Exception as ex:
        print("fetch_and_store_data", ex)


if __name__ == "__main__":
    while True:
        for link in links:
            try:
                fetch_and_store_data(link)
            except Exception as ex:
                print(ex)
        time.sleep(10)
