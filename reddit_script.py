import os
import praw

# Configure Reddit API using environment variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),  # Optional for authenticated actions
    password=os.getenv("REDDIT_PASSWORD"),  # Optional for authenticated actions
)

# Example: Fetch and print top posts from a subreddit
subreddit = reddit.subreddit("learnpython")  # Replace with your preferred subreddit
print("Top posts from r/learnpython:")
for post in subreddit.top(limit=5):
    print(f"Title: {post.title}, Upvotes: {post.score}")
