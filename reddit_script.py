import os
import praw
import subprocess
import random

# Define the minimum title length required by the subreddit
MIN_TITLE_LENGTH = 20

def generate_title():
    # Lists of travel-related words
    topics = ['Beaches', 'Mountains', 'Cities', 'Deserts', 'Forests', 'Islands', 'Road Trips', 'Cultural Festivals']
    adjectives = ['Amazing', 'Unforgettable', 'Breathtaking', 'Hidden', 'Enchanting', 'Exotic', 'Adventurous', 'Scenic']
    descriptors = ['Destinations', 'Journeys', 'Experiences', 'Adventures', 'Escapes', 'Getaways', 'Expeditions', 'Trails']
    
    # Randomly select words from each list
    topic = random.choice(topics)
    adjective = random.choice(adjectives)
    descriptor = random.choice(descriptors)
    
    # Construct the title
    title = f"{adjective} {descriptor} in {topic}"
    
    # Ensure the title meets the minimum length requirement
    if len(title) < MIN_TITLE_LENGTH:
        raise ValueError(f"Generated title is too short: {title}")
    
    return title

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
prompt = "Describe a lesser-known travel destination that offers unique cultural experiences and natural beauty."
content = generate_content(prompt)
print(content)

# Post to Reddit
subreddit_name = 'phtravel'  # Corrected subreddit name without 'r/' prefix
try:
    subreddit = reddit.subreddit(subreddit_name)
    title = generate_title()
    flair_templates = list(subreddit.flair.link_templates)
    if flair_templates:
        selected_flair = random.choice(flair_templates)
        flair_id = selected_flair['id']
        flair_text = selected_flair['text']
        print(f"Selected Flair - ID: {flair_id}, Text: {flair_text}")
        submission = subreddit.submit(title, selftext=content, flair_id=flair_id)
    else:
        submission = subreddit.submit(title, selftext=content)
    print(f"Post submitted to r/{subreddit_name}")
except praw.exceptions.RedditAPIException as e:
    print(f"An error occurred: {e}")

# Test connection
try:
    print(f"Logged in as: {reddit.user.me()}")
except Exception as e:
    print(f"Failed to retrieve user information: {e}")
