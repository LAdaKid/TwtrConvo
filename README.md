
# TwtrConvo

TwtrConvo is a python package that utilizes tweepy, pandas, TextBlob, and plotly to query for the latest top tweets corresponding to a public company (given it's ticker symbol) and provides various interactive plots to display overall sentiment and metrics on the Twitter conversation surrounding the company.  

To accomplish this the library:
    - first, queries for tweets using tweepy and the user's Twitter API keys
    - second, organizes the tweets and their metadata using pandas DataFrames
    - third, parses and cleans the text then calculates the sentiment using TextBlob and regex
    - forth and finally, graphically displays the results using plotly.

nbviewer link: https://nbviewer.jupyter.org/github/LAdaKid/TwtrConvo/blob/master/README.ipynb

### Setup

In order to use this module you will first need to setup your Twitter API keys.  If you don't have Twitter API keys, get them by following this guide:

https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html

Once you get your Twitter API keys you will need to add them to your environment with the variable names:

    TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET

This will allow the TwtrConvo "tweets" module access to the Twitter API in order to query for tweets.

### Importing packages

For this jupyter-notebook we'll just import the TwtrConvo package along with the os library for path manipulation as well as some plotly utilities for creating offline plots within the notebook.


```python
import os
import TwtrConvo
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

# Now let's initialize the ticker for the company we'd like to analyze
ticker = 'TSLA'
```


<script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script><script type="text/javascript">if (window.MathJax) {MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}</script><script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window._Plotly) {require(['plotly'],function(plotly) {window._Plotly=plotly;});}</script>


## Tweets module (tweets.py)

The tweets module acts as a wrapper layer around tweepy with the main function "get_tweets".  This method allows the user to query for "n" number of tweets, then by default will filter tweets tagged as retweets and organize the remaining tweets into lists: regular tweets and replies.  You can change the total tweets that will be returned in the query by using the "max_tweets" keyword argument.  The tweets and replies will both be organized into lists of dictionaries matching the json format of the Twitter API.  For more documentation on this visit the link below.

Twitter developer API docs: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object


```python
# Get the raw tweets and replies using the "tweets.get_tweets" method
tweet_list, reply_list = TwtrConvo.tweets.get_tweets(ticker, max_tweets=10)

# Let's take a look at one of the tweets that get's returned directly from Twitter
print(tweet_list[0])
```

    {'created_at': 'Wed May 08 03:06:02 +0000 2019', 'id': 1125960018002468864, 'id_str': '1125960018002468864', 'full_text': 'I believe Trump will announce Sunday a 50% Tariffs increase across the board on China exports, out of anger. Do you believe this is appropriate means of negotiations. $bidu $baba $jd $mmm $cnc $antm $khc $ge $x $ttm $cgc $nvda $aapl $regn $tsla @jimcramer', 'truncated': False, 'display_text_range': [0, 255], 'entities': {'hashtags': [], 'symbols': [{'text': 'bidu', 'indices': [167, 172]}, {'text': 'baba', 'indices': [173, 178]}, {'text': 'jd', 'indices': [179, 182]}, {'text': 'mmm', 'indices': [183, 187]}, {'text': 'cnc', 'indices': [188, 192]}, {'text': 'antm', 'indices': [193, 198]}, {'text': 'khc', 'indices': [199, 203]}, {'text': 'ge', 'indices': [204, 207]}, {'text': 'x', 'indices': [208, 210]}, {'text': 'ttm', 'indices': [211, 215]}, {'text': 'cgc', 'indices': [216, 220]}, {'text': 'nvda', 'indices': [221, 226]}, {'text': 'aapl', 'indices': [227, 232]}, {'text': 'regn', 'indices': [233, 238]}, {'text': 'tsla', 'indices': [239, 244]}], 'user_mentions': [{'screen_name': 'jimcramer', 'name': 'Jim Cramer', 'id': 14216123, 'id_str': '14216123', 'indices': [245, 255]}], 'urls': []}, 'metadata': {'iso_language_code': 'en', 'result_type': 'recent'}, 'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 3241885086, 'id_str': '3241885086', 'name': 'JRD', 'screen_name': 'JoeRDiaz2', 'location': 'United States', 'description': 'Very contrarian', 'url': None, 'entities': {'description': {'urls': []}}, 'protected': False, 'followers_count': 72, 'friends_count': 54, 'listed_count': 3, 'created_at': 'Thu Jun 11 04:18:48 +0000 2015', 'favourites_count': 182, 'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'verified': False, 'statuses_count': 201, 'lang': 'en', 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': 'C0DEED', 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1018642410664947712/89fAc4yB_normal.jpg', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1018642410664947712/89fAc4yB_normal.jpg', 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': True, 'default_profile': True, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 0, 'favorite_count': 0, 'favorited': False, 'retweeted': False, 'lang': 'en'}


## TwtrConvo module (twtrconvo.py)

The twtrconvo module houses the main logic of the package including the methods to either build a new dataset or load an existing dataset.  The datasets are composed of:

    tweet_df: the "n" top tweets ranked by retweets, favorites, and net influence (followers - following)
    reply_df: the replies to the top tweets (includes same fields as tweet_df with addition of id of original tweet the reply corresponds to
    user_df: user information corresponding to the top tweets
    
Let's step through each portion of the main functionality (which can be found within the "twtrconvo.main" method) and show each step in the analysis of the recent Twitter conversation surrounding the company.

### Loading datasets

Generally you would use the "build_dataset" method to get the tweet_df, reply_df, and user_df, however with the default set to 2500 tweets can quickly max out you're hourly queries using the Twitter API if you call build_dataset multiple times within an hour (the hourly limit is 100 queries without paying for a premium account).  For this reason, you are also able to load previously built data and use it to conduct statistical analysis.


```python
# Build new dataset
#tweet_df, reply_df, user_df = twtrconvo.build_dataset(ticker)

# Load existing dataset
tweet_df, reply_df, user_df = TwtrConvo.twtrconvo.load_dataset(
    os.path.join(os.getcwd(), 'datasets', ticker)
)
# Let's take a look at what fields the tweet_df contains
tweet_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>id</th>
      <th>username</th>
      <th>user_id</th>
      <th>tweet</th>
      <th>text</th>
      <th>favorites</th>
      <th>retweets</th>
      <th>followers</th>
      <th>following</th>
      <th>polarity</th>
      <th>subjectivity</th>
      <th>net_influence</th>
      <th>net_influencerank</th>
      <th>retweetsrank</th>
      <th>favoritesrank</th>
      <th>rank</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>955</td>
      <td>1125754099390078979</td>
      <td>Teslarati</td>
      <td>1308211178</td>
      <td>Elon Musk confirms $25 million $TSLA purchase,...</td>
      <td>Elon Musk confirms 25 million TSLA purchase bo...</td>
      <td>554</td>
      <td>65</td>
      <td>90528</td>
      <td>72</td>
      <td>0.100000</td>
      <td>0.400000</td>
      <td>90456</td>
      <td>1029.0</td>
      <td>1038.0</td>
      <td>1038.0</td>
      <td>3105.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>953</td>
      <td>1125754190930821120</td>
      <td>WallStCynic</td>
      <td>1961333743</td>
      <td>Who wants to tell the guys on TV that the effe...</td>
      <td>Who wants to tell the guys on TV that the effe...</td>
      <td>255</td>
      <td>36</td>
      <td>27872</td>
      <td>866</td>
      <td>0.400000</td>
      <td>0.450000</td>
      <td>27006</td>
      <td>1015.0</td>
      <td>1037.0</td>
      <td>1037.0</td>
      <td>3089.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>744</td>
      <td>1125785546817560576</td>
      <td>GerberKawasaki</td>
      <td>349249475</td>
      <td>Help me here. Is the new Audi Etron commercial...</td>
      <td>Help me here Is the new Audi Etron commercial ...</td>
      <td>104</td>
      <td>11</td>
      <td>58959</td>
      <td>4666</td>
      <td>0.188258</td>
      <td>0.288636</td>
      <td>54293</td>
      <td>1022.5</td>
      <td>1027.0</td>
      <td>1034.0</td>
      <td>3083.5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>13</td>
      <td>1125948002055548929</td>
      <td>GerberKawasaki</td>
      <td>349249475</td>
      <td>Tesla (TSLA) is going to get up to $2 billion ...</td>
      <td>Tesla TSLA is going to get up to 2 billion fro...</td>
      <td>41</td>
      <td>10</td>
      <td>58959</td>
      <td>4666</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>54293</td>
      <td>1022.5</td>
      <td>1024.5</td>
      <td>1007.0</td>
      <td>3054.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>861</td>
      <td>1125768109653209090</td>
      <td>SamAntar</td>
      <td>17893558</td>
      <td>If @PlugInFUD was around during the Crazy Eddi...</td>
      <td>If was around during the Crazy Eddie days I mi...</td>
      <td>86</td>
      <td>14</td>
      <td>11522</td>
      <td>810</td>
      <td>-0.445833</td>
      <td>0.720833</td>
      <td>10712</td>
      <td>987.0</td>
      <td>1030.0</td>
      <td>1031.0</td>
      <td>3048.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Now let's take a look at what fields are contained within the user_df
user_df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>username</th>
      <th>favorites</th>
      <th>followers</th>
      <th>following</th>
      <th>full_description</th>
      <th>tweet_count</th>
      <th>user_id</th>
      <th>description</th>
      <th>net_influence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>10minutetrading</td>
      <td>2993</td>
      <td>2776</td>
      <td>180</td>
      <td>🥇Awarded Top 💯 People in Finance💰 Tools, Tips ...</td>
      <td>14231</td>
      <td>19242782</td>
      <td>Awarded Top People in Finance Tools Tips Trick...</td>
      <td>2596</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4xRevenue</td>
      <td>8259</td>
      <td>871</td>
      <td>460</td>
      <td>The best PMs are analysts who have yet to mana...</td>
      <td>6203</td>
      <td>457483584</td>
      <td>The best PMs are analysts who have yet to mana...</td>
      <td>411</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AlephBlog</td>
      <td>2</td>
      <td>13166</td>
      <td>222</td>
      <td>The two main goals: teaching investors about b...</td>
      <td>27363</td>
      <td>120209971</td>
      <td>The two main goals teaching investors about be...</td>
      <td>12944</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Alpsoy66</td>
      <td>8203</td>
      <td>461</td>
      <td>302</td>
      <td>Consulting, IT, Cloud, A.I. Bootloader, On twi...</td>
      <td>5952</td>
      <td>302045293</td>
      <td>Consulting IT Cloud A I Bootloader On twitter ...</td>
      <td>159</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AlterViggo</td>
      <td>13677</td>
      <td>2178</td>
      <td>246</td>
      <td>I like, you know, facts. And science. And bett...</td>
      <td>4814</td>
      <td>983380841484042241</td>
      <td>I like you know facts And science And better cars</td>
      <td>1932</td>
    </tr>
  </tbody>
</table>
</div>



### Top 10 Tweets and their stats

Let's take a look at some of the top tweets.  This is a good starting point to get a feel for any recent news or sentiment of the company.


```python
for i in range(10):
    tweet = tweet_df.iloc[i]
    print(
        tweet['username'],
        '({} Favorites, {} Retweets, Net Influence {}, Polarity {:.3f}, Subjectivity {:.3f}): \n'.format(
            tweet['favorites'], tweet['retweets'], tweet['net_influence'], tweet['polarity'],
            tweet['subjectivity']),
        tweet['tweet'], '\n')
```

    Teslarati (554 Favorites, 65 Retweets, Net Influence 90456, Polarity 0.100, Subjectivity 0.400): 
     Elon Musk confirms $25 million $TSLA purchase, boosts Tesla stake to nearly 20%
    https://t.co/YOy6UqBMkF 
    
    WallStCynic (255 Favorites, 36 Retweets, Net Influence 27006, Polarity 0.400, Subjectivity 0.450): 
     Who wants to tell the guys on TV that the effective cost of capital on the $TSLA convert was over 8%, not the 2% coupon? 
    
    GerberKawasaki (104 Favorites, 11 Retweets, Net Influence 54293, Polarity 0.188, Subjectivity 0.289): 
     Help me here. Is the new Audi Etron commercial using a car you can’t buy in America. Is that legal? I see some fine print in the ad saying this. You Tesla peeps see these Audi EV ads? Seems deceptive to advertise a car that Americans can’t buy? $tsla 
    
    GerberKawasaki (41 Favorites, 10 Retweets, Net Influence 54293, Polarity 0.000, Subjectivity 0.000): 
     Tesla (TSLA) is going to get up to $2 billion from Fiat-Chrysler to meet emission standards. Bet you didn’t have this molded in. #tesla $tsla  https://t.co/u0WYROgbWj 
    
    SamAntar (86 Favorites, 14 Retweets, Net Influence 10712, Polarity -0.446, Subjectivity 0.721): 
     If @PlugInFUD was around during the Crazy Eddie days, I might have had a hard time defrauding investors. $TSLA $TSLAQ https://t.co/3JLjnWUTKl 
    
    howardlindzon (72 Favorites, 4 Retweets, Net Influence 252326, Polarity 0.125, Subjectivity 0.217): 
     My first big profit on @onrallyrd investment in a collector car ...screw $tsla .... https://t.co/tU6aSomXyp 
    
    GerberKawasaki (33 Favorites, 9 Retweets, Net Influence 54293, Polarity 0.000, Subjectivity 0.000): 
     Please read, we need to do something about #climatechange and you CAN make a difference. #Tesla $TSLA https://t.co/Jv7JXo9lu0 
    
    markbspiegel (51 Favorites, 8 Retweets, Net Influence 12100, Polarity 0.191, Subjectivity 0.570): 
     Not only is this incredibly deceptive, but absolutely nowhere (much less in LARGE LETTERS) does it say that for now and the foreseeable future drivers must keep both hands on the wheel at all times. Keep killing people, @elonmusk. You'll pay monetarily &amp; with your freedom.
    $TSLA https://t.co/rbudjp2R6G 
    
    pierpont_morgan (51 Favorites, 13 Retweets, Net Influence 8426, Polarity -0.050, Subjectivity 0.200): 
     $TSLA 2025 bond giving back capital raise gains, with spread to UST 5bp off record wide. https://t.co/3LnzXXgU4f 
    
    WallStCynic (46 Favorites, 5 Retweets, Net Influence 27005, Polarity 0.000, Subjectivity 0.000): 
     In case you didn’t think the $TSLA narrative is “officially” changing... https://t.co/4wMlByuAbC 
    


### User Data

Next let's take a look at some data on the types of Twitter users that are tweeting about the company with the most influence.  By creating a visualization that displays the relationship between the number of times a term is mentioned in user profile descriptions and the average net influence of those users we can get an idea of the type of profiles participating in the conversation.


```python
user_blob = TwtrConvo.twtrconvo.get_blob(ticker, user_df, header='description')
user_word_count = TwtrConvo.twtrconvo.get_word_count(user_blob)
user_word_count = TwtrConvo.twtrconvo.add_user_data(user_word_count, user_df)

fig = TwtrConvo.plots.create_user_description_scatter(user_word_count)

iplot(fig)
```


<div id="0ecd1362-e2a2-4441-9dee-1cf728cd4893" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("0ecd1362-e2a2-4441-9dee-1cf728cd4893", [{"marker": {"size": 36}, "mode": "markers", "name": "advice", "x": [12], "y": [5699.166666666667], "type": "scatter", "uid": "5f3f9985-e84c-4750-aa11-ec3e721faa8a"}, {"marker": {"size": 36}, "mode": "markers", "name": "options", "x": [12], "y": [3813.5], "type": "scatter", "uid": "c497a30e-9fb9-47d8-b8a7-6d28d2589fd8"}, {"marker": {"size": 36}, "mode": "markers", "name": "trader", "x": [12], "y": [4766.153846153846], "type": "scatter", "uid": "1d3f0caa-3df5-4265-955b-0185251c642a"}, {"marker": {"size": 33}, "mode": "markers", "name": "tesla", "x": [11], "y": [8132.0], "type": "scatter", "uid": "f200e899-cd9c-4200-8f55-29761dbe3019"}, {"marker": {"size": 33}, "mode": "markers", "name": "investment", "x": [11], "y": [9112.153846153846], "type": "scatter", "uid": "8c53a948-c81f-4068-91d2-9fc0fc0af041"}, {"marker": {"size": 30}, "mode": "markers", "name": "trading", "x": [10], "y": [10216.857142857143], "type": "scatter", "uid": "ee45d40a-744b-4b15-ab93-ef2101e13e13"}, {"marker": {"size": 30}, "mode": "markers", "name": "investor", "x": [10], "y": [9051.636363636364], "type": "scatter", "uid": "ba413778-4f49-4407-a336-10d3560fb746"}, {"marker": {"size": 30}, "mode": "markers", "name": "short", "x": [10], "y": [2834.909090909091], "type": "scatter", "uid": "c30c6608-e923-4325-8ec1-0af86925e96f"}, {"marker": {"size": 27}, "mode": "markers", "name": "tslaq", "x": [9], "y": [1311.5555555555557], "type": "scatter", "uid": "cc3c705b-9f77-4156-ad12-5ca7cc64592b"}, {"marker": {"size": 27}, "mode": "markers", "name": "stock", "x": [9], "y": [8957.92857142857], "type": "scatter", "uid": "fb6915cf-fc78-4076-a0e6-9b8f68038db1"}, {"marker": {"size": 24}, "mode": "markers", "name": "long", "x": [8], "y": [3448.0], "type": "scatter", "uid": "33006293-6f42-42f9-98e6-f6e784058389"}, {"marker": {"size": 24}, "mode": "markers", "name": "owner", "x": [8], "y": [2157.625], "type": "scatter", "uid": "b2fa619a-2814-4cd1-914d-d4de3e82315d"}, {"marker": {"size": 24}, "mode": "markers", "name": "trade", "x": [8], "y": [4277.45], "type": "scatter", "uid": "5393f3d8-3a3d-4042-9c80-8891a279fe65"}, {"marker": {"size": 21}, "mode": "markers", "name": "stocks", "x": [7], "y": [5869.0], "type": "scatter", "uid": "61a29464-3972-4462-af0b-ccd7671aadf8"}, {"marker": {"size": 21}, "mode": "markers", "name": "market", "x": [7], "y": [10760.0], "type": "scatter", "uid": "37e14b7d-b217-4bc6-a5a7-05c15ef9cd49"}], {"title": "User Description Scatter", "xaxis": {"title": "Count", "zeroline": false}, "yaxis": {"title": "Average Net Influence", "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("0ecd1362-e2a2-4441-9dee-1cf728cd4893"));});</script>


Now let's get an idea of the general influence of most of our top tweeters by looking at a distribution of net influence of our users.


```python
fig = TwtrConvo.plots.create_distplot(user_df)
iplot(fig)
```


<div id="448f31a6-f053-4371-9cd6-c81efbfa946b" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("448f31a6-f053-4371-9cd6-c81efbfa946b", [{"autobinx": false, "histnorm": "probability density", "legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)"}, "name": "net_influence", "opacity": 0.7, "x": [2596, 411, 12944, 159, 1932, 1474, 19314, 1420, 349, 865, 1129, 84445, 83, 1772, 382, 3111, 17300, 578, 62, 155, 1204, 10292, 2812, 54293, 1222, 6458, 6983, 1096, 1954, 1299, 4335, 267, 655, 688, 7808, 2209, 2382, 13773, 153, 496, 41435, 19986, 711, 1951, 3003, 4593, 3646, 12522, 2512, 2163, 1102, 105, 158, 10712, 7742, 1364, 47, 67, 6829, 28, 714, 1168, 1997, 90456, 2618, 322, 1451, 550, 607, 6079, 321, 1593, 1114, 4644, 344, 3382, -3, 27006, 2230, 849138, -59, 238, 1713, 1122, 9281, 13314, 15472, 2688, 14411, 10612, 1502, 1346, 27, 252326, 15638, 12100, 604, 2609, 283, 1630, 8426, 2548, 719, 8079, 354, 817, 125, 18964, 116, 231, 226, 549, 4978, 582, 521], "xaxis": "x", "xbins": {"end": 849138.0, "size": 0.0, "start": -59.0}, "yaxis": "y", "type": "histogram", "uid": "dd258bc0-0249-4e5b-a8c0-6fd2bca43c75"}, {"legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)"}, "mode": "lines", "name": "net_influence", "showlegend": false, "x": [-59.0, 1639.394, 3337.788, 5036.182, 6734.576, 8432.97, 10131.364, 11829.758, 13528.152, 15226.546, 16924.94, 18623.334, 20321.728, 22020.122, 23718.516, 25416.91, 27115.304, 28813.698, 30512.092, 32210.486, 33908.88, 35607.274, 37305.668, 39004.062, 40702.456, 42400.85, 44099.244, 45797.638, 47496.032, 49194.426, 50892.82, 52591.214, 54289.608, 55988.002, 57686.396, 59384.79, 61083.184, 62781.578, 64479.972, 66178.366, 67876.76, 69575.154, 71273.548, 72971.942, 74670.336, 76368.73, 78067.124, 79765.518, 81463.912, 83162.306, 84860.7, 86559.094, 88257.488, 89955.882, 91654.276, 93352.67, 95051.064, 96749.458, 98447.852, 100146.246, 101844.64, 103543.034, 105241.428, 106939.822, 108638.216, 110336.61, 112035.004, 113733.398, 115431.792, 117130.186, 118828.58, 120526.974, 122225.368, 123923.762, 125622.156, 127320.55, 129018.944, 130717.338, 132415.732, 134114.126, 135812.52, 137510.914, 139209.308, 140907.702, 142606.096, 144304.49, 146002.884, 147701.278, 149399.672, 151098.066, 152796.46, 154494.854, 156193.248, 157891.642, 159590.036, 161288.43, 162986.824, 164685.218, 166383.612, 168082.006, 169780.4, 171478.794, 173177.188, 174875.582, 176573.976, 178272.37, 179970.764, 181669.158, 183367.552, 185065.946, 186764.34, 188462.734, 190161.128, 191859.522, 193557.916, 195256.31, 196954.704, 198653.098, 200351.492, 202049.886, 203748.28, 205446.674, 207145.068, 208843.462, 210541.856, 212240.25, 213938.644, 215637.038, 217335.432, 219033.826, 220732.22, 222430.614, 224129.008, 225827.402, 227525.796, 229224.19, 230922.584, 232620.978, 234319.372, 236017.766, 237716.16, 239414.554, 241112.948, 242811.342, 244509.736, 246208.13, 247906.524, 249604.918, 251303.312, 253001.706, 254700.1, 256398.494, 258096.888, 259795.282, 261493.676, 263192.07, 264890.464, 266588.858, 268287.252, 269985.646, 271684.04, 273382.434, 275080.828, 276779.222, 278477.616, 280176.01, 281874.404, 283572.798, 285271.192, 286969.586, 288667.98, 290366.374, 292064.768, 293763.162, 295461.556, 297159.95, 298858.344, 300556.738, 302255.132, 303953.526, 305651.92, 307350.314, 309048.708, 310747.102, 312445.496, 314143.89, 315842.284, 317540.678, 319239.072, 320937.466, 322635.86, 324334.254, 326032.648, 327731.042, 329429.436, 331127.83, 332826.224, 334524.618, 336223.012, 337921.406, 339619.8, 341318.194, 343016.588, 344714.982, 346413.376, 348111.77, 349810.164, 351508.558, 353206.952, 354905.346, 356603.74, 358302.134, 360000.528, 361698.922, 363397.316, 365095.71, 366794.104, 368492.498, 370190.892, 371889.286, 373587.68, 375286.074, 376984.468, 378682.862, 380381.256, 382079.65, 383778.044, 385476.438, 387174.832, 388873.226, 390571.62, 392270.014, 393968.408, 395666.802, 397365.196, 399063.59, 400761.984, 402460.378, 404158.772, 405857.166, 407555.56, 409253.954, 410952.348, 412650.742, 414349.136, 416047.53, 417745.924, 419444.318, 421142.712, 422841.106, 424539.5, 426237.894, 427936.288, 429634.682, 431333.076, 433031.47, 434729.864, 436428.258, 438126.652, 439825.046, 441523.44, 443221.834, 444920.228, 446618.622, 448317.016, 450015.41, 451713.804, 453412.198, 455110.592, 456808.986, 458507.38, 460205.774, 461904.168, 463602.562, 465300.956, 466999.35, 468697.744, 470396.138, 472094.532, 473792.926, 475491.32, 477189.714, 478888.108, 480586.502, 482284.896, 483983.29, 485681.684, 487380.078, 489078.472, 490776.866, 492475.26, 494173.654, 495872.048, 497570.442, 499268.836, 500967.23, 502665.624, 504364.018, 506062.412, 507760.806, 509459.2, 511157.594, 512855.988, 514554.382, 516252.776, 517951.17, 519649.564, 521347.958, 523046.352, 524744.746, 526443.14, 528141.534, 529839.928, 531538.322, 533236.716, 534935.11, 536633.504, 538331.898, 540030.292, 541728.686, 543427.08, 545125.474, 546823.868, 548522.262, 550220.656, 551919.05, 553617.444, 555315.838, 557014.232, 558712.626, 560411.02, 562109.414, 563807.808, 565506.202, 567204.596, 568902.99, 570601.384, 572299.778, 573998.172, 575696.566, 577394.96, 579093.354, 580791.748, 582490.142, 584188.536, 585886.93, 587585.324, 589283.718, 590982.112, 592680.506, 594378.9, 596077.294, 597775.688, 599474.082, 601172.476, 602870.87, 604569.264, 606267.658, 607966.052, 609664.446, 611362.84, 613061.234, 614759.628, 616458.022, 618156.416, 619854.81, 621553.204, 623251.598, 624949.992, 626648.386, 628346.78, 630045.174, 631743.568, 633441.962, 635140.356, 636838.75, 638537.144, 640235.538, 641933.932, 643632.326, 645330.72, 647029.114, 648727.508, 650425.902, 652124.296, 653822.69, 655521.084, 657219.478, 658917.872, 660616.266, 662314.66, 664013.054, 665711.448, 667409.842, 669108.236, 670806.63, 672505.024, 674203.418, 675901.812, 677600.206, 679298.6, 680996.994, 682695.388, 684393.782, 686092.176, 687790.57, 689488.964, 691187.358, 692885.752, 694584.146, 696282.54, 697980.934, 699679.328, 701377.722, 703076.116, 704774.51, 706472.904, 708171.298, 709869.692, 711568.086, 713266.48, 714964.874, 716663.268, 718361.662, 720060.056, 721758.45, 723456.844, 725155.238, 726853.632, 728552.026, 730250.42, 731948.814, 733647.208, 735345.602, 737043.996, 738742.39, 740440.784, 742139.178, 743837.572, 745535.966, 747234.36, 748932.754, 750631.148, 752329.542, 754027.936, 755726.33, 757424.724, 759123.118, 760821.512, 762519.906, 764218.3, 765916.694, 767615.088, 769313.482, 771011.876, 772710.27, 774408.664, 776107.058, 777805.452, 779503.846, 781202.24, 782900.634, 784599.028, 786297.422, 787995.816, 789694.21, 791392.604, 793090.998, 794789.392, 796487.786, 798186.18, 799884.574, 801582.968, 803281.362, 804979.756, 806678.15, 808376.544, 810074.938, 811773.332, 813471.726, 815170.12, 816868.514, 818566.908, 820265.302, 821963.696, 823662.09, 825360.484, 827058.878, 828757.272, 830455.666, 832154.06, 833852.454, 835550.848, 837249.242, 838947.636, 840646.03, 842344.424, 844042.818, 845741.212, 847439.606], "xaxis": "x", "y": [1.163608499729609e-05, 1.1696835617752144e-05, 1.1726291935852163e-05, 1.1724275819671527e-05, 1.1690867198464444e-05, 1.1626402607156215e-05, 1.1531470230259743e-05, 1.1406901544212011e-05, 1.1253759721325843e-05, 1.1073325018665235e-05, 1.0867077429748913e-05, 1.0636676924803213e-05, 1.0383941645261193e-05, 1.0110824449509288e-05, 9.819388228936819e-06, 9.511780425829925e-06, 9.190207187520705e-06, 8.856907584662461e-06, 8.514128306009997e-06, 8.164099218319441e-06, 7.809010148823524e-06, 7.450989210224852e-06, 7.092082945450298e-06, 6.734238522775878e-06, 6.379288162664243e-06, 6.0289359270594824e-06, 5.684746951229366e-06, 5.348139148736082e-06, 5.020377372857967e-06, 4.7025699737546825e-06, 4.3956676507000036e-06, 4.100464463470904e-06, 3.817600836982057e-06, 3.547568368821039e-06, 3.290716230633822e-06, 3.047258941332386e-06, 2.817285282699712e-06, 2.6007681258720975e-06, 2.3975749399919564e-06, 2.207478761561453e-06, 2.0301694141331687e-06, 1.8652647823455866e-06, 1.7123219613187504e-06, 1.5708481214330787e-06, 1.4403109488985308e-06, 1.3201485436864892e-06, 1.2097786777900673e-06, 1.10860733789948e-06, 1.0160364969882606e-06, 9.314710786305385e-07, 8.543250958045426e-07, 7.840269622479991e-07, 7.200239889486842e-07, 6.617860909733695e-07, 6.088087405143505e-07, 5.606152107701759e-07, 5.167581621269955e-07, 4.7682062715771023e-07, 4.4041645432688597e-07, 4.0719027212242423e-07, 3.7681703578871346e-07, 3.49001218078913e-07, 3.2347570364874525e-07, 3.0000044405285756e-07, 2.783609269446135e-07, 2.5836650918031165e-07, 2.3984865923762617e-07, 2.2265914981139061e-07, 2.0666823676963371e-07, 1.9176285594650852e-07, 1.7784486460923273e-07, 1.6482934994168517e-07, 1.526430226022686e-07, 1.4122270938926574e-07, 1.3051395532213613e-07, 1.2046974204984192e-07, 1.1104932644503713e-07, 1.0221720054459116e-07, 9.394217165337909e-08, 8.619655943379312e-08, 7.895550514651211e-08, 7.219638687256254e-08, 6.58983335126371e-08, 6.004182960413185e-08, 5.4608402494399e-08, 4.9580383133854967e-08, 4.494073167765589e-08, 4.0672919182322155e-08, 3.676085692700802e-08, 3.3188865251996736e-08, 2.994167426463928e-08, 2.7004449292173724e-08, 2.436283454039887e-08, 2.2003009027919226e-08, 1.991174949082344e-08, 1.8076495577807477e-08, 1.6485413268957506e-08, 1.5127453043132796e-08, 1.3992399881950723e-08, 1.3070912727788083e-08, 1.2354551506022105e-08, 1.1835790276785453e-08, 1.1508015499197105e-08, 1.1365508773012175e-08, 1.1403413771535442e-08, 1.1617687398749366e-08, 1.2005035496560509e-08, 1.2562833698573095e-08, 1.328903427834906e-08, 1.4182060075750074e-08, 1.524068680705222e-08, 1.6463915274621006e-08, 1.785083519062208e-08, 1.9400482516091795e-08, 2.1111692390231985e-08, 2.2982949882561455e-08, 2.5012240939178935e-08, 2.719690600973175e-08, 2.9533498929024218e-08, 3.201765368146865e-08, 3.464396169260973e-08, 3.7405862264750484e-08, 4.029554869874786e-08, 4.330389251756067e-08, 4.6420388026376e-08, 4.963311920765438e-08, 5.292875065724742e-08, 5.6292543921553354e-08, 5.970840019895867e-08, 6.315892992686722e-08, 6.662554929555402e-08, 7.008860322072292e-08, 7.352751377838077e-08, 7.692095257017052e-08, 8.024703495736338e-08, 8.348353359070453e-08, 8.660810818492197e-08, 8.959854805447774e-08, 9.243302355400297e-08, 9.509034226470575e-08, 9.755020554730008e-08, 9.979346095122656e-08, 1.0180234593546772e-07, 1.0356071842194674e-07, 1.0505426986948883e-07, 1.0627071682295118e-07, 1.0719996725387843e-07, 1.0783425845864724e-07, 1.0816826380764518e-07, 1.0819916623237877e-07, 1.0792669698231812e-07, 1.0735313886398259e-07, 1.0648329387436407e-07, 1.053244158418056e-07, 1.0388610937236814e-07, 1.0218019705148925e-07, 1.002205574533216e-07, 9.802293704899003e-08, 9.560473956749204e-08, 9.298479673874032e-08, 9.018312462953407e-08, 8.722066996500918e-08, 8.411905090820306e-08, 8.090029674944308e-08, 7.758659083878764e-08, 7.42000208847204e-08, 7.076234044906795e-08, 6.729474510198853e-08, 6.381766627379156e-08, 6.035058536538043e-08, 5.6911870170119836e-08, 5.3518635131004985e-08, 5.0186626422163396e-08, 4.693013231632348e-08, 4.3761918792459626e-08, 4.0693189861566216e-08, 3.773357165317032e-08, 3.4891118918744e-08, 3.2172342276814697e-08, 2.9582254252532776e-08, 2.7124431954135026e-08, 2.4801094080646197e-08, 2.26131898681389e-08, 2.0560497553171807e-08, 1.8641729957603323e-08, 1.6854644873624203e-08, 1.519615804553665e-08, 1.366245669884021e-08, 1.2249111750551046e-08, 1.0951187040204801e-08, 9.763344141625869e-09, 8.679941544502855e-09, 7.695127225793584e-09, 6.8029238582705425e-09, 5.997306122107929e-09, 5.272269791057025e-09, 4.621892454037878e-09, 4.0403859032746044e-09, 3.522140369618224e-09, 3.0617609133786834e-09, 2.654096384482634e-09, 2.294261449353736e-09, 1.9776522443948442e-09, 1.6999562585912294e-09, 1.4571570721669145e-09, 1.2455345862814473e-09, 1.0616613724995236e-09, 9.023957523327647e-10, 7.648721886950859e-10, 6.464895347328562e-10, 5.448976431942173e-10, 4.579827931487739e-10, 3.838523421483525e-10, 3.208189623224217e-10, 2.6738476971321794e-10, 2.2222560844697722e-10, 1.8417570597327443e-10, 1.5221287324783084e-10, 1.2544438486407975e-10, 1.0309363906461987e-10, 8.448766644657473e-11, 6.904552904691257e-11, 5.626762828064043e-11, 4.57259207452148e-11, 3.7055024971092354e-11, 2.994418951497212e-11, 2.4130083051208174e-11, 1.9390359992648928e-11, 1.5537950334298138e-11, 1.2416019536004232e-11, 9.893543031306459e-12, 7.861440075090406e-12, 6.229212852930325e-12, 4.922038826283964e-12, 3.87826696426408e-12, 3.0472716268302622e-12, 2.387621255797079e-12, 1.8655225651477762e-12, 1.4535044913718303e-12, 1.1293096807889722e-12, 8.749646869218614e-13, 6.760032772491026e-13, 5.208202704816871e-13, 4.001361209124248e-13, 3.0655502392479234e-13, 2.3420163338886595e-13, 1.7842356101570156e-13, 1.3554867839502434e-13, 1.0268787664152001e-13, 7.757537101146996e-14, 5.843988469743129e-14, 4.3901124133239605e-14, 3.288688449164312e-14, 2.4566915182017297e-14, 1.8300346861964992e-14, 1.3594048585259218e-14, 1.0069759902880129e-14, 7.43824047778419e-15, 5.4790102859820646e-15, 4.0245267466064534e-15, 2.9478699617180092e-15, 2.1531913523300166e-15, 1.5683310240999732e-15, 1.1391309236955588e-15, 8.250691547206043e-16, 5.959198642441807e-16, 4.292063857980308e-16, 3.0826575985745934e-16, 2.2078278344188205e-16, 1.576833801934901e-16, 1.123019867599975e-16, 7.975717435813503e-17, 5.648496716889504e-17, 3.98911726784414e-17, 2.8093220482536013e-17, 1.9729089971390218e-17, 1.3816351721812921e-17, 9.648515727955367e-18, 6.719058761197428e-18, 4.6659187373492384e-18, 3.2310725058305126e-18, 2.231192483765228e-18, 1.5364137110902592e-18, 1.0550185885284315e-18, 7.224251394887752e-19, 4.932946334589029e-19, 3.358928293497196e-19, 2.2807405068660727e-19, 1.5443005303892123e-19, 1.0427220723754787e-19, 7.020792125524433e-20, 4.713944484395122e-20, 3.1561934496796794e-20, 2.1072864092399257e-20, 1.403021478995125e-20, 9.31506467810672e-21, 6.1672028188068945e-21, 4.07165890841706e-21, 2.680620585939377e-21, 1.7598680599182265e-21, 1.1521411059501855e-21, 7.521631201488001e-22, 4.89665155415259e-22, 3.1788290090990667e-22, 2.0578605247345564e-22, 1.328450900126981e-22, 8.551767448669395e-23, 5.489680453616139e-23, 3.514140068278659e-23, 2.2432202621804621e-23, 1.4279259934493065e-23, 9.064015157587902e-24, 5.737428222234243e-24, 3.6215723724094814e-24, 2.2796305491779933e-24, 1.4309690998535556e-24, 8.95827246537912e-25, 5.594048170026134e-25, 3.486177115277984e-25, 2.1710198298458573e-25, 1.3557501050303312e-25, 8.566916142041707e-26, 5.60157907175277e-26, 3.979324071014063e-26, 3.3240458941090625e-26, 3.483088308149605e-26, 4.493545885364394e-26, 6.590462327960816e-26, 1.0258634531964343e-25, 1.633879187809631e-25, 2.621008071428481e-25, 4.208619215451688e-25, 6.74850409641475e-25, 1.0796582690623435e-24, 1.722787816426962e-24, 2.741511682682347e-24, 4.350519873606508e-24, 6.884580283662294e-24, 1.0864162255193766e-23, 1.709607594216738e-23, 2.682734324721637e-23, 4.197974354718031e-23, 6.550624873646758e-23, 1.0193104864786579e-22, 1.5816524570007194e-22, 2.447351964302847e-22, 3.7762662312960713e-22, 5.810447480712396e-22, 8.915328634799002e-22, 1.3640991389347978e-21, 2.0813030199023778e-21, 3.1666895975826845e-21, 4.804591603245265e-21, 7.269227517796503e-21, 1.0967328386094634e-20, 1.6500390953163903e-20, 2.4755313050909318e-20, 3.703594347142273e-20, 5.52534250022264e-20, 8.220075313861592e-20, 1.2194758127727107e-19, 1.8040616999997245e-19, 2.66140141694362e-19, 3.9151660168246785e-19, 5.743422728713813e-19, 8.40179699884117e-19, 1.2256159017916904e-18, 1.782860616883294e-18, 2.5861945820212384e-18, 3.740983605643498e-18, 5.396239465665898e-18, 7.762067662614004e-18, 1.1133826158199908e-17, 1.5925469669896824e-17, 2.2715424857403374e-17, 3.2309503201262775e-17, 4.5826901889882336e-17, 6.481738667753414e-17, 9.142044641597521e-17, 1.2858075150958935e-16, 1.8033888627653402e-16, 2.5222237351439826e-16, 3.517698671262011e-16, 4.892315569929863e-16, 6.785019373189658e-16, 9.383579177817534e-16, 1.2940967758852684e-15, 1.779695855161731e-15, 2.4406506749468586e-15, 3.3376920242906496e-15, 4.551637838469914e-15, 6.189704823709821e-15, 8.393691049073438e-15, 1.1350547812742793e-14, 1.530599145270962e-14, 2.0581968631624864e-14, 2.7598988081999286e-14, 3.6904574922203013e-14, 4.9209398577723035e-14, 6.543298133788357e-14, 8.676132212031435e-14, 1.1471928081786894e-13, 1.5126117562050597e-13, 1.9888376308718412e-13, 2.607666137259925e-13, 3.4094588056062606e-13, 4.445286013741222e-13, 5.779559940064693e-13, 7.493257149171406e-13, 9.687847698932262e-13, 1.2490067061302935e-12, 1.605768887880548e-12, 2.058648070245416e-12, 2.631855138652492e-12, 3.3552327689501226e-12, 4.2654428694924615e-12, 5.40737396535973e-12, 6.83580213562754e-12, 8.61734266102952e-12, 1.0832733106631459e-11, 1.3579492056550757e-11, 1.6975001016392027e-11, 2.1160059959808984e-11, 2.6302969447439924e-11, 3.260419399056326e-11, 4.0301662141181166e-11, 4.9676758410573365e-11, 6.106106026990553e-11, 7.484386986758643e-11, 9.148058439003022e-11, 1.1150194086672965e-10, 1.355241603471417e-10, 1.6426000243596748e-10, 1.9853072386779717e-10, 2.392789138731925e-10, 2.875821543324894e-10, 3.446674240020705e-10, 4.119261333957461e-10, 4.909296402925243e-10, 5.834450555386299e-10, 6.914511051912103e-10, 8.17153768663461e-10, 9.630013641187733e-10, 1.1316987028699306e-09, 1.326219885125737e-09, 1.549819261458376e-09, 1.8060400394134591e-09, 2.0987199745095836e-09, 2.4319935513997256e-09, 2.810290036240631e-09, 3.2383267674707073e-09, 3.7210970513823154e-09, 4.263852043201102e-09, 4.872076025836562e-09, 5.551454548827876e-09, 6.3078349607564e-09, 7.147178960627132e-09, 8.075506908040299e-09, 9.098833768421728e-09, 1.0223096727530795e-08, 1.1454074687578912e-08, 1.2797300053438113e-08, 1.4257963428674394e-08, 1.584081206374014e-08, 1.7550043128061855e-08, 1.938919310865281e-08, 2.1361024864313895e-08, 2.34674140799346e-08, 2.570923706297424e-08, 2.8086261996748097e-08, 3.059704590554693e-08, 3.323883968794289e-08, 3.600750363044406e-08, 3.8897435818196906e-08, 4.190151580795184e-08, 4.501106581741938e-08, 4.8215831512339626e-08, 5.1503984237529853e-08, 5.4862146242140606e-08, 5.827544009543098e-08, 6.172756308261383e-08, 6.520088691760665e-08, 6.867658261958502e-08, 7.213476988339098e-08, 7.555468974188228e-08, 7.891489878408738e-08, 8.219348267026285e-08, 8.53682861876844e-08, 8.841715663331982e-08, 9.13181969049957e-08, 9.405002434398289e-08, 9.659203111037988e-08, 9.892464169785654e-08, 1.0102956311364604e-07, 1.0289002326817258e-07, 1.0449099323869802e-07, 1.0581938929241677e-07, 1.068642508731742e-07, 1.0761689116628697e-07, 1.0807101734892967e-07], "yaxis": "y", "type": "scatter", "uid": "ae8de3b5-89b8-4185-a197-2bf032e0faab"}, {"legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)", "symbol": "line-ns-open"}, "mode": "markers", "name": "net_influence", "showlegend": false, "x": [2596, 411, 12944, 159, 1932, 1474, 19314, 1420, 349, 865, 1129, 84445, 83, 1772, 382, 3111, 17300, 578, 62, 155, 1204, 10292, 2812, 54293, 1222, 6458, 6983, 1096, 1954, 1299, 4335, 267, 655, 688, 7808, 2209, 2382, 13773, 153, 496, 41435, 19986, 711, 1951, 3003, 4593, 3646, 12522, 2512, 2163, 1102, 105, 158, 10712, 7742, 1364, 47, 67, 6829, 28, 714, 1168, 1997, 90456, 2618, 322, 1451, 550, 607, 6079, 321, 1593, 1114, 4644, 344, 3382, -3, 27006, 2230, 849138, -59, 238, 1713, 1122, 9281, 13314, 15472, 2688, 14411, 10612, 1502, 1346, 27, 252326, 15638, 12100, 604, 2609, 283, 1630, 8426, 2548, 719, 8079, 354, 817, 125, 18964, 116, 231, 226, 549, 4978, 582, 521], "xaxis": "x", "y": ["net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence"], "yaxis": "y2", "type": "scatter", "uid": "6b33bf37-2d12-45c1-a021-93770196f2b2"}], {"barmode": "overlay", "hovermode": "closest", "legend": {"traceorder": "reversed"}, "xaxis": {"anchor": "y2", "domain": [0.0, 1.0], "zeroline": false}, "yaxis": {"anchor": "free", "domain": [0.35, 1], "position": 0.0}, "yaxis2": {"anchor": "x", "domain": [0, 0.25], "dtick": 1, "showticklabels": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("448f31a6-f053-4371-9cd6-c81efbfa946b"));});</script>


## Tweet Sentiment Analysis

Now that we've got our data organized and an idea of the type of users are contributing to the data set we can dive into the tweets themselves.

### Word Frequency

The first thing we'd like to look at within the tweets is word frequency within the top ranked tweets and their replies.  This could identify any patterns and could point out key words that will effect the current social sentiment that we observe.  We'll use TextBlob and our functions "get_blob" and "get_word_count" to do this then display the word count data using plotly pie charts.


```python
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


<div id="27eb2ef4-c09d-46ea-b3aa-03ebf4f215b7" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("27eb2ef4-c09d-46ea-b3aa-03ebf4f215b7", [{"domain": {"column": 0}, "hole": 0.4, "labels": ["tesla", "tslaq", "car", "amp", "elon", "musk", "model", "nflx", "get", "new"], "name": "Tweet", "values": [63, 57, 24, 22, 22, 19, 19, 15, 13, 12], "type": "pie", "uid": "3b145c85-2582-4fa1-98a0-34b22e4f0c93"}, {"domain": {"column": 1}, "hole": 0.4, "labels": ["tslaq", "tesla", "model", "elon", "musk", "short", "ross", "capital", "car", "bull"], "name": "Replies", "values": [9, 8, 7, 6, 6, 6, 5, 5, 5, 4], "type": "pie", "uid": "5ca80606-a5de-4c11-944c-207e726260d8"}], {"annotations": [{"font": {"size": 20}, "showarrow": false, "text": "Tweet", "x": 0.2, "y": 0.5}, {"font": {"size": 20}, "showarrow": false, "text": "Replies", "x": 0.8, "y": 0.5}], "grid": {"columns": 2, "rows": 1}, "title": "Word Frequency"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("27eb2ef4-c09d-46ea-b3aa-03ebf4f215b7"));});</script>


### Bigrams and Trigrams

Looking over word frequency can give us some great insight, but it may lack context.  To add some contextual analysis let's create the same visualization with the most frequently used bigrams and trigrams (these are groups of 2 and 3 words used together).  We'll do this by using the "n" keyword argument of the "get_word_count" function.


```python
tweet_bigram_count = TwtrConvo.twtrconvo.get_word_count(tweet_blob, n=2)
tweet_trigram_count = TwtrConvo.twtrconvo.get_word_count(tweet_blob, n=3)

fig = TwtrConvo.plots.create_pie_chart(
    tweet_bigram_count, tweet_trigram_count, name_1='bigrams',
    name_2='trigrams')
iplot(fig)
```


<div id="27f47884-d8aa-421b-982a-b6620cb30fce" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("27f47884-d8aa-421b-982a-b6620cb30fce", [{"domain": {"column": 0}, "hole": 0.4, "labels": ["elon musk", "self driving", "aapl amzn", "cmcsa fb", "vz wmt", "tmus vz", "nvda tmus", "nflx nvda", "msft nflx", "intc msft"], "name": "bigrams", "values": [11, 7, 5, 4, 4, 4, 4, 4, 4, 4], "type": "pie", "uid": "1d6d8cd2-0002-4952-ae29-7594b046c1a2"}, {"domain": {"column": 1}, "hole": 0.4, "labels": ["ba cmcsa fb", "nflx nvda tmus", "wallstreet stockmarket stocks", "stockmarket stocks valueinvesting", "aapl amzn ba", "vz wmt xom", "tmus vz wmt", "nvda tmus vz", "amzn ba cmcsa", "msft nflx nvda"], "name": "trigrams", "values": [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], "type": "pie", "uid": "9ae77cd0-9eed-40c6-a0a7-f2ba5a972bfc"}], {"annotations": [{"font": {"size": 20}, "showarrow": false, "text": "bigrams", "x": 0.2, "y": 0.5}, {"font": {"size": 20}, "showarrow": false, "text": "trigrams", "x": 0.8, "y": 0.5}], "grid": {"columns": 2, "rows": 1}, "title": "Word Frequency"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("27f47884-d8aa-421b-982a-b6620cb30fce"));});</script>


### Sentiment Gauge

Now that we've got the general idea of frequently used words and terms let's take a look at the overall sentiment of all the tweets using TextBlob.  We'll start by grouping all the text together as a single text blob then displaying the calculated polarity and subjectivity of that large string.  Then we'll display the measured polarity and subjectivity as a sentiment guage using the "create_sentiment_guage" function of the TwtrConvo.plots module.

    - polarity: The polarity score is within the range [-1.0, 1.0] and represents positive or negative sentiment.
    - subjectivity: The subjectivity is within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.


```python
fig = TwtrConvo.plots.create_sentiment_gauge(tweet_blob)
iplot(fig)
```


<div id="56f94358-9877-488a-ac1e-62ba363964df" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("56f94358-9877-488a-ac1e-62ba363964df", [{"direction": "clockwise", "domain": {"x": [0.0, 0.48]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "-1", "0", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "023392d7-7b02-4e11-bea7-41697528c7ec"}, {"direction": "clockwise", "domain": {"x": [0.0, 0.48]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Polarity", "Negative", "Neutral", "Positive"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "b8e1f2a4-a37a-46a2-ad46-d99d145c0e17"}, {"direction": "clockwise", "domain": {"x": [0.52, 1.0]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "0", "0.5", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(178, 255, 102)", "rgb(192, 192, 192)", "rgb(255, 102, 102)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "1acd3e25-1c9e-4122-a22b-998877ad7442"}, {"direction": "clockwise", "domain": {"x": [0.52, 1.0]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Subjectivity", "Very Objective", "Neutral", "Very Subjective"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(178, 255, 102)", "rgb(192, 192, 192)", "rgb(255, 102, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "52da054c-312f-4984-90b5-b5b2c3c0575d"}], {"annotations": [{"showarrow": false, "text": "0.104", "x": 0.24, "xref": "paper", "y": 0.45, "yref": "paper"}, {"showarrow": false, "text": "0.46", "x": 0.76, "xref": "paper", "y": 0.45, "yref": "paper"}], "shapes": [{"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.23505271582577839 0.500724140386594 L 0.2617242115978182 0.6484185252266482 L 0.2449472841742216 0.49927585961340604 Z", "type": "path", "xref": "paper", "yref": "paper"}, {"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.755030726040014 0.4994465415005575 L 0.7433962450167252 0.6490782187995798 L 0.764969273959986 0.5005534584994424 Z", "type": "path", "xref": "paper", "yref": "paper"}], "xaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}, "yaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("56f94358-9877-488a-ac1e-62ba363964df"));});</script>


### Tweet Metadata

Let's take a look at some of the metadata related to the tweets so that we can get a revised sentiment guage that weights the higher ranked tweets more heavily.  First, we'll dive into some of the metadata then we'll create weights and regenerate the guage.

#### Retweet and Favorite Distributions (Using Boxplots)


```python
fig = TwtrConvo.plots.create_boxplot(tweet_df)
iplot(fig)
```


<div id="e3ccbeb3-dd18-4d95-b61a-ac54277c3da2" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("e3ccbeb3-dd18-4d95-b61a-ac54277c3da2", [{"boxpoints": "all", "jitter": 0.5, "line": {"width": 1}, "name": "retweets", "whiskerwidth": 0.2, "x": [65, 36, 11, 10, 14, 4, 9, 8, 13, 5, 7, 18, 5, 9, 6, 7, 6, 5, 5, 7, 5, 2, 2, 4, 10, 3, 24, 1, 18, 6, 10, 1, 6, 4, 1, 4, 14, 1, 6, 1, 14, 3, 3, 10, 3, 4, 4, 2, 2, 5, 1, 3, 2, 1, 5, 9, 9, 2, 2, 1, 5, 2, 1, 6, 1, 2, 5, 6, 3, 6, 3, 6, 1, 5, 1, 3, 1, 1, 1, 2, 6, 8, 4, 4, 2, 4, 2, 2, 1, 24, 15, 5, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 3, 2, 2, 1, 2, 2, 1, 1, 2, 1, 6, 1, 4, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 0, 5, 3, 2, 0, 1, 3, 1, 1, 2, 7, 0, 1, 0, 2, 2, 1, 1, 1, 0, 0, 1, 1, 2, 0, 0, 0, 1, 0, 1, 5, 1, 0, 3, 1, 1, 3, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 3, 3, 3, 2, 0, 1, 1, 2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 2, 0, 2, 0], "type": "box", "uid": "d53c0960-ce60-4584-84fb-05d72701ab39"}, {"boxpoints": "all", "jitter": 0.5, "line": {"width": 1}, "name": "favorites", "whiskerwidth": 0.2, "x": [554, 255, 104, 41, 86, 72, 33, 51, 51, 46, 53, 99, 57, 36, 21, 28, 55, 21, 31, 39, 23, 12, 14, 21, 55, 7, 67, 26, 119, 6, 76, 27, 35, 51, 32, 66, 37, 16, 41, 12, 84, 28, 7, 77, 5, 19, 51, 5, 9, 49, 11, 43, 28, 15, 38, 47, 66, 22, 31, 13, 44, 19, 8, 125, 10, 6, 9, 8, 17, 38, 12, 23, 7, 7, 35, 2, 22, 37, 26, 12, 28, 22, 41, 44, 7, 34, 26, 2, 8, 103, 72, 13, 8, 10, 18, 2, 13, 4, 10, 14, 10, 1, 7, 6, 12, 1, 13, 10, 3, 3, 7, 13, 17, 26, 34, 1, 23, 4, 4, 16, 17, 3, 5, 21, 8, 1, 8, 12, 14, 3, 23, 24, 8, 23, 8, 11, 6, 10, 6, 5, 3, 7, 22, 11, 11, 9, 1, 3, 9, 1, 11, 7, 1, 3, 5, 7, 6, 8, 8, 7, 6, 12, 9, 5, 4, 5, 2, 3, 5, 5, 1, 4, 16, 2, 4, 1, 21, 3, 3, 3, 3, 31, 3, 3, 4, 3, 11, 3, 7, 6, 9, 2, 3, 2, 3, 3, 4, 18, 3, 8], "type": "box", "uid": "2db90007-0c24-4ca5-89e4-43bd0600544c"}], {"title": "Retweets and Favorites"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("e3ccbeb3-dd18-4d95-b61a-ac54277c3da2"));});</script>


#### Polarity and Subjectivity Distributions (Using Violin Plots)


```python
 fig = TwtrConvo.plots.create_violin_plot(
        tweet_df, ['polarity', 'subjectivity'], 'Sentiment Violin Plot')
iplot(fig)
```


<div id="bba20b3e-d5b3-4a3f-b6f5-739dbec1d9f7" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("bba20b3e-d5b3-4a3f-b6f5-739dbec1d9f7", [{"box": {"visible": true}, "jitter": 0, "meanline": {"visible": true}, "name": "polarity", "opacity": 0.6, "points": "all", "y": [0.1, 0.4, 0.18825757575757576, 0.0, -0.4458333333333333, 0.125, 0.0, 0.19126984126984128, -0.05, 0.0, 0.125, 0.75, 0.0, -0.6, 1.0, -0.2, 0.0, 0.12727272727272726, -0.25, 0.1285714285714286, 0.2611111111111111, 0.2, 0.0, -0.04, 0.1643939393939394, 0.0, 0.14, 0.55, 0.2, 0.1, 0.25, 0.0, 0.0, 0.0, 0.11111111111111112, 0.0, 0.0, 0.3715909090909091, -0.4, 0.0, 0.0, 0.0, 0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.13636363636363635, 0.09523809523809523, 0.0, 0.2333333333333333, 0.05, 0.21818181818181814, -0.05185185185185186, 0.2333333333333333, 0.18611111111111112, 0.0, -0.3125, -0.5, -0.5, -0.3, 0.3, 0.0, 0.2, 0.2857142857142857, 0.30000000000000004, -0.0008417508417508471, 0.0, -0.1195436507936508, -0.16111111111111112, 0.0, -0.07142857142857144, 0.2266666666666667, 0.21666666666666667, -0.15000000000000002, 0.2625, 0.0, 0.16948051948051948, 0.5, 0.0, 0.054999999999999986, 0.0, 0.037500000000000006, 0.75, 0.012121212121212116, 0.014285714285714275, 0.0, 0.175, 0.3055555555555556, 0.5, 0.0, -0.17833333333333334, -0.026041666666666668, 0.0, 0.0, 0.0, 0.0, -0.03333333333333333, 0.2, 0.0, 0.2, 0.05357142857142857, 0.2, 0.0, 0.0, 0.0, -0.19444444444444445, 0.43333333333333335, 0.0, 0.3, 0.0, -0.175, -0.15, 0.25, 0.16666666666666666, 0.02083333333333334, 0.3, 0.0, 0.2916666666666667, -0.06224489795918368, 0.0625, 0.275, 0.20000000000000004, -0.1875, 0.0, 0.6, -0.038888888888888896, -0.25, 0.0, -0.3, -0.125, 0.0, 0.0, 0.0, 0.35, 0.375, 0.0, 0.4333333333333333, 0.08333333333333333, 0.0, 0.30000000000000004, 0.5375, 0.07333333333333332, 0.30000000000000004, 0.5148148148148147, 0.0, 0.175, 0.0695, 0.0, 0.0, 0.0, 0.1481818181818182, 0.0, 0.15, -0.1962962962962963, 0.4, 0.037037037037037014, 0.4590909090909091, 0.8, 0.3, 0.0, 0.2125, 0.7, 0.1, 0.5, 0.2, -0.09722222222222222, 0.4, 0.0, 0.0, 0.2, 0.0, 0.1125, -0.3, 0.0, 0.4454545454545455, 0.0, 0.5, 0.21428571428571427, 0.2, -0.19444444444444445, -0.5, -0.11, 0.0, 0.0, -0.06666666666666668, 0.08000000000000003, 0.0, 0.4000000000000001, 0.3333333333333333, 0.0, 0.0, 0.10555555555555557, 0.8, 0.55, 0.6, 0.011111111111111113, 0.45, 0.0], "type": "violin", "uid": "0d1b751d-267c-4e45-9803-bf7df76c5c7d"}, {"box": {"visible": true}, "jitter": 0, "meanline": {"visible": true}, "name": "subjectivity", "opacity": 0.6, "points": "all", "y": [0.4, 0.45, 0.28863636363636364, 0.0, 0.7208333333333333, 0.21666666666666667, 0.0, 0.5700396825396825, 0.2, 0.0, 0.65, 0.75, 0.25, 0.9, 1.0, 0.3, 0.125, 0.4909090909090909, 0.5, 0.4047619047619047, 0.6611111111111111, 0.30000000000000004, 1.0, 0.053333333333333344, 0.3590909090909091, 0.0, 0.58, 0.7, 0.45, 0.1, 0.6499999999999999, 0.0, 0.05, 0.0, 0.3555555555555556, 0.0, 0.0, 0.5428030303030302, 0.6, 0.0, 0.0, 0.0, 0.0, 0.9, 0.275, 0.0, 0.0, 0.0, 0.4545454545454545, 0.32142857142857145, 0.0, 0.3333333333333333, 0.7999999999999999, 0.4772727272727273, 0.12962962962962965, 0.4833333333333333, 0.5222222222222223, 0.0, 0.5750000000000001, 0.3, 1.0, 0.5, 0.1, 0.0, 0.2, 0.5357142857142857, 0.6, 0.5404040404040403, 0.0, 0.5677579365079365, 0.2277777777777778, 0.0, 0.6785714285714285, 0.54, 0.3833333333333333, 0.8, 0.4, 0.0, 0.5006493506493507, 0.5, 0.0, 0.4507142857142857, 0.0, 0.16666666666666669, 0.95, 0.18484848484848485, 0.4714285714285715, 0.0, 0.7000000000000001, 0.3333333333333333, 0.5, 0.0, 0.5149999999999999, 0.39166666666666666, 0.0, 0.0, 0.0, 0.0, 0.4000000000000001, 0.2, 0.0, 0.3333333333333333, 0.6321428571428571, 0.2, 0.0, 0.0, 0.0, 0.4166666666666667, 0.3666666666666667, 0.0, 0.7333333333333334, 1.0, 0.5, 0.5666666666666668, 0.5, 0.3333333333333333, 0.605952380952381, 0.2, 1.0, 0.4583333333333333, 0.5704081632653061, 0.5, 0.35, 0.6, 0.725, 0.0, 0.65, 0.20347222222222225, 0.25, 0.0, 0.2, 0.35, 0.0, 0.0, 0.0, 1.0, 0.75, 0.0, 0.7333333333333333, 0.6833333333333332, 0.0, 0.7666666666666666, 0.8, 0.3933333333333333, 0.5666666666666667, 0.3962962962962964, 0.0, 0.7125, 0.38299999999999995, 0.0, 0.0, 0.0, 0.4972727272727272, 0.0, 0.1125, 0.5629629629629629, 0.6875, 0.3629629629629629, 0.6886363636363636, 0.75, 0.2, 0.0, 0.6875, 0.6000000000000001, 0.1, 0.5, 0.2, 0.6805555555555555, 0.5, 0.0, 0.0, 0.3, 0.25, 0.5, 0.5, 0.0, 0.5181818181818182, 0.0, 0.5, 0.6428571428571429, 0.30000000000000004, 0.4166666666666667, 0.5, 0.2933333333333333, 0.25, 0.0, 0.4444444444444445, 0.4764285714285714, 0.0, 0.6333333333333334, 0.3666666666666667, 0.0, 0.0, 0.3333333333333333, 0.75, 1.0, 1.0, 0.05555555555555556, 0.6944444444444444, 0.0], "type": "violin", "uid": "3077b1dc-ecb2-4f2e-926f-5905ac3559c4"}], {"title": "Sentiment Violin Plot", "yaxis": {"zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("bba20b3e-d5b3-4a3f-b6f5-739dbec1d9f7"));});</script>

