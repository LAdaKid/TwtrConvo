
# TwtrConvo

TwtrConvo is a python package that utilizes tweepy, pandas, TextBlob, and plotly to generate an overall sentiment of a company (given it's ticker symbol).  It does this by querying for tweets using tweepy and Twitter API keys, then organizing an the tweets using pandas DataFrame, then parsing the text and getting the sentiment using TextBlob and regex, and finally graphically displaying statistics using plotly.

nbviewer link: https://nbviewer.jupyter.org/github/LAdaKid/TwtrConvo/blob/master/README.ipynb

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

       index                   id         username  \
    0     81  1123030520558960640          FedPorn   
    1     60  1123034536252727296         SamAntar   
    2     44  1123040250807422976   NetflixAndLamp   
    3     69  1123033053008240640  whistlerian1834   
    4     47  1123039259911389184         SamAntar   
    
                                                   tweet  \
    0  If I buy a $TSLA do I get back a subsidy that ...   
    1  Crazy Eddie Memoirs: It wouldn’t change a thin...   
    2  My favorite software companies are the ones th...   
    3  $tsla 1/ Here's a summary of my intuition on #...   
    4  I don’t love or hate Elon Musk. For me, he’s s...   
    
                                                    text  favorites  retweets  \
    0  If I buy a TSLA do I get back a subsidy that I...         24         4   
    1  Crazy Eddie Memoirs It wouldn t change a thing...         15         3   
    2  My favorite software companies are the ones th...         47         6   
    3  tsla 1 Here's a summary of my intuition on crc...         45         9   
    4  I don t love or hate Elon Musk For me he s sim...         15         2   
    
       followers  following  net_influence  net_influencerank  retweetsrank  \
    0      15312        582          14730              121.0         122.0   
    1      11290        804          10486              119.5         120.0   
    2       2006        363           1643              104.0         123.5   
    3       1581         80           1501              103.0         125.0   
    4      11290        804          10486              119.5         115.0   
    
       favoritesrank   rank  
    0          122.5  365.5  
    1          116.5  356.0  
    2          125.0  352.5  
    3          124.0  352.0  
    4          116.5  351.0  


### Top Five Tweets and their stats


```python
for i in range(5):
    tweet = tweet_df.iloc[i]
    print(
        tweet['username'],
        '({} Favorites, {} Retweets, Net Influence {}) : \n'.format(
            tweet['favorites'], tweet['retweets'], tweet['net_influence']),
        tweet['tweet'], '\n')
```

    FedPorn (24 Favorites, 4 Retweets, Net Influence 14730) : 
     If I buy a $TSLA do I get back a subsidy that I subsidized? https://t.co/J21hrFjRba 
    
    SamAntar (15 Favorites, 3 Retweets, Net Influence 10486) : 
     Crazy Eddie Memoirs: It wouldn’t change a thing if Wall St. analysts had the opportunity to read 10-Qs before an earnings call because 99.9% of them are stupid. $TSLA $TSLAQ https://t.co/IyyZsC9Lbn 
    
    NetflixAndLamp (47 Favorites, 6 Retweets, Net Influence 1643) : 
     My favorite software companies are the ones that don't actually make software but have single digit gross margins and negative double digit net margins with massive capital intensity. Those are definitely my favorite software companies. They're the best. Bigly. No doubt. $TSLA https://t.co/QgftVO0eGI 
    
    whistlerian1834 (45 Favorites, 9 Retweets, Net Influence 1501) : 
     $tsla 1/ Here's a summary of my intuition on #crcl: I don't believe there's a singular disclosure that is prohibiting a raise. I don't believe the SEC is holding back a raise. Instead, consistent w/ Occam's razor, I believe the puzzle pieces fit as follows: In its first 4 years, 
    
    SamAntar (15 Favorites, 2 Retweets, Net Influence 10486) : 
     I don’t love or hate Elon Musk. For me, he’s simply a source of amusement. I think he’s a dumb crook whose problems are mostly self inflicted. And for the record, I’m not long or short Tesla. $TSLA $TSLAQ https://t.co/y5CIprmak4 
    


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



<div id="28a1aca0-2600-4647-a595-cedd4f609448" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("28a1aca0-2600-4647-a595-cedd4f609448", [{"domain": {"column": 0}, "hole": 0.4, "labels": ["tslaq", "tesla", "'s", "short", "software", "earnings", "think", "1", "amp", "make"], "name": "Tweets", "values": [17, 15, 11, 8, 7, 6, 5, 5, 5, 4], "type": "pie", "uid": "785398ac-bb2e-4a3f-87f1-e9bff25d1008"}, {"domain": {"column": 1}, "hole": 0.4, "labels": ["n't", "people", "also", "'s", "going", "think", "better", "lot", "million", "correct"], "name": "Replies", "values": [5, 4, 4, 4, 3, 3, 3, 3, 3, 3], "type": "pie", "uid": "6f4c7787-926e-4978-bcce-12290e403735"}], {"annotations": [{"font": {"size": 20}, "showarrow": false, "text": "Tweets", "x": 0.2, "y": 0.5}, {"font": {"size": 20}, "showarrow": false, "text": "Replies", "x": 0.8, "y": 0.5}], "grid": {"columns": 2, "rows": 1}, "title": "Word Frequency"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("28a1aca0-2600-4647-a595-cedd4f609448"));});</script>


### Sentiment Gauge

Using TextBlob we will get a general sentiment of all the tweets and display it on a guage using plotly.


```python
fig = TwtrConvo.plots.create_sentiment_gauge(tweet_blob)
iplot(fig)
```


<div id="456b4722-a197-4b96-b395-f3f810f9cc7e" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("456b4722-a197-4b96-b395-f3f810f9cc7e", [{"direction": "clockwise", "domain": {"x": [0, 0.48]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "-1", "0", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 255, 255)", "rgb(255, 255, 255)", "rgb(255, 255, 255)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "2c1d7c8e-a1c6-4ea0-93d2-8d81cf22d8e6"}, {"direction": "clockwise", "domain": {"x": [0, 0.48]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Polarity", "Negative", "Neutral", "Positive"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "744f0402-ed60-4595-9b7f-aa5dac825717"}], {"annotations": [{"showarrow": false, "text": "0.127", "x": 0.23, "xref": "paper", "y": 0.45, "yref": "paper"}], "shapes": [{"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.23507830917069134 0.5008814529940384 L 0.2664435898211511 0.6476507248792593 L 0.24492169082930865 0.49911854700596164 Z", "type": "path", "xref": "paper", "yref": "paper"}], "xaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}, "yaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("456b4722-a197-4b96-b395-f3f810f9cc7e"));});</script>


### Boxplots

Let's take a look at spread of retweets and favorites from the top ranked tweets.


```python
fig = TwtrConvo.plots.create_boxplot(tweet_df)
iplot(fig)
```


<div id="b289d791-1c5b-4d0c-992a-652cc2ebcf48" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("b289d791-1c5b-4d0c-992a-652cc2ebcf48", [{"boxpoints": "all", "fillcolor": "rgba(93, 164, 214, 0.5)", "jitter": 0.5, "line": {"width": 1}, "marker": {"size": 2}, "name": "favorites", "whiskerwidth": 0.2, "y": [24, 15, 47, 45, 15, 15, 20, 24, 6, 11, 18, 6, 22, 4, 7, 12, 5, 7, 6, 5, 15, 4, 5, 3, 4, 9, 4, 6, 13, 5, 2, 5, 2, 3, 2, 1, 5, 1, 6, 5, 4, 2, 1, 1, 2, 2, 0, 2, 1, 0], "type": "box", "uid": "f44db048-decd-4d94-be04-c404f5026d6b"}, {"boxpoints": "all", "fillcolor": "rgba(255, 65, 54, 0.5)", "jitter": 0.5, "line": {"width": 1}, "marker": {"size": 2}, "name": "retweets", "whiskerwidth": 0.2, "y": [4, 3, 6, 9, 2, 1, 2, 3, 2, 3, 6, 1, 1, 1, 2, 1, 2, 2, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], "type": "box", "uid": "21872761-9a4d-4670-b4bb-ae116f73bd32"}], {"margin": {"b": 80, "l": 40, "r": 30, "t": 100}, "paper_bgcolor": "rgb(243, 243, 243)", "plot_bgcolor": "rgb(243, 243, 243)", "showlegend": false, "title": "Retweets and Favorites", "yaxis": {"autorange": true, "dtick": 5, "gridcolor": "rgb(255, 255, 255)", "gridwidth": 1, "showgrid": true, "zeroline": true, "zerolinecolor": "rgb(255, 255, 255)", "zerolinewidth": 2}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("b289d791-1c5b-4d0c-992a-652cc2ebcf48"));});</script>

