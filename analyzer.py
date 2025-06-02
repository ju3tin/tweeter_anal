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
