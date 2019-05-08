"""
This module will be responsible for collecting the tweets.
"""

import os
import tweepy

# Get twitter api keys from environment
TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
# Initialize tweepy objects
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(auth, wait_on_rate_limit=True)


def filter_tweets(tweet_list, filter_retweets=True, filter_replies=True):
    """
        This method will filter tweets that are either retweets or replies.

        Args: 
            tweet_list (list): list of tweets
            filter_retweets (bool): switch for filtering retweets
            filter_replies (bool):  switch for filtering replies

        Returns:
            filtered list of tweets
    """
    filtered_list = []
    # Iterate over tweet list and apply conditions
    for t in tweet_list:
        conditions = []
        # Add retweet filter condition if selected
        if filter_retweets:
            conditions.append(
                (not t['retweeted']) and
                (t['full_text'][0:2] != 'RT'))
        # Add reply filter condition if selected
        if filter_replies:
            conditions.append(
                not t['in_reply_to_status_id'])
        # If filter_replies is set to False, method will return only replies
        else:
            conditions.append(
                t['in_reply_to_status_id'] is not None)

        # If all conditions met, add tweet to filtered list
        if sum(conditions) == len(conditions):
            filtered_list.append(t)

    return filtered_list


def get_tweets(ticker, max_tweets=2500):
    """
        This method will get tweets given a ticker symbol.

        Args:
            ticker (str): stock / crypto ticker symbol
            count (int): number of latest tweets to pull

        Returns:
            list of tweets
    """

    # Add $ to beginning of string if not already $
    if ticker[0] != '$':
        ticker = '$' + ticker
    # Get tweets
    tweet_list = [
        status for status in
        tweepy.Cursor(
            tweepy_api.search,
            q=ticker,
            tweet_mode='extended').items(max_tweets)
    ]
    # Convert tweets to json format
    tweet_list = _convert_to_json(tweet_list)
    # Filter out retweets and replies
    tweets = filter_tweets(tweet_list)
    # Get all tweets classified as replies
    replies = filter_tweets(tweet_list, filter_replies=False)

    return tweets, replies


def _convert_to_json(tweet_list):
    """
        Convert a list of tweepy tweet objects to json format.

        Args:
            tweet_list (list): list of tweepy tweet objects

        Returns:
            modified list in json format
    """
    tweet_list = [i._json for i in tweet_list]

    return tweet_list
