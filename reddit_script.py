import os
import praw
import subprocess

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

# Generate content using Ollama
prompt = "Write an engaging blog post about the latest trends in AI."
content = generate_content(prompt)
print(content)

# Post to Reddit
subreddit_name = 'ChikaPH'  # Corrected subreddit name without 'r/' prefix
try:
    subreddit = reddit.subreddit(subreddit_name)
    title = "Latest Trends in AI"
    submission = subreddit.submit(title, selftext=content)
    print(f"Post submitted to r/{subreddit_name}")
except praw.exceptions.RedditAPIException as e:
    print(f"An error occurred: {e}")

# Test connection
try:
    print(f"Logged in as: {reddit.user.me()}")
except Exception as e:
    print(f"Failed to retrieve user information: {e}")
