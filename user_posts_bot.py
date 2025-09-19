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

def get_user_profile_data(target_username):
    """
    Connects to Reddit and fetches profile data for a specified user.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=USERNAME,
        password=PASSWORD
    )

    redditor = reddit.redditor(target_username)
    print(f"Fetching profile data for u/{target_username}...")

    profile_data = {
        "username": redditor.name,
        "created_utc": datetime.datetime.fromtimestamp(redditor.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        "link_karma": redditor.link_karma,
        "comment_karma": redditor.comment_karma,
        "is_employee": redditor.is_employee,
        "is_mod": redditor.is_mod,
        "is_gold": redditor.is_gold,
        "has_verified_email": redditor.has_verified_email,
        "total_karma": redditor.total_karma
    }
    return profile_data

def save_to_file(data, filename):
    """
    Saves a dictionary or list of dictionaries to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved data to {filename}")

if __name__ == "__main__":
    target_username = "nerfn1k"

    # Fetch and save user posts
    user_posts = get_user_posts(target_username)
    save_to_file(user_posts, f"posts_by_{target_username}.json")

    # Fetch and save user profile data
    user_profile = get_user_profile_data(target_username)
    save_to_file(user_profile, f"profile_of_{target_username}.json")
