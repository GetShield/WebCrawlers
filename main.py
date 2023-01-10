import time

from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC
from random import randint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import logging
from driver_utils import Utilities
from element_finder import Finder
import re
logger = logging.getLogger(__name__)
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(format)
logger.addHandler(ch)
import sqlite3
import json
con = sqlite3.connect("data.db")
cur = con.cursor()


links=["https://twitter.com/DestroyPhish","https://twitter.com/TAKAMURASANG",
        "https://twitter.com/AtomSpam",
        "https://twitter.com/quicksandphish",
        "https://twitter.com/kioan",
        "https://twitter.com/ecarlesi",
        "https://twitter.com/1c4m3by",
        "https://twitter.com/PhishStats",
        "https://twitter.com/CryptoPhishing"]

tweets_count = 100
posts_data = {}
retry = 10
def check_tweets_presence(tweet_list,retry):
    if len(tweet_list) <= 0:
        retry -= 1


def check_retry(retry):
    return retry <= 0


def fetch_and_store_data(driver,retry,profile):
    try:
        all_ready_fetched_posts = []
        present_tweets = Finder.find_all_tweets(driver)
        check_tweets_presence(present_tweets,retry)
        all_ready_fetched_posts.extend(present_tweets)
        retry=10
        posts_data={}
        scol=0
        while len(posts_data) < tweets_count or scol<tweets_count:
            time.sleep(5)
            try:
                driver.find_elements(By.XPATH, '//*[contains(text(), "Not now")]')[0].click()  # ;)

            except:pass

            driver.maximize_window()
            print('total done: ',len(posts_data),scol)
            for tweet in present_tweets:
                try:
                    name = Finder.find_name_from_tweet(tweet)
                    status, tweet_url = Finder.find_status(tweet)
                    replies = Finder.find_replies(tweet)
                    retweets = Finder.find_shares(tweet)
                    username = tweet_url.split("/")[3]
                    status = status[-1]
                    is_retweet = Finder.is_retweet(tweet)
                    posted_time = Finder.find_timestamp(tweet)
                    content = Finder.find_content(tweet)
                    likes = Finder.find_like(tweet)
                    images = Finder.find_images(tweet)
                    videos = Finder.find_videos(tweet)
                    hashtags = re.findall(r"#(\w+)", content)
                    mentions = re.findall(r"@(\w+)", content)
                    profile_picture = Finder.find_profile_image_link(tweet)
                    link = Finder.find_external_link(tweet)
                    if '//' in content:
                        for li in content.split("\n"):
                            if li.startswith('//'):
                                cur.execute(
                                    f"insert into main(tweet_id,username,name,images,tweet_url,link,profile) VALUES('{status}','{username}','{name}','{images}','{tweet_url}','{li}','{profile}')")
                                con.commit()
                    if link=="":
                        continue
                    query = f"SELECT * from main where tweet_id='{status}'"
                    if cur.execute(query).fetchone() is not None:
                        scol=scol+1
                        continue
                    cur.execute(
                        f"insert into main(tweet_id,username,name,images,tweet_url,link,profile) VALUES('{status}','{username}','{name}','{images}','{tweet_url}','{link}','{profile}')")
                    con.commit()
                    posts_data[status] = {
                        "tweet_id": status,
                        "username": username,
                        "name": name,
                        "profile_picture": profile_picture,
                        "replies": replies,
                        "retweets": retweets,
                        "likes": likes,
                        "is_retweet": is_retweet,
                        "posted_time": posted_time,
                        "content": content,
                        "hashtags": hashtags,
                        "mentions": mentions,
                        "images": images,
                        "videos": videos,
                        "tweet_url": tweet_url,
                        "link": link
                    }
                except:pass

            Utilities.scroll_down(driver)
            driver.minimize_window()
            # Utilities.wait_until_completion(driver)
            # Utilities.wait_until_tweets_appear(driver)
            present_tweets = Finder.find_all_tweets(
                driver)
            present_tweets = [
                post for post in present_tweets if post not in all_ready_fetched_posts]
            # check_tweets_presence(present_tweets,retry)
            if len(present_tweets) <= 0:
                retry -= 1
            all_ready_fetched_posts.extend(present_tweets)
            if check_retry(retry) is True:
                break

    except Exception as ex:
        logger.exception(
            "Error at method fetch_and_store_data : {}".format(ex))


def scrap(driver):
    try:
        data=[]
        for URL in links:
            tweets_count = 100
            retry = 10
            driver.get(URL)
            Utilities.wait_until_completion(driver)
            while 1:
                try:
                    if 'Yes, view profile' in driver.page_source:
                        driver.find_elements(By.XPATH, '//*[contains(text(), "Yes, view profile")]')[0].click()  # ;)
                        break
                    else:break
                except:
                    Utilities.scroll_downkey(driver,2)
            time.sleep(5)
            driver.find_elements(By.XPATH, '//body')[0].click()
            try:
                driver.find_elements(By.XPATH, '//*[contains(text(), "Not now")]')[0].click()  # ;)

            except:pass
            time.sleep(5)
            fetch_and_store_data(driver,retry,URL)

    except Exception as ex:
        logger.exception(
            "Error at method scrap on : {}".format(ex))










driver = uc.Chrome()
data=scrap(driver)
driver.quit()




