import os
import praw
import subprocess
import random

def generate_content(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Error generating content: {result.stderr.strip()}")
    return result.stdout.strip()

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),  # Ensure this is set in your environment variables
    password=os.getenv("REDDIT_PASSWORD")   # Ensure this is set in your environment variables
)

subreddit_name = 'phtravel'  # Replace with your target subreddit
subreddit = reddit.subreddit(subreddit_name)

# Fetch top posts from the subreddit
top_posts = subreddit.top(limit=5)  # Adjust the limit as needed

# Iterate through each top post
for post in top_posts:
    print(f"Processing Post: {post.title} (ID: {post.id})")
    post.comments.replace_more(limit=0)  # Load all top-level comments
    top_level_comments = post.comments.list()

    # Iterate through each top-level comment
    for comment in top_level_comments:
        if isinstance(comment, praw.models.Comment):
            print(f"Processing Comment ID: {comment.id}")
            prompt = f"Reply to the following comment: '{comment.body}'"
            try:
                response_content = generate_content(prompt)
                comment.reply(response_content)
                print(f"Replied to comment {comment.id}")
                time.sleep(10)  # Sleep to respect Reddit's API rate limits
            except praw.exceptions.RedditAPIException as e:
                print(f"Reddit API error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
