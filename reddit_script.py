import os
import praw

# Configure PRAW with environment variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),  # Optional
    password=os.getenv("REDDIT_PASSWORD")   # Optional
)

# Test connection
print(f"Logged in as: {reddit.user.me()}")
