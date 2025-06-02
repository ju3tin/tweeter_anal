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
