import praw
import os
from dotenv import load_dotenv
import json
import re # Import regular expression module
import datetime # Import datetime module

load_dotenv()

# Load credentials from environment variables
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

def search_subreddit(subreddit_name, search_word, limit=1000):
    """
    Connects to Reddit and searches for a specific word in posts and comments
    within a specified subreddit.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=USERNAME,
        password=PASSWORD
    )

    subreddit = reddit.subreddit(subreddit_name)
    print(f"Searching for '{search_word}' in r/{subreddit_name} (limit: {limit} posts)...")

    found_items = {
        "posts": [],
        "comments": []
    }

    # Search in posts
    for submission in subreddit.new(limit=limit):
        # Check title and selftext
        if re.search(r'\b' + re.escape(search_word) + r'\b', submission.title, re.IGNORECASE) or \
           (submission.selftext and re.search(r'\b' + re.escape(search_word) + r'\b', submission.selftext, re.IGNORECASE)):
            found_items["posts"].append({
                "type": "post",
                "title": submission.title,
                "url": submission.url,
                "score": submission.score,
                "author": submission.author.name if submission.author else "[deleted]",
                "created_utc": datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            })

        # Search in comments
        submission.comments.replace_more(limit=0) # Flatten comment tree
        for comment in submission.comments.list():
            if re.search(r'\b' + re.escape(search_word) + r'\b', comment.body, re.IGNORECASE):
                found_items["comments"].append({
                    "type": "comment",
                    "body": comment.body,
                    "permalink": comment.permalink,
                    "score": comment.score,
                    "author": comment.author.name if comment.author else "[deleted]",
                    "created_utc": datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "submission_title": submission.title
                })
    
    print(f"Found {len(found_items['posts']) } posts and {len(found_items['comments']) } comments containing '{search_word}'")
    return found_items

def save_to_file(data, filename):
    """
    Saves a dictionary or list of dictionaries to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved data to {filename}")

if __name__ == "__main__":
    target_subreddit = "netherlands"
    search_word = "bot"

    found_data = search_subreddit(target_subreddit, search_word)
    save_to_file(found_data, f"search_results_{target_subreddit}_{search_word}.json")
