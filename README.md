
# TwtrConvo

TwtrConvo is a python package that utilizes tweepy, pandas, TextBlob, and plotly to generate an overall sentiment of a company (given it's ticker symbol).  It does this by querying for tweets using tweepy and Twitter API keys, then organizing an the tweets using pandas DataFrame, then parsing the text and getting the sentiment using TextBlob and regex, and finally graphically displaying statistics using plotly.

## Tweets module (tweets.py)

The tweets module acts as a wrapper layer around tweepy with the main functions:

    get_tweets
    get_replies

### Setup

In order to use this module you will first need to setup your Twitter API keys.  If you don't have Twitter API keys, get them by following this guide:

https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html

Once you get your Twitter API keys you will need to add them to your environment with the variable names:

    TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET

This will allow the TwtrConvo "tweets" module access to the Twitter API in order to query for tweets.

## TwtrConvo module (twtrconvo.py)

The twtrconvo module houses the main logic of the package including the methods to build or load the dataset as well as the ranking function for ranking the tweets that were queried. Let's step through each portion of the main function and show each step in creating the statistical analysis of the company's overall Twitter sentiment.

### Import package and load dataset


```python
import os
import TwtrConvo

ticker = 'TSLA'

# Generally you would use the "build_dataset" method to get tweets and replies, however with
# the default of 500 tweets this generally maxes out you're hourly queries using the Twitter
# API if the ticker has a lot of interaction on Twitter and if you call build_dataset multiple
# times within an hour.  For this reason, you are also able to load previously built data and
# use it to conduct statistical analysis.

#tweet_df, reply_df = twtrconvo.build_dataset(ticker)

tweet_df, reply_df = TwtrConvo.twtrconvo.load_dataset(
    os.path.join(os.getcwd(), 'datasets', ticker)
)

print(tweet_df.head())
```

                        id       username  \
    0  1122625832009097217    TeslaCharts   
    1  1122620038576578562    ElonBachman   
    2  1122628670366134272    QTRResearch   
    3  1122642374180655104  GatorInvestor   
    4  1122640088511524865         JTSEO9   
    
                                                   tweet  \
    0  There will never be a $TSLA robotaxi. https://...   
    1  1\ $TSLA wants Wall Street to look at its 20% ...   
    2  OH ITS JUST SO GREAT $TSLA $TSLAQ https://t.co...   
    3  I am sure it's nothing. Dutch fleet / rental b...   
    4  Did anyone else notice that $TSLA didn't break...   
    
                                                    text  favorites  retweets  \
    0                There will never be a TSLA robotaxi         94         8   
    1  1 TSLA wants Wall Street to look at its 20 aut...         91        14   
    2                    OH ITS JUST SO GREAT TSLA TSLAQ         16         2   
    3  I am sure it s nothing Dutch fleet rental busi...         44        11   
    4  Did anyone else notice that TSLA didn t break ...         29         3   
    
       followers  following  net_influence  net_influencerank  retweetsrank  \
    0      13058       1341          11717              143.0         145.0   
    1       7293        271           7022              139.0         147.0   
    2      56578        999          55579              147.0         137.5   
    3       3009        354           2655              132.0         146.0   
    4       6291        200           6091              137.0         140.5   
    
       favoritesrank   rank  
    0          147.0  435.0  
    1          146.0  432.0  
    2          140.0  424.5  
    3          145.0  423.0  
    4          144.0  421.5  


### Word Frequency

The first thing we'd like to look at is word frequency within the top ranks tweets and their replies.  This could identify any patterns and could point out key words that will effect the current social sentiment that we observe.  We'll use TextBlob and our functions "get_blob" and "get_word_count" to do this then display the word count data using plotly pie charts


```python
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

# Get text blobs and word count
tweet_blob = TwtrConvo.twtrconvo.get_blob(ticker, tweet_df)
tweet_word_count = TwtrConvo.twtrconvo.get_word_count(tweet_blob)
reply_blob = TwtrConvo.twtrconvo.get_blob(ticker, reply_df)
reply_word_count = TwtrConvo.twtrconvo.get_word_count(reply_blob)

# The pie chart will default to the top ten words for each word count unless n is
# specified to be different
fig = TwtrConvo.plots.create_pie_chart(tweet_word_count, reply_word_count)

iplot(fig)
```


<script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script><script type="text/javascript">if (window.MathJax) {MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}</script><script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window._Plotly) {require(['plotly'],function(plotly) {window._Plotly=plotly;});}</script>



<div id="955ff722-bf98-483c-9496-76814edc298b" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("955ff722-bf98-483c-9496-76814edc298b", [{"domain": {"column": 0}, "hole": 0.4, "labels": ["tslaq", "tesla", "fleet", "3", "sales", "please", "model", "going", "volume", "want"], "name": "Tweets", "values": [14, 12, 6, 4, 4, 3, 3, 3, 3, 3], "type": "pie", "uid": "ba5b4492-9fac-4241-8728-1f8e00abfb02"}, {"domain": {"column": 1}, "hole": 0.4, "labels": ["tips", "musk", "tslaq", "woah", "one", "tesla", "equipment", "thing", "everything", "know"], "name": "Replies", "values": [5, 3, 3, 3, 3, 2, 2, 2, 2, 2], "type": "pie", "uid": "6faf6403-7171-4e38-9b5b-d1582c1ed263"}], {"annotations": [{"font": {"size": 20}, "showarrow": false, "text": "Tweets", "x": 0.2, "y": 0.5}, {"font": {"size": 20}, "showarrow": false, "text": "Replies", "x": 0.8, "y": 0.5}], "grid": {"columns": 2, "rows": 1}, "title": "Word Frequency"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("955ff722-bf98-483c-9496-76814edc298b"));});</script>


### Sentiment Gauge

Using TextBlob we will get a general sentiment of all the tweets and display it on a guage using plotly.


```python
fig = TwtrConvo.plots.create_sentiment_gauge(tweet_blob)
iplot(fig)
```


<div id="f2c9415e-e363-46b8-92b5-843dcd67820f" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("f2c9415e-e363-46b8-92b5-843dcd67820f", [{"direction": "clockwise", "domain": {"x": [0, 0.48]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "-1", "0", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 255, 255)", "rgb(255, 255, 255)", "rgb(255, 255, 255)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "3c96dd97-8ac4-4512-a5f0-24e4e165d4dd"}, {"direction": "clockwise", "domain": {"x": [0, 0.48]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Polarity", "Negative", "Neutral", "Positive"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "145f069d-c34f-4611-ac17-594cfd2b2714"}], {"annotations": [{"showarrow": false, "text": "0.131", "x": 0.23, "xref": "paper", "y": 0.45, "yref": "paper"}], "shapes": [{"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.23508279040511593 0.5009061179834768 L 0.267183539504304 0.647516287846522 L 0.24491720959488406 0.4990938820165232 Z", "type": "path", "xref": "paper", "yref": "paper"}], "xaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}, "yaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("f2c9415e-e363-46b8-92b5-843dcd67820f"));});</script>

