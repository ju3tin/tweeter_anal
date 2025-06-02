# Tweeter Trust Bot

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
