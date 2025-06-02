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
