import praw
import os
from dotenv import load_dotenv
import datetime
import json # Import json module

load_dotenv()

# Load credentials from environment variables
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

def get_subreddit_posts(subreddit_name="netherlands", limit=200):
    """
    Connects to Reddit and fetches posts from the specified subreddit.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=USERNAME,
        password=PASSWORD
    )

    subreddit = reddit.subreddit(subreddit_name)
    print(f"Fetching last {limit} posts from r/{subreddit_name}...")

    posts_data = []
    for submission in subreddit.new(limit=limit):
        post_info = {
            "title": submission.title,
            "text": submission.selftext,
            "url": submission.url,
            "created_utc": datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "author": submission.author.name if submission.author else "[deleted]", # Extract author username
            "score": submission.score # Add post score
        }
        posts_data.append(post_info)
    return posts_data

def save_posts_to_file(posts, filename="reddit_posts.json"):
    """
    Saves a list of post dictionaries to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(posts)} posts to {filename}")

if __name__ == "__main__":
    all_posts = get_subreddit_posts()
    save_posts_to_file(all_posts)
