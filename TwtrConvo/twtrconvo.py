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
import numpy as np
import json
import re
from textblob import TextBlob
from nltk.corpus import stopwords
# local imports
from .tweets import get_tweets
from .plots import (
    create_pie_chart, create_sentiment_gauge, create_boxplot,
    create_distplot, create_user_description_scatter, create_2d_histogram,
    create_violin_plot
)


def convert_tweets_to_df(tweet_list, replies=False):
    """
        This method will cast the list of tweets to a DataFrame

        Args:
            tweet_list (list): list of tweets
            replies (bool): whether or not df is replies

        Returns:
            pandas.DataFrame of tweets with various fields
    """
    columns = ['id', 'username', 'user_id','tweet', 'text', 'favorites', 'retweets',
               'followers', 'following', 'polarity', 'subjectivity']
    if replies:
        columns += ['reply_id']
    df = pd.DataFrame(
        index=range(len(tweet_list)),
        columns=columns)
    index = 0
    for tweet in tweet_list:
        cleaned_text = clean_text(tweet['full_text'])
        # Create TextBlob to get sentiment results
        blob = TextBlob(cleaned_text)
        # Build row
        values = [
            tweet['id'],
            tweet['user']['screen_name'],
            tweet['user']['id'],
            tweet['full_text'],
            cleaned_text,
            tweet['favorite_count'],
            tweet['retweet_count'],
            tweet['user']['followers_count'],
            tweet['user']['friends_count'],
            blob.sentiment.polarity,
            blob.sentiment.subjectivity
        ]
        # If replies==True, include foreign key
        if replies:
            values.append(
                tweet['in_reply_to_status_id'])

        df.loc[index, columns] = values
        index += 1
    # Create column for net influence
    df['net_influence'] = df['followers'] - df['following']
    # Filter invalid tweets
    df = df.loc[~df['text'].isnull()].reset_index()

    return df


def clean_text(tweet):
    """
        Utility function to clean tweet text by removing links, special
        characters  and other unwanted characters using a simple regex.

        Args:
            tweet (str): tweet text string

        Returns:
            cleaned text
    """
    regx = re.compile("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)")
    return ' '.join(re.sub(regx, " ", tweet).split()) 


def rank_tweets(tweet_df, n=200):
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


def get_user_info_df(tweet_list, ids=[]):
    """
        This method will organize user data from a list of a tweets into a
        DataFrame.

        Args:
            tweet_list (list): list of tweets
            ids (list): list of user ids to filter by

        Returns:
            user information DataFrame
    """
    # Cast user data to DataFrame
    user_df = pd.DataFrame(
        {i['user']['screen_name']: {
            'user_id': i['user']['id'],
            'full_description': i['user']['description'],
            'followers': i['user']['followers_count'],
            'following': i['user']['friends_count'],
            'favorites': i['user']['favourites_count'],
            'tweet_count': i['user']['statuses_count']
            } for i in tweet_list}).T.reset_index()
    user_df.rename(columns={'index': 'username'}, inplace=True)
    # Clean full descriptions
    user_df['description'] = [
        clean_text(d) for d in user_df['full_description']]
    user_df['net_influence'] = user_df['followers'] - user_df['following']
    # If list of ids are passed in, filter by this list
    if ids:
        user_df = user_df.loc[user_df['user_id'].isin(ids)]

    return user_df


def build_dataset(ticker, data_path=''):
    """
        This method will build a dataset for a given ticker.

        Args:
            ticker (str): company ticker symbol
            save (bool): switch for whether to save the dataset

        Returns:
            tweet and reply DataFrames
    """
    # Get tweets (returns latest tweets in dict)
    tweet_list, reply_list = get_tweets(ticker)
    # --- Metrics for tweet ranking ---
    tweet_df = convert_tweets_to_df(tweet_list)
    reply_df = convert_tweets_to_df(reply_list, replies=True)
    # Only get highest ranked tweets
    tweet_df = rank_tweets(tweet_df)
    # Get replies to top tweets
    reply_df = reply_df.loc[
        reply_df['reply_id'].isin(tweet_df['id'].values)]
    # Get user information
    user_df = get_user_info_df(
        tweet_list, ids=list(tweet_df['user_id'].unique()))
    # Save tweets, replies, and user information
    if data_path:
        tweet_df.to_csv(os.path.join(data_path, 'tweets.csv'),
                        index=False)
        reply_df.to_csv(os.path.join(data_path, 'replies.csv'),
                        index=False)
        user_df.to_csv(os.path.join(data_path, 'users.csv'),
                       index=False)

    return tweet_df, reply_df, user_df


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
    user_df = pd.read_csv(os.path.join(data_path, 'users.csv'),
                          na_filter=False)

    return tweet_df, reply_df, user_df


def get_blob(ticker, df, header='text'):
    """
        This method will take a DataFrame of tweets and turn all the text into
        a single TextBlob.

        Args:
            ticker (str): ticker symbol
            df (pandas.DataFrame): data with text
            header (str): header of text column

        Returns:
            textblob.TextBlob object of all text from tweets
    """
    # Create initial blob
    blob = TextBlob(' '.join(df[header].values).lower())
    # Filter by stopwords
    filtered_words = [
        word for word in blob.words
        if (word not in stopwords.words('english')) and
        (not word.isnumeric()) and
        (word != ticker.lower())]
    # Create new blob without stop words
    blob = TextBlob(' '.join(filtered_words))

    return blob


def get_word_count(blob, n=1):
    """
        This method will build a word count DataFrame given a text blob.

        Args:
            blob (textblob.TextBlob): blob of all words from tweets
            n (int): number of ngrams

        Returns:
            word count pandas.DataFrame
    """
    # Get the count of each words
    count_dict = {}
    for ngram in blob.ngrams(n=n):
        term = ' '.join(ngram)
        if term in count_dict:
            count_dict[term] += 1
        else:
            count_dict[term] = 1
    # Cast to DataFrame
    word_count = pd.DataFrame(
        data=list(count_dict.items()),
        columns=['word', 'count']).sort_values('count', ascending=False)
    # Reset index of word count df
    word_count = word_count.reset_index(drop=True)

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


def add_user_data(user_word_count, user_df):
    """
        This method will add data to the word count DataFrame.
    """

    # Add avg net influence of users with each word in their description
    user_word_count['avg_net_influence'] = np.nan

    for index, row in user_word_count.iterrows():
        word_in_description = user_df['description'].apply(
            lambda x: row['word'] in x.lower())
        user_word_count.loc[index, 'avg_net_influence'] = user_df.loc[
            word_in_description, 'net_influence'].mean()

    return user_word_count


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
        tweet_df, reply_df, user_df = build_dataset(
            ticker, data_path=data_path)
    # Otherwise, load previously collected tweets
    else:
        # Load dataset
        tweet_df, reply_df, user_df = load_dataset(data_path)
    # Get text blobs and word count
    tweet_blob = get_blob(ticker, tweet_df)
    tweet_word_count = get_word_count(tweet_blob)
    tweet_bigram_count = get_word_count(tweet_blob, n=2)
    tweet_trigram_count = get_word_count(tweet_blob, n=3)
    reply_blob = get_blob(ticker, reply_df)
    reply_word_count = get_word_count(reply_blob)
    user_blob = get_blob(ticker, user_df, header='description')
    user_word_count = get_word_count(user_blob)
    user_word_count = add_user_data(user_word_count, user_df)
    # --- Create plotly HTML files ---
    # Initialize html directory
    html_path = os.path.join(data_path, 'html')
    if not os.path.exists(html_path):
        os.makedirs(html_path)
    # -- Create Figures --
    figures = {}
    figures['word_count_pie_chart'] = create_pie_chart(
        tweet_word_count, reply_word_count)
    figures['ngram_count_pie_chart'] = create_pie_chart(
        tweet_bigram_count, tweet_trigram_count, name_1='bigrams',
        name_2='trigrams')
    figures['sentiment_guage'] = create_sentiment_gauge(tweet_blob)
    figures['retweets_favs_boxplots'] = create_boxplot(tweet_df)
    figures['sentiment_boxplots'] = create_boxplot(
        tweet_df, columns=['polarity', 'subjectivity'], title='Sentiment')
    figures['sentiment_violin_plot'] = create_violin_plot(
        tweet_df, ['polarity', 'subjectivity'], 'Sentiment Violin Plot')
    figures['user_influence_distplot'] = create_distplot(user_df)
    figures['user_description_scatter'] = create_user_description_scatter(
        user_word_count)
    figures['user_activity_heatmap'] = create_2d_histogram(
        user_df, 'net_influence', 'tweet_count',
        'User Activity vs. Influence')
    # -- Save figures as html files --
    save_figures(html_path, figures)

    return
