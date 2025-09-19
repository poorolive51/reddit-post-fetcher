import praw
import os
from dotenv import load_dotenv
import datetime
import json

load_dotenv()

# Load credentials from environment variables
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

def get_user_posts(target_username, limit=100):
    """
    Connects to Reddit and fetches recent posts from a specified user.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=USERNAME,
        password=PASSWORD
    )

    redditor = reddit.redditor(target_username)
    print(f"Fetching last {limit} posts from u/{target_username}...")

    posts_data = []
    for submission in redditor.submissions.new(limit=limit):
        post_info = {
            "title": submission.title,
            "text": submission.selftext,
            "url": submission.url,
            "created_utc": datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "subreddit": submission.subreddit.display_name,
            "author": submission.author.name if submission.author else "[deleted]"
        }
        posts_data.append(post_info)
    return posts_data

def save_posts_to_file(posts, filename):
    """
    Saves a list of post dictionaries to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(posts)} posts to {filename}")

if __name__ == "__main__":
    target_username = "nerfn1k"
    user_posts = get_user_posts(target_username)
    save_posts_to_file(user_posts, f"posts_by_{target_username}.json")
