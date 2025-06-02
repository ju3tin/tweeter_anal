# main.py
import tweepy
import time
from listener import Listener
from analyzer import Analyzer
from trusted_accounts import TrustedAccounts
from replier import Replier

# Configuration (to be set via environment variables on Replit)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"
BEARER_TOKEN = "your_bearer_token"

# Initialize Tweepy client (v2 for streaming and user lookup)
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Initialize bot components
listener = Listener(client)
analyzer = Analyzer(client)
trusted_accounts = TrustedAccounts(client)
replier = Replier(client)

def main():
    print("Starting Idea Factory Trust Bot...")
    while True:
        try:
            # Listen for replies mentioning @projectruggaurd with the phrase
            tweets = listener.listen_for_trigger()
            for tweet in tweets:
                # Extract original tweet and author
                original_author_id = listener.get_original_author_id(tweet)
                if not original_author_id:
                    continue

                # Analyze the original author
                analysis = analyzer.analyze_user(original_author_id)
                
                # Check if vouched by trusted accounts
                vouched = trusted_accounts.is_vouched(original_author_id)
                analysis["vouched"] = vouched

                # Reply with the trustworthiness report
                replier.reply_with_report(tweet.id, analysis)
                
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()

# listener.py
class Listener:
    def __init__(self, client):
        self.client = client
        self.trigger_phrase = "@projectruggaurd riddle me this"

    def listen_for_trigger(self):
        # Use X API to fetch recent mentions of @projectruggaurd
        query = "@projectruggaurd -is:retweet"
        tweets = self.client.search_recent_tweets(
            query=query,
            tweet_fields=["in_reply_to_status_id", "author_id"],
            max_results=10
        )
        if not tweets.data:
            return []
        
        # Filter tweets containing the trigger phrase
        matching_tweets = [
            tweet for tweet in tweets.data
            if self.trigger_phrase.lower() in tweet.text.lower()
        ]
        return matching_tweets

    def get_original_author_id(self, tweet):
        # Get the original tweet being replied to
        if not tweet.in_reply_to_status_id:
            return None
        original_tweet = self.client.get_tweet(
            tweet.in_reply_to_status_id,
            user_fields=["id"]
        )
        return original_tweet.data.author_id if original_tweet.data else None

# analyzer.py
from datetime import datetime

class Analyzer:
    def __init__(self, client):
        self.client = client

    def analyze_user(self, user_id):
        # Fetch user data
        user = self.client.get_user(
            id=user_id,
            user_fields=["created_at", "public_metrics", "description"]
        )
        if not user.data:
            return {"error": "User not found"}

        # Fetch recent tweets for content analysis
        tweets = self.client.get_users_tweets(
            id=user_id,
            tweet_fields=["public_metrics"],
            max_results=10
        )

        # Analyze account age
        account_age_days = (datetime.now() - user.data.created_at).days

        # Follower/following ratio
        followers = user.data.public_metrics["followers_count"]
        following = user.data.public_metrics["following_count"]
        ratio = followers / (following + 1)  # Avoid division by zero

        # Bio analysis
        bio = user.data.description
        bio_length = len(bio)
        has_keywords = any(keyword in bio.lower() for keyword in ["scam", "fake", "legit"])

        # Engagement patterns
        avg_likes = 0
        avg_retweets = 0
        if tweets.data:
            total_likes = sum(tweet.public_metrics["like_count"] for tweet in tweets.data)
            total_retweets = sum(tweet.public_metrics["retweet_count"] for tweet in tweets.data)
            avg_likes = total_likes / len(tweets.data)
            avg_retweets = total_retweets / len(tweets.data)

        # Simple sentiment score (placeholder for content analysis)
        sentiment_score = 0.5  # Neutral (0 to 1 scale)

        return {
            "account_age_days": account_age_days,
            "follower_following_ratio": ratio,
            "bio_length": bio_length,
            "has_suspicious_keywords": has_keywords,
            "avg_likes": avg_likes,
            "avg_retweets": avg_retweets,
            "sentiment_score": sentiment_score
        }

# trusted_accounts.py
class TrustedAccounts:
    def __init__(self, client):
        self.client = client
        # Trusted accounts list (from the provided GitHub link layout)
        self.trusted_user_ids = [
            "123456789",  # Replace with actual user IDs from the list
            "987654321",
            "456789123",
            "789123456",
            "321654987"
        ]

    def is_vouched(self, user_id):
        # Check if the user is followed by at least 3 trusted accounts
        following_count = 0
        for trusted_id in self.trusted_user_ids:
            # Check if trusted_id follows user_id
            relation = self.client.get_users_following(id=trusted_id)
            if relation.data and user_id in [follow.id for follow in relation.data]:
                following_count += 1
        return following_count >= 3

# replier.py
class Replier:
    def __init__(self, client):
        self.client = client

    def reply_with_report(self, reply_to_tweet_id, analysis):
        if "error" in analysis:
            report = "Error: Could not analyze the user."
        else:
            # Generate trustworthiness score (simple heuristic)
            score = 50  # Base score
            if analysis["account_age_days"] > 365:
                score += 10
            if analysis["follower_following_ratio"] > 1:
                score += 10
            if not analysis["has_suspicious_keywords"]:
                score += 10
            if analysis["avg_likes"] > 5:
                score += 10
            if analysis["vouched"]:
                score += 20

            report = (
                f"Trustworthiness Report: Score {score}/100\n"
                f"Account Age: {analysis['account_age_days']} days\n"
                f"Follower/Following Ratio: {analysis['follower_following_ratio']:.2f}\n"
                f"Vouched by Trusted Accounts: {'Yes' if analysis['vouched'] else 'No'}"
            )

        # Post the reply
        self.client.create_tweet(
            text=report,
            in_reply_to_tweet_id=reply_to_tweet_id
        )

# requirements.txt
tweepy==4.14.0

# README.md (in markdown format)
# Idea Factory Trust Bot

A simple X bot that analyzes the trustworthiness of a tweet's original author when triggered by the phrase "@projectruggaurd riddle me this" in a reply. The bot is designed to be deployed on a Replit Virtual Machine.

## Setup and Installation

### Prerequisites
- A free X Developer account (sign up at https://developer.x.com/en/portal/petition/essential/basic-info).
- API credentials (API Key, API Secret, Access Token, Access Token Secret, Bearer Token).
- Replit account for deployment.

### Steps
1. **Clone the Repository**
   - Fork or clone this repository to your GitHub account.
   - Import the repository into Replit by selecting "Import from GitHub".

2. **Install Dependencies**
   - Replit will automatically install dependencies listed in `requirements.txt`. Ensure `tweepy` is installed.

3. **Configure API Keys**
   - In Replit, go to the "Secrets" tab (lock icon on the left sidebar).
   - Add the following environment variables with your X API credentials:
     - `API_KEY`: Your API Key
     - `API_SECRET`: Your API Secret
     - `ACCESS_TOKEN`: Your Access Token
     - `ACCESS_TOKEN_SECRET`: Your Access Token Secret
     - `BEARER_TOKEN`: Your Bearer Token
   - Update `main.py` to load these variables (already set up to use hardcoded placeholders; replace them with `os.environ['KEY_NAME']` if needed).

4. **Update Trusted Accounts**
   - In `trusted_accounts.py`, replace the `trusted_user_ids` list with the actual user IDs from the provided trust list: https://github.com/devsyrem/turst-list/blob/main/list.

## Running the Bot
1. In Replit, click the "Run" button.
2. The bot will start monitoring X for replies containing "@projectruggaurd riddle me this".
3. When triggered, it will analyze the original tweet's author and post a trustworthiness report as a reply.

## Bot Architecture
The bot is modular, with separate components for each major function:

- **main.py**: Orchestrates the bot's operation, connecting all modules.
- **listener.py**: Monitors X for the trigger phrase and extracts the original author's user ID.
- **analyzer.py**: Analyzes the target user's trustworthiness based on account age, follower ratio, bio, engagement, and content.
- **trusted_accounts.py**: Checks if the user is vouched by trusted accounts.
- **replier.py**: Generates and posts the trustworthiness report.
- **requirements.txt**: Lists dependencies for Replit deployment.

## Key Features
- Listens for the trigger phrase "@projectruggaurd riddle me this" in replies.
- Analyzes the original tweet's author (not the commenter).
- Evaluates trustworthiness based on multiple metrics.
- Checks if the user is vouched by at least 3 trusted accounts.
- Replies with a concise trustworthiness report.

## Notes
- The bot uses a free X Developer account, which allows up to 1,500 posts per month.
- The trusted accounts list must be updated manually in `trusted_accounts.py`.
- The bot runs continuously, with error handling to prevent crashes.
