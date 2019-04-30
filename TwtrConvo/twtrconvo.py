"""
Lee Alessandrini
Text Mining

This module will function as the main driver for the twitter conversation
sentiment analysis package TwtrConvo.
"""

# System imports
import os
import sys
import argparse
import pandas as pd
import json
import re
from textblob import TextBlob
from nltk.corpus import stopwords
# local imports
from .tweets import get_tweets, get_replies
from .plots import create_pie_chart, create_sentiment_gauge, create_boxplot


def convert_tweets_to_df(tweet_list):
    """
        This method will cast the list of tweets to a DataFrame

        Args:
            tweet_list (list): list of tweets

        Returns:
            pandas.DataFrame of tweets with various fields
    """
    columns = ['id', 'username', 'tweet', 'text', 'favorites', 'retweets',
               'followers', 'following']
    df = pd.DataFrame(
        index=range(len(tweet_list)),
        columns=columns)
    index = 0
    for tweet in tweet_list:
        df.loc[index, columns] = [
            tweet['id'],
            tweet['user']['screen_name'],
            tweet['full_text'],
            clean_tweet(tweet['full_text']),
            tweet['favorite_count'],
            tweet['retweet_count'],
            tweet['user']['followers_count'],
            tweet['user']['friends_count']
        ]
        index += 1
    # Create column for net influence
    df['net_influence'] = df['followers'] - df['following']
    # Filter invalid tweets
    df = df.loc[~df['text'].isnull()].reset_index()

    return df


def clean_tweet(tweet):
    """
        Utility function to clean tweet text by removing links, special
        characters  and other unwanted characters using a simple regex.

        Args:
            tweet (str): tweet text string

        Returns:
            cleaned text
    """
    regx = re.compile("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t'])|(\w+:\/\/\S+)")
    return ' '.join(re.sub(regx, " ", tweet).split()) 


def rank_tweets(tweet_df, n=50):
    """
        Get top n ranked tweets based on net influence (net followers),
        retweets, and favorites.
        TODO: Add weighting

        Args:
            tweet_df (pandas.DataFrame): DataFrame of tweets
            n (int): top number of ranked tweets to take

        Returns:
            n top ranked tweets
    """

    cols = ['net_influence', 'retweets', 'favorites']
    ranked_cols = {c: c + 'rank' for c in cols}
    ranks = tweet_df[cols].rank().rename(columns=ranked_cols)
    tweet_df = pd.concat([tweet_df, ranks], axis=1)
    tweet_df['rank'] = tweet_df[list(ranked_cols.values())].sum(axis=1)
    tweet_df.sort_values('rank', ascending=False, inplace=True)

    return tweet_df.head(n)


def get_reply_df(tweet_df):
    """
        Get replies to top ranked tweets.

        Args:
            tweet_df (pandas.DataFrame): tweet table

        Returns:
            table of replies with foreign key columns linking to ranked tweets
    """
    reply_df = pd.DataFrame()

    for index, row in tweet_df.iterrows():
        tweet_id = row['id']
        username = row['username']
        # Get replies
        replies = get_replies(tweet_id, username)
        # Create replies df
        replies_df = convert_tweets_to_df(replies)
        # Add original tweet id as foreign key
        replies_df['reply_id'] = tweet_id
        # Concat on existing data
        reply_df = pd.concat([reply_df, replies_df], ignore_index=True)

    return reply_df


def build_dataset(ticker, save=False):
    """
        This method will build a dataset for a given ticker.

        Args:
            ticker (str): company ticker symbol
            save (bool): switch for whether to save the dataset

        Returns:
            tweet and reply DataFrames
    """
    # Get tweets (returns latest tweets in dict)
    tweet_list = get_tweets(ticker)
    # --- Metrics for tweet ranking ---
    tweet_df = convert_tweets_to_df(tweet_list)
    # Only get highest ranked tweets
    tweet_df = rank_tweets(tweet_df)
    # Get replies to ranked tweets
    reply_df = get_reply_df(tweet_df)
    # Save tweets
    if save:
        tweet_df.to_csv(os.path.join('datasets', ticker, 'tweets.csv'),
                        index=False)
        reply_df.to_csv(os.path.join('datasets', ticker, 'replies.csv'),
                        index=False)

    return tweet_df, reply_df


def load_dataset(data_path):
    """
        This method will load a previously built dataset.
        TODO: Figure out why empty strings are being saved,
              for now just use na_filter=False

        Args:
            data_path (str): path to dataset

        Returns:
            tweet and reply DataFrames
    """
    # Load tweets
    tweet_df = pd.read_csv(os.path.join(data_path, 'tweets.csv'),
                           na_filter=False)
    reply_df = pd.read_csv(os.path.join(data_path, 'replies.csv'),
                           na_filter=False)

    return tweet_df, reply_df


def get_blob(ticker, tweet_df):
    """
        This method will take a DataFrame of tweets and turn all the text into
        a single TextBlob.

        Args:
            ticker (str): ticker symbol
            tweet_df (pandas.DataFrame): tweets

        Returns:
            textblob.TextBlob object of all text from tweets
    """
    # Create initial blob
    blob = TextBlob(' '.join(tweet_df['text'].values).lower())
    # Filter by stopwords
    filtered_words = [
        word for word in blob.words
        if (word not in stopwords.words('english')) and
        (word != ticker.lower())]
    # Create new blob without stop words
    blob = TextBlob(' '.join(filtered_words))

    return blob


def get_word_count(blob):
    """
        This method will build a word count DataFrame given a text blob.
        TODO: Make all words singular
        TODO: Add n-grams (likely n=2)

        Args:
            blob (textblob.TextBlob): blob of all words from tweets

        Returns:
            word count pandas.DataFrame
    """
    # Get the count of each words
    count_dict = {word: blob.words.count(word) for word in blob.words}
    # Cast to DataFrame
    word_count = pd.DataFrame(
        data=list(count_dict.items()),
        columns=['word', 'count']).sort_values('count', ascending=False)

    return word_count


def save_figures(html_path, figures):
    """
        This method will save the figures to interactive html files using
        plotly's offline mode.

        Args:
            html_path (str): path to where plots will be saved
            figures (dict): map of plotly figure dicts

        Returns:
            None
    """
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot
    from plotly import tools

    for figure_name, fig in figures.items():
            # Save plotly figure to html
            plot(fig, filename=os.path.join(
                html_path, '{}.html'.format(figure_name)))

    return


def main(ticker, build):
    """
        This method will drive the primary functionality of the package.

        Args:
            ticker (str): company ticker symbol
            build (bool): boolean to build or load data

        Returns:
            None
    """
    # Initialize data path
    data_path = os.path.join('datasets', ticker)
    # If build, get new tweets and save them
    if build:
        # If dataset path does not exist, create it
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        # Build dataset
        tweet_df, reply_df = build_dataset(ticker, save=True)
    # Otherwise, load previously collected tweets
    else:
        # Load dataset
        tweet_df, reply_df = load_dataset(data_path)
    # Get text blobs and word count
    tweet_blob = get_blob(ticker, tweet_df)
    tweet_word_count = get_word_count(tweet_blob)
    reply_blob = get_blob(ticker, reply_df)
    reply_word_count = get_word_count(reply_blob)
    # --- Create plotly HTML files ---
    # Initialize html directory
    html_path = os.path.join(data_path, 'html')
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    # -- Create Figures --
    figures = {}
    figures['pie_chart'] = create_pie_chart(tweet_word_count, reply_word_count)
    figures['sentiment_guage'] = create_sentiment_gauge(tweet_blob)
    figures['boxplots'] = create_boxplot(tweet_df)
    # -- Save figures as html files --
    save_figures(html_path, figures)

    return
