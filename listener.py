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
