from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import Auth_key


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(Auth_key.API_Key, Auth_key.APi_Secret)
        auth.set_access_token(Auth_key.Acess_Token,
                              Auth_key.Acess_Token_Secret)
        return auth


class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # Filter stream to capture keywords:
        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        print(data)
        with open(self.fetched_tweets_filename, 'a') as tf:
            tf.write(data)
            return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    hash_tag_list["donald trump", "hillary clinton"]
    fetched_tweets_filename = "tweets.txt"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
