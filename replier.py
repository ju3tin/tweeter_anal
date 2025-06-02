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

