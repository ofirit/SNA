import tweepy as tw

consumer_key = "61QlCNww0s7qGxyEqjiUmjdih"
consumer_secret = "cwLq6wJ0P232WkvatBk1utWp1BcxlDXCh4Fns8xFfrZj051J3X"

access_token = "1204366824353226752-YKXETabiCRWYgdcbU2YuNIKZiuVl55"
access_token_secret = "W1f6FMnfeH52bxpmwYTHeFzExFlpYTUJJ94G0HSrACZNR"


class TwitterAccount:

    def __init__(self):
        # Authorize twitter, initialize tweepy
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(auth, wait_on_rate_limit=True)

    def run(self):
        twitter_account = TwitterAccount()

        try:
            twitter_account.api.verify_credentials()
            print("Authentication OK")

        except:
            print("Error during authentication")

        self.api = twitter_account.api


if __name__ == '__main__':
    b = TwitterAccount()
    b.run()
