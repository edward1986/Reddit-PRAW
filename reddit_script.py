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
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),  # Optional
    password=os.getenv("REDDIT_PASSWORD")   # Optional
)

prompt = "Write an engaging blog post about the latest trends in AI."
content = generate_content(prompt)

# Post to Reddit
subreddit = reddit.subreddit('popular')
title = "Latest Trends in AI"
submission = subreddit.submit(title, selftext=content)

# Test connection
print(f"Logged in as: {reddit.user.me()}")
