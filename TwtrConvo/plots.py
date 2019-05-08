"""
This module will create the different plotly objects.
"""

import os
import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff


def create_pie_chart(word_count_1, word_count_2, name_1='Tweet', 
                     name_2='Replies', n=10):
    """
        This method will create two pie charts displaying word frequencies.

        Args:
            word_count_1 (pandas.DataFrame): word count of top tweets
            word_count_2 (pandas.DataFrame): word count of replies

        Returns:
            figure dict object formatted for plotly
    """
    # --- Create Pie Chart with top n terms --- 
    fig = {
      "data": [
        {
          "values": word_count_1['count'].values[:n],
          "labels": word_count_1['word'].values[:n],
          "domain": {"column": 0},
          "hole": .4,
          "type": "pie",
          "name": name_1
        },
        {
          "values": word_count_2['count'].values[:n],
          "labels": word_count_2['word'].values[:n],
          "domain": {"column": 1},
          "hole": .4,
          "type": "pie",
          "name": name_2
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
                    "text": name_1,
                    "x": 0.20,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": name_2,
                    "x": 0.8,
                    "y": 0.5
                }
            ]
        }
    }

    return fig


def _rotate_point(point, angle, center_point=(0, 0)):
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
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    # --- Initialize Gauge Chart Metrics ---
    guage_data = {
        'polarity': {
            'value': polarity,
            'x': [0.0, .48],
            'guage_labels': ["-", "-1", "0", "1"],
            'angle':  -80.0 * polarity,
            'color_labels': ['Polarity', 'Negative', 'Neutral', 'Positive'],
            'colors': [
                'rgb(255, 255, 255)', # Black
                'rgb(255, 102, 102)', # Light Red
                'rgb(192, 192, 192)', # Grey
                'rgb(178, 255, 102)' # Light Green
            ]
        },
        'subjectivity': {
            'value': subjectivity,
            'x': [.52, 1.0],
            'guage_labels': ["-", "0", "0.5", "1"],
            'angle': -80.0 * ((subjectivity * 2) - 1),
            'color_labels': ['Subjectivity', 'Very Objective', 'Neutral',
                             'Very Subjective'],
            'colors': [
                'rgb(255, 255, 255)', # Black
                'rgb(178, 255, 102)', # Light Green
                'rgb(192, 192, 192)', # Grey
                'rgb(255, 102, 102)' # Light Red
            ]
        }
    }
    # --- Initialize Layout ---
    layout = {
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False
        },
        'shapes': [],
        'annotations': []
    }
    # Initialize data list
    data = []
    # Iterate over guage data and create each guage
    for key, values in guage_data.items():
        base_chart = {
            "values": [40, 20, 20, 20],
            "labels": values['guage_labels'],
            "domain": {'x': values['x']},
            "marker": {
                "colors": values['colors'],
                "line": {"width": 0}
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
            "labels": values['color_labels'],
            "marker": {'colors': values['colors']},
            "domain": {"x": values['x']},
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

        # Initialize coordinates
        coords = np.array([
            [values['x'][0] + 0.235, 0.5],
            [values['x'][0] + 0.24, 0.65],
            [values['x'][0] + 0.245, 0.5]])
        pivot = [values['x'][0] + 0.24, 0.5]
        # Rotate dial about centeroid
        new_coords = np.array([
            _rotate_point(coord, values['angle'], center_point=pivot)
            for coord in coords])
        # Create shape
        shape = {
            'type': 'path',
            'path': 'M {} {} L {} {} L {} {} Z'.format(*new_coords.flatten()),
            'fillcolor': 'rgba(44, 160, 101, 0.5)', # Fill triangle green
            'line': {'width': 0.5},
            'xref': 'paper',
            'yref': 'paper'
        }
        # Create annotations
        annotation = {
            'xref': 'paper',
            'yref': 'paper',
            'x': (values['x'][0] + values['x'][1]) / 2,
            'y': 0.45,
            'text': str(np.round(values['value'], 3)),
            'showarrow': False
        }
        # Add objects to layout and data
        layout['shapes'].append(shape)
        layout['annotations'].append(annotation)
        data.append(base_chart)
        data.append(meter_chart)
    # we don't want the boundary now
    base_chart['marker']['line']['width'] = 0
    # Create figure dict
    fig = {"data": data, "layout": layout}

    return fig


def create_boxplot(tweet_df, columns=['retweets', 'favorites'],
                   title='Retweets and Favorites'):
    """
        This method will create boxplots for retweets and favorites.

        Args:
            tweet_df (pandas.DataFrame): top tweets

        Returns:
            figure dict object formatted for plotly
    """
    # Build trace objects
    traces = []
    for header in columns:
        traces.append(go.Box(
            x=tweet_df[header].values,
            name=header,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            line=dict(width=1),
        ))
    # Build layout
    layout = go.Layout(title=title)

    fig = {'data': traces, 'layout': layout}

    return fig


def create_distplot(tweet_df, headers=['net_influence'],
                    bin_sizes = [0.0, 500.0, 1000.0, 5000.0]):
    """
        This method will create a distribution plot given tweets and desired
        list of headers.

        Args:
            tweet_df (pandas.DataFrame): top tweets
            headers (list): list of DataFrame headers for plotting dist
            bin_sizes (list): bin sizes for distribution histogram

        Returns:
            figure dict object formatted for plotly
    """
    # Create list of histogram data arrays
    hist_data = [tweet_df[header].values for header in headers]
    # Create figure
    fig = ff.create_distplot(hist_data, headers, bin_size=bin_sizes)

    return fig


def create_user_description_scatter(user_word_count, n=15):
    """
        This method will create the user description word count scatter
        plot.  This plot will give insight into the backround of the
        profiles whom have the recent top tweets.

        Args:
            user_word_count (pandas.DataFrame): user description word counts
            n (int): number of words that will be shown on plot

        Returns:
            figure dict object formatted for plotly
    """

    data = []
    # Iterate over top n words and plot each
    for index, row in user_word_count.head(n).iterrows():
        trace = go.Scatter(
            x=[row['count']],
            y=[row['avg_net_influence']],
            name=row['word'],
            # Scale the size of the point by the count of words
            marker= {
                'size': row['count'] * 3,
                },
            mode='markers'
            )
        data.append(trace)
    # Create layout
    layout = {
        'title': 'User Description Scatter',
        'xaxis': {'title': 'Count', 'zeroline': False},
        'yaxis': {'title': 'Average Net Influence', 'zeroline': False}
        }

    fig = {'data': data, 'layout': layout}

    return fig


def create_2d_histogram(df, xaxis, yaxis, title):
    """
        This method will create a 2d histogram (heatmap)

        Args:
            df (pandas.DataFrame): data that will be displayed
            xaxis (str): x axis header
            yaxis (str): y axis header
            title (str): plot title

        Returns:
            figure dict object formatted for plotly
    """
    # Create data
    data = [
        go.Histogram2d(
           x=df[xaxis],
           y=df[yaxis]
        )
    ]
    # Create layout
    layout = {
        'title': title,
        'xaxis': {'title': xaxis},
        'yaxis': {'title': yaxis}
    }

    fig = {'data': data, 'layout': layout}

    return fig


def create_violin_plot(df, columns, title):
    """
        This method will create violin plots given a DataFrame and columns.

        Args:
            df (pandas.DataFrame): data that will be displayed
            columns (list): list of columns
            title (str): violin plot title

        Returns:
            figure dict object formatted for plotly
    """
    # Create trace data
    data = []
    for c in columns:
        data.append(
            {
                "type": 'violin',
                "y": df[c],
                #"line": {"color": 'black'},
                "box": {"visible": True},
                "meanline": {"visible": True},
                #"fillcolor": '#8dd3c7',
                "opacity": 0.6,
                "name": c,
                "points": 'all',
                "jitter": 0
            }
        )
    # Create layout
    layout = {
        "title": title,
        "yaxis": {"zeroline": False}
    }

    fig = {'data': data, 'layout': layout}


    return fig
