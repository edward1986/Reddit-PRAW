import os
import praw
import subprocess
import random
import time

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

# Fetch a random post from the subreddit
random_post = subreddit.random()
if random_post is None:
    raise Exception(f"No random post found in r/{subreddit_name}")
print(f"Selected Post: {random_post.title} (ID: {random_post.id})")

# Fetch comments from the selected post
random_post.comments.replace_more(limit=0)  # Load all top-level comments
comments = random_post.comments.list()

# Filter out comments that are instances of MoreComments
comments = [comment for comment in comments if isinstance(comment, praw.models.Comment)]

# Select a random comment
if not comments:
    raise Exception(f"No comments found in the selected post (ID: {random_post.id})")
selected_comment = random.choice(comments)
print(f"Selected Comment ID: {selected_comment.id}")

# Generate content using Ollama
prompt = f"Reply to the following comment: '{selected_comment.body}'"
response_content = generate_content(prompt)
print(f"Generated Response: {response_content}")

# Reply to the selected comment
try:
    selected_comment.reply(response_content)
    print(f"Replied to comment {selected_comment.id}")
    time.sleep(10)  # Sleep to respect Reddit's API rate limits
except praw.exceptions.RedditAPIException as e:
    print(f"Reddit API error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
