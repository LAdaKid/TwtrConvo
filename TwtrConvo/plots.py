"""
This module will create the different plotly objects.
"""

import os
import numpy as np
import plotly.graph_objs as go


def create_pie_chart(tweet_word_count, reply_word_count, n=10):
    """
        This method will create two pie charts displaying word frequencies.

        Args:
            tweet_word_count (pandas.DataFrame): word count of top tweets
            reply_word_count (pandas.DataFrame): word count of replies

        Returns:
            figure dict object formatted for plotly
    """
    # --- Create Pie Chart with top n terms --- 
    fig = {
      "data": [
        {
          "values": tweet_word_count['count'].values[:n],
          "labels": tweet_word_count['word'].values[:n],
          "domain": {"column": 0},
          "hole": .4,
          "type": "pie",
          "name": "Tweets"
        },
        {
          "values": reply_word_count['count'].values[:n],
          "labels": reply_word_count['word'].values[:n],
          "domain": {"column": 1},
          "hole": .4,
          "type": "pie",
          "name": "Replies"
        }],
      "layout": {
            "title":"Word Frequency",
            "grid": {"rows": 1, "columns": 2},
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Tweets",
                    "x": 0.20,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Replies",
                    "x": 0.8,
                    "y": 0.5
                }
            ]
        }
    }

    return fig


def create_sentiment_gauge(blob):
    """
        This method will create a plotly formatted dict which will be displayed
        as a guage, and will show the general sentiment of the text from all
        the tweets.
        TODO: Add subjectivity as second guage

        Args:
            blob (textblob.TextBlob): TextBlob of all tweets

        Returns:
            figure dict object formatted for plotly
    """
    # --- Create Gauge Chart ---
    polarity = blob.sentiment.polarity

    base_chart = {
        "values": [40, 20, 20, 20],
        "labels": ["-", "-1", "0", "1"],
        "domain": {"x": [0, .48]},
        "marker": {
            "colors": [
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)'
            ],
            "line": {
                "width": 1
            }
        },
        "name": "Gauge",
        "hole": .4,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 108,
        "showlegend": False,
        "hoverinfo": "none",
        "textinfo": "label",
        "textposition": "outside"
    }

    pos_fraction = 50 / 3

    meter_chart = {
        "values": [50, pos_fraction, pos_fraction, pos_fraction],
        "labels": ["Polarity", "Negative", "Neutral", "Positive"],
        "marker": {
            'colors': [
                'rgb(255, 255, 255)',
                'rgb(255, 102, 102)', # Light Red
                'rgb(192, 192, 192)', # Grey
                'rgb(178, 255, 102)' # Light Green
            ]
        },
        "domain": {"x": [0, 0.48]},
        "name": "Gauge",
        "hole": .3,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90,
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "hoverinfo": "none"
    }

    # Create dial for guage

    # -- Rotate dial appropriately --
    def rotate_point(point, angle, center_point=(0, 0)):
        """Rotates a point around center_point(origin by default)
        Angle is in degrees.
        Rotation is counter-clockwise
        """
        angle_rad = np.radians(angle % 360)
        # Shift the point so that center_point becomes the origin
        new_point = (point[0] - center_point[0], point[1] - center_point[1])
        new_point = (
            new_point[0] * np.cos(angle_rad) - new_point[1] * np.sin(angle_rad),
            new_point[0] * np.sin(angle_rad) + new_point[1] * np.cos(angle_rad))
        # Reverse the shifting we have done
        new_point = (
            new_point[0] + center_point[0], new_point[1] + center_point[1])

        return new_point

    # Initialize coordinates
    coords = np.array([
        [0.235, 0.5],
        [0.24, 0.65],
        [0.245, 0.5]])
    # Get centeroid
    #centeroid = coords.mean(axis=0)
    pivot = [0.24, 0.5]
    # Rotate dial about centeroid
    angle = -80 * polarity

    new_coords = np.array([
        rotate_point(coord, angle, center_point=pivot) for coord in coords])

    layout = {
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'shapes': [
            {
                'type': 'path',
                'path': 'M {} {} L {} {} L {} {} Z'.format(*new_coords.flatten()),
                'fillcolor': 'rgba(44, 160, 101, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.23,
                'y': 0.45,
                'text': str(np.round(polarity, 3)),
                'showarrow': False
            }
        ]
    }

    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0

    fig = {"data": [base_chart, meter_chart],
           "layout": layout}

    return fig


def create_boxplot(tweet_df):
    """
        This method will create boxplots for retweets and favorites.

        Args:
            tweet_df (pandas.DataFrame): top tweets

        Returns:
            figure dict object formatted for plotly
    """
    # Setup values boxplots will be created for
    columns = {
        'favorites': 'rgba(93, 164, 214, 0.5)',  # Blue
        'retweets': 'rgba(255, 65, 54, 0.5)'  # Orange
    }
    # Build trace objects
    traces = []
    for key, value in columns.items():
        traces.append(go.Box(
            y=tweet_df[key].values,
            name=key,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=value,
            marker=dict(
                size=2,
            ),
            line=dict(width=1),
        ))
    # Build layout
    layout = go.Layout(
        title='Retweets and Favorites',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=False
    )

    fig = {'data': traces, 'layout': layout}

    return fig
