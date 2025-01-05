import os
import praw
import subprocess
import random
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def generate_content(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Error generating content: {result.stderr.strip()}")
    response = result.stdout.strip()
    promotion = "\n\n---\n[🌐 Visit my blog for more insights: Edwardize](https://edwardize.blogspot.com/) \n---\n"
    return promotion + response

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

def fetch_post_with_comments(subreddit, retries=10):
    """Fetch a random or hot post with comments."""
    attempts = 0
    while attempts < retries:
        try:
            logger.info("Attempting to fetch a random post...")
            random_post = subreddit.random()
            if random_post is None:
                raise Exception("Random post retrieval returned None.")

            random_post.comments.replace_more(limit=0)
            comments = [comment for comment in random_post.comments if isinstance(comment, praw.models.Comment)]
            if comments:
                logger.info(f"Selected Post: {random_post.title} (ID: {random_post.id})")
                return random_post, comments

            logger.warning(f"No comments found in post (ID: {random_post.id}). Retrying...")
        except Exception as e:
            logger.warning(f"Random post retrieval failed: {e}")

        # Fallback to hot posts
        logger.info("Falling back to 'hot' posts...")
        hot_posts = list(subreddit.hot(limit=100))
        if not hot_posts:
            raise Exception(f"No posts available in r/{subreddit.display_name}.")
        random_post = random.choice(hot_posts)
        random_post.comments.replace_more(limit=0)
        comments = [comment for comment in random_post.comments if isinstance(comment, praw.models.Comment)]
        if comments:
            logger.info(f"Selected Post from 'hot': {random_post.title} (ID: {random_post.id})")
            return random_post, comments

        attempts += 1

    raise Exception("Max retries reached. Could not find a post with comments.")

def main():
    popular_subreddits = [sub.display_name for sub in reddit.subreddits.popular(limit=50)]
    subreddit_name = random.choice(popular_subreddits)
    subreddit = reddit.subreddit(subreddit_name)
    logger.info(f"Selected Subreddit: {subreddit_name}")

    try:
        random_post, comments = fetch_post_with_comments(subreddit)
        selected_comment = random.choice(comments)
        logger.info(f"Selected Comment ID: {selected_comment.id}")

        # Generate content and reply
        prompt = f"Reply to the following comment: '{selected_comment.body}'"
        response_content = generate_content(prompt)
        logger.info(f"Generated Response: {response_content}")

        selected_comment.reply(response_content)
        logger.info(f"Replied to comment {selected_comment.id}")
        time.sleep(10)  # Sleep to respect Reddit's API rate limits
    except praw.exceptions.RedditAPIException as e:
        if "RATELIMIT" in str(e):
            logger.warning("Rate limit exceeded. Retrying in 10 minutes...")
            time.sleep(600)  # Wait for 10 minutes
        else:
            logger.error(f"Reddit API error: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
