
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

    {'created_at': 'Thu May 09 06:39:40 +0000 2019', 'id': 1126376168222072832, 'id_str': '1126376168222072832', 'full_text': "You can't make this up.\n\n$TSLA\nH/T: @lazygetter https://t.co/vaeYl13gV9", 'truncated': False, 'display_text_range': [0, 47], 'entities': {'hashtags': [], 'symbols': [{'text': 'TSLA', 'indices': [25, 30]}], 'user_mentions': [{'screen_name': 'lazygetter', 'name': 'Bubble Boy', 'id': 920833801, 'id_str': '920833801', 'indices': [36, 47]}], 'urls': [], 'media': [{'id': 1126376154062032897, 'id_str': '1126376154062032897', 'indices': [48, 71], 'media_url': 'http://pbs.twimg.com/media/D6GxJPJWkAEXb1V.png', 'media_url_https': 'https://pbs.twimg.com/media/D6GxJPJWkAEXb1V.png', 'url': 'https://t.co/vaeYl13gV9', 'display_url': 'pic.twitter.com/vaeYl13gV9', 'expanded_url': 'https://twitter.com/ravenvanderrave/status/1126376168222072832/photo/1', 'type': 'photo', 'sizes': {'medium': {'w': 592, 'h': 880, 'resize': 'fit'}, 'thumb': {'w': 150, 'h': 150, 'resize': 'crop'}, 'small': {'w': 457, 'h': 680, 'resize': 'fit'}, 'large': {'w': 592, 'h': 880, 'resize': 'fit'}}}]}, 'extended_entities': {'media': [{'id': 1126376154062032897, 'id_str': '1126376154062032897', 'indices': [48, 71], 'media_url': 'http://pbs.twimg.com/media/D6GxJPJWkAEXb1V.png', 'media_url_https': 'https://pbs.twimg.com/media/D6GxJPJWkAEXb1V.png', 'url': 'https://t.co/vaeYl13gV9', 'display_url': 'pic.twitter.com/vaeYl13gV9', 'expanded_url': 'https://twitter.com/ravenvanderrave/status/1126376168222072832/photo/1', 'type': 'photo', 'sizes': {'medium': {'w': 592, 'h': 880, 'resize': 'fit'}, 'thumb': {'w': 150, 'h': 150, 'resize': 'crop'}, 'small': {'w': 457, 'h': 680, 'resize': 'fit'}, 'large': {'w': 592, 'h': 880, 'resize': 'fit'}}}]}, 'metadata': {'iso_language_code': 'en', 'result_type': 'recent'}, 'source': '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', 'in_reply_to_status_id': None, 'in_reply_to_status_id_str': None, 'in_reply_to_user_id': None, 'in_reply_to_user_id_str': None, 'in_reply_to_screen_name': None, 'user': {'id': 968913585907871745, 'id_str': '968913585907871745', 'name': 'Gavran', 'screen_name': 'ravenvanderrave', 'location': '', 'description': 'Managing Member at Kerviel Leeson Jett Capital, Canada Institute of Cultural Teslaqology, Run the $TSLAQ Doomsday Clock. Long #FUDcoin, short $GRBR, #CYAZ $TSLA', 'url': None, 'entities': {'description': {'urls': []}}, 'protected': False, 'followers_count': 1736, 'friends_count': 1017, 'listed_count': 34, 'created_at': 'Wed Feb 28 18:19:35 +0000 2018', 'favourites_count': 25671, 'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'verified': False, 'statuses_count': 24595, 'lang': 'en', 'contributors_enabled': False, 'is_translator': False, 'is_translation_enabled': False, 'profile_background_color': 'F5F8FA', 'profile_background_image_url': None, 'profile_background_image_url_https': None, 'profile_background_tile': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1124212559786250240/WO5LNftf_normal.png', 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1124212559786250240/WO5LNftf_normal.png', 'profile_banner_url': 'https://pbs.twimg.com/profile_banners/968913585907871745/1551602187', 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 'has_extended_profile': False, 'default_profile': True, 'default_profile_image': False, 'following': False, 'follow_request_sent': False, 'notifications': False, 'translator_type': 'none'}, 'geo': None, 'coordinates': None, 'place': None, 'contributors': None, 'is_quote_status': False, 'retweet_count': 1, 'favorite_count': 4, 'favorited': False, 'retweeted': False, 'possibly_sensitive': False, 'lang': 'en'}


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
      <td>739</td>
      <td>1126143473789407233</td>
      <td>Teslarati</td>
      <td>1308211178</td>
      <td>Tesla $TSLA completes $2.7B funding round as B...</td>
      <td>Tesla TSLA completes 2 7B funding round as BMW...</td>
      <td>266</td>
      <td>31</td>
      <td>90709</td>
      <td>71</td>
      <td>0.150000</td>
      <td>0.450000</td>
      <td>90638</td>
      <td>791.0</td>
      <td>791.0</td>
      <td>794.0</td>
      <td>2376.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>357</td>
      <td>1126230448101703680</td>
      <td>GerberKawasaki</td>
      <td>349249475</td>
      <td>Have an appointment with the Audi Etron on Fri...</td>
      <td>Have an appointment with the Audi Etron on Fri...</td>
      <td>138</td>
      <td>8</td>
      <td>58945</td>
      <td>4665</td>
      <td>0.465341</td>
      <td>0.513636</td>
      <td>54280</td>
      <td>786.5</td>
      <td>776.5</td>
      <td>791.0</td>
      <td>2354.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>312</td>
      <td>1126240263632969729</td>
      <td>GerberKawasaki</td>
      <td>349249475</td>
      <td>You wonder why they attack Tesla relentlessly....</td>
      <td>You wonder why they attack Tesla relentlessly ...</td>
      <td>57</td>
      <td>15</td>
      <td>58945</td>
      <td>4665</td>
      <td>0.000000</td>
      <td>0.100000</td>
      <td>54280</td>
      <td>786.5</td>
      <td>785.0</td>
      <td>775.5</td>
      <td>2347.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>310</td>
      <td>1126241351656398854</td>
      <td>GerberKawasaki</td>
      <td>349249475</td>
      <td>It's as if my soul mate took over the @Tesla t...</td>
      <td>It s as if my soul mate took over the twitter ...</td>
      <td>91</td>
      <td>7</td>
      <td>58945</td>
      <td>4665</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>54280</td>
      <td>786.5</td>
      <td>771.0</td>
      <td>787.0</td>
      <td>2344.5</td>
    </tr>
    <tr>
      <th>4</th>
      <td>600</td>
      <td>1126172969506619393</td>
      <td>LanceRoberts</td>
      <td>49958733</td>
      <td>So, @realDonaldTrump showed tax losses which m...</td>
      <td>So showed tax losses which makes him a poor bu...</td>
      <td>62</td>
      <td>14</td>
      <td>22514</td>
      <td>6679</td>
      <td>-0.160000</td>
      <td>0.640000</td>
      <td>15835</td>
      <td>770.0</td>
      <td>784.0</td>
      <td>779.0</td>
      <td>2333.0</td>
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
      <td>4xRevenue</td>
      <td>8279</td>
      <td>876</td>
      <td>460</td>
      <td>The best PMs are analysts who have yet to mana...</td>
      <td>6215</td>
      <td>457483584</td>
      <td>The best PMs are analysts who have yet to mana...</td>
      <td>416</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AlterViggo</td>
      <td>13725</td>
      <td>2195</td>
      <td>246</td>
      <td>I like, you know, facts. And science. And bett...</td>
      <td>4823</td>
      <td>983380841484042241</td>
      <td>I like you know facts And science And better cars</td>
      <td>1949</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Andreas_Hopf</td>
      <td>4115</td>
      <td>1486</td>
      <td>15</td>
      <td>Designer in Berlin, BA/MA educator and design ...</td>
      <td>707</td>
      <td>937065664128475138</td>
      <td>Designer in Berlin BA MA educator and design r...</td>
      <td>1471</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BagholderQuotes</td>
      <td>18119</td>
      <td>19990</td>
      <td>676</td>
      <td>You don't loose if you don't sell. A satire, p...</td>
      <td>20301</td>
      <td>3424441204</td>
      <td>You don t loose if you don t sell A satire par...</td>
      <td>19314</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BarkMSmeagol</td>
      <td>15327</td>
      <td>1759</td>
      <td>337</td>
      <td>Poking fun and documenting the TSLA fake bears...</td>
      <td>5567</td>
      <td>980554784133427200</td>
      <td>Poking fun and documenting the TSLA fake bears...</td>
      <td>1422</td>
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

    Teslarati (266 Favorites, 31 Retweets, Net Influence 90638, Polarity 0.150, Subjectivity 0.450): 
     Tesla $TSLA completes $2.7B funding round as BMW pledges more EV competition, including a plan for 25 electric and electrified vehicles by 2025
    https://t.co/vtOmor8zuP 
    
    GerberKawasaki (138 Favorites, 8 Retweets, Net Influence 54280, Polarity 0.465, Subjectivity 0.514): 
     Have an appointment with the Audi Etron on Friday morning. Will be giving the full review after. Excited to drive this new EV and compare it to the best. $TSLA #Tesla 
    
    GerberKawasaki (57 Favorites, 15 Retweets, Net Influence 54280, Polarity 0.000, Subjectivity 0.100): 
     You wonder why they attack Tesla relentlessly. #Big #Oil #Money $TSLA https://t.co/CBjy5XrpLQ 
    
    GerberKawasaki (91 Favorites, 7 Retweets, Net Influence 54280, Polarity 0.000, Subjectivity 0.000): 
     It's as if my soul mate took over the @Tesla twitter. $TSLA 
    
    LanceRoberts (62 Favorites, 14 Retweets, Net Influence 15835, Polarity -0.160, Subjectivity 0.640): 
     So, @realDonaldTrump showed tax losses which makes him a poor businessman. Okay, by that logic, $AMZN is a terrible company, they pay $0 taxes. $TSLA is worse and don't even talk about $NFLX. @nytimes needs to flesh out their stories better. #writeoffs https://t.co/QGVL9mq89l 
    
    markbspiegel (76 Favorites, 6 Retweets, Net Influence 12113, Polarity 0.200, Subjectivity 0.567): 
     Wow, a ton of $TSLA borrow opened up today. Thanks, Elon, for printing all those fresh shares! 
    
    markbspiegel (76 Favorites, 4 Retweets, Net Influence 12113, Polarity 0.067, Subjectivity 0.489): 
     It's actually hilarious that the CEO of a $40B public company can claim that his rapidly depreciating, least-reliable-car-on-the-market shitboxes are "appreciating assets"!
    
    #Tesla 
    $TSLA
    $TSLAQ 
    
    hiddenforcespod (43 Favorites, 16 Retweets, Net Influence 4064, Polarity 0.250, Subjectivity 0.283): 
     Want to understand what motivates the community known as $TSLAQ? Listen to @CoveringDelta's episode w/@TeslaCharts and @eddiemac3356, as they discuss "the realization" and why there is more to the story of $TSLA than the public has been led to believe... https://t.co/HAj6uEXSZD https://t.co/pTY0Jd6wnD 
    
    BagholderQuotes (37 Favorites, 5 Retweets, Net Influence 19314, Polarity 0.300, Subjectivity 0.100): 
     “I spend an inordinate amount of my time attempting to explain why $TSLA is worth $2,000 PPS.” https://t.co/qASGs6acDV 
    
    GerberKawasaki (28 Favorites, 4 Retweets, Net Influence 54280, Polarity 0.500, Subjectivity 0.500): 
     Audi e-tron customers face more delivery delays, fines for canceled orders: can they #scale ... $tsla #tesla  https://t.co/Qk5VsOSMdV 
    


### User Data

Next let's take a look at some data on the types of Twitter users that are tweeting about the company with the most influence.  By creating a visualization that displays the relationship between the number of times a term is mentioned in user profile descriptions and the average net influence of those users we can get an idea of the type of profiles participating in the conversation.


```python
user_blob = TwtrConvo.twtrconvo.get_blob(ticker, user_df, header='description')
user_word_count = TwtrConvo.twtrconvo.get_word_count(user_blob)
user_word_count = TwtrConvo.twtrconvo.add_user_data(user_word_count, user_df)

fig = TwtrConvo.plots.create_user_description_scatter(user_word_count)

iplot(fig)
```


<div id="ee726ed2-f934-47fe-ae65-9ca940ef4fa3" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("ee726ed2-f934-47fe-ae65-9ca940ef4fa3", [{"marker": {"size": 33}, "mode": "markers", "name": "investment", "x": [11], "y": [10813.142857142857], "type": "scatter", "uid": "7c247981-8222-402a-85fa-9250dd13e500"}, {"marker": {"size": 27}, "mode": "markers", "name": "tesla", "x": [9], "y": [19498.14285714286], "type": "scatter", "uid": "7251b588-9bb6-4a64-834e-3377acdeecdb"}, {"marker": {"size": 27}, "mode": "markers", "name": "advice", "x": [9], "y": [2848.1], "type": "scatter", "uid": "859ff6cb-5600-4edb-a69e-2796b3c4162e"}, {"marker": {"size": 21}, "mode": "markers", "name": "options", "x": [7], "y": [23342.428571428572], "type": "scatter", "uid": "9e41d360-54e8-434f-98bc-6d448b05e2bd"}, {"marker": {"size": 18}, "mode": "markers", "name": "musk", "x": [6], "y": [25518.6], "type": "scatter", "uid": "3a018937-e9b6-4800-8e14-d5f2b732d3ed"}, {"marker": {"size": 18}, "mode": "markers", "name": "owner", "x": [6], "y": [6360.166666666667], "type": "scatter", "uid": "7ccd2ba3-2904-4a60-b1c2-f5a6415c05e1"}, {"marker": {"size": 18}, "mode": "markers", "name": "buy", "x": [6], "y": [22657.333333333332], "type": "scatter", "uid": "aa6fb2cd-c8a9-4449-b5bf-85c24ef1f766"}, {"marker": {"size": 15}, "mode": "markers", "name": "tslaq", "x": [5], "y": [1126.8], "type": "scatter", "uid": "353cd8f7-816c-405c-8c33-1122aef6b120"}, {"marker": {"size": 15}, "mode": "markers", "name": "short", "x": [5], "y": [3771.4], "type": "scatter", "uid": "3423d45b-7e8b-4553-9656-9f1a762df045"}, {"marker": {"size": 15}, "mode": "markers", "name": "news", "x": [5], "y": [181147.5], "type": "scatter", "uid": "be494f62-ddaf-42bf-8098-acd07ab82840"}, {"marker": {"size": 15}, "mode": "markers", "name": "trading", "x": [5], "y": [15032.333333333334], "type": "scatter", "uid": "fff65bb4-cf3d-42b6-ab28-9c1559e264ac"}, {"marker": {"size": 12}, "mode": "markers", "name": "model", "x": [4], "y": [8999.5], "type": "scatter", "uid": "bf3e2364-5f7c-4fe4-8ce4-e76bdee38f87"}, {"marker": {"size": 12}, "mode": "markers", "name": "ceo", "x": [4], "y": [19034.25], "type": "scatter", "uid": "c912355c-97a2-405b-b2d7-047d6546d67d"}, {"marker": {"size": 12}, "mode": "markers", "name": "elon", "x": [4], "y": [31837.5], "type": "scatter", "uid": "19f8fd37-6478-4829-bdc5-e6418a534e83"}, {"marker": {"size": 12}, "mode": "markers", "name": "market", "x": [4], "y": [25073.25], "type": "scatter", "uid": "21fd02e9-9506-4668-afe3-7a5ed03b04c1"}], {"title": "User Description Scatter", "xaxis": {"title": "Count", "zeroline": false}, "yaxis": {"title": "Average Net Influence", "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("ee726ed2-f934-47fe-ae65-9ca940ef4fa3"));});</script>


Now let's get an idea of the general influence of most of our top tweeters by looking at a distribution of net influence of our users.


```python
fig = TwtrConvo.plots.create_distplot(user_df)
iplot(fig)
```


<div id="64ad6b41-5d34-4e87-b18e-160f4c52f16e" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("64ad6b41-5d34-4e87-b18e-160f4c52f16e", [{"autobinx": false, "histnorm": "probability density", "legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)"}, "name": "net_influence", "opacity": 0.7, "x": [416, 1949, 1471, 19314, 1422, 68869, 6524, 972, 386, 1205, 5148, 20827, 4140, 54280, 1232, 4337, 1432, 675, 15, 697, 2873, 8502, 15835, 38244, 312, 3567, 1688, 494, 20033, 3006, 3648, 2528, 2166, 1074, 1558, 717, 90638, 2631, 2298, 15851, 318, 1597, 1113, 849341, 1724, 2195, 1425, 2689, 436, 1190, 1512, 7891, 58, 4064, 118892, 184, 12113, 1145, 42591, 605, 803, 2607, 287, 1630, 1914, 49232, 32672, 771, 169, 140], "xaxis": "x", "xbins": {"end": 849341.0, "size": 0.0, "start": 15.0}, "yaxis": "y", "type": "histogram", "uid": "d277a756-e089-4c81-871b-5fb5bc30e511"}, {"legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)"}, "mode": "lines", "name": "net_influence", "showlegend": false, "x": [15.0, 1713.652, 3412.304, 5110.956, 6809.608, 8508.26, 10206.912, 11905.564, 13604.216, 15302.868, 17001.52, 18700.172, 20398.824, 22097.476, 23796.128, 25494.78, 27193.432, 28892.084, 30590.736, 32289.388, 33988.04, 35686.692, 37385.344, 39083.996, 40782.648, 42481.3, 44179.952, 45878.604, 47577.256, 49275.908, 50974.56, 52673.212, 54371.864, 56070.516, 57769.168, 59467.82, 61166.472, 62865.124, 64563.776, 66262.428, 67961.08, 69659.732, 71358.384, 73057.036, 74755.688, 76454.34, 78152.992, 79851.644, 81550.296, 83248.948, 84947.6, 86646.252, 88344.904, 90043.556, 91742.208, 93440.86, 95139.512, 96838.164, 98536.816, 100235.468, 101934.12, 103632.772, 105331.424, 107030.076, 108728.728, 110427.38, 112126.032, 113824.684, 115523.336, 117221.988, 118920.64, 120619.292, 122317.944, 124016.596, 125715.248, 127413.9, 129112.552, 130811.204, 132509.856, 134208.508, 135907.16, 137605.812, 139304.464, 141003.116, 142701.768, 144400.42, 146099.072, 147797.724, 149496.376, 151195.028, 152893.68, 154592.332, 156290.984, 157989.636, 159688.288, 161386.94, 163085.592, 164784.244, 166482.896, 168181.548, 169880.2, 171578.852, 173277.504, 174976.156, 176674.808, 178373.46, 180072.112, 181770.764, 183469.416, 185168.068, 186866.72, 188565.372, 190264.024, 191962.676, 193661.328, 195359.98, 197058.632, 198757.284, 200455.936, 202154.588, 203853.24, 205551.892, 207250.544, 208949.196, 210647.848, 212346.5, 214045.152, 215743.804, 217442.456, 219141.108, 220839.76, 222538.412, 224237.064, 225935.716, 227634.368, 229333.02, 231031.672, 232730.324, 234428.976, 236127.628, 237826.28, 239524.932, 241223.584, 242922.236, 244620.888, 246319.54, 248018.192, 249716.844, 251415.496, 253114.148, 254812.8, 256511.452, 258210.104, 259908.756, 261607.408, 263306.06, 265004.712, 266703.364, 268402.016, 270100.668, 271799.32, 273497.972, 275196.624, 276895.276, 278593.928, 280292.58, 281991.232, 283689.884, 285388.536, 287087.188, 288785.84, 290484.492, 292183.144, 293881.796, 295580.448, 297279.1, 298977.752, 300676.404, 302375.056, 304073.708, 305772.36, 307471.012, 309169.664, 310868.316, 312566.968, 314265.62, 315964.272, 317662.924, 319361.576, 321060.228, 322758.88, 324457.532, 326156.184, 327854.836, 329553.488, 331252.14, 332950.792, 334649.444, 336348.096, 338046.748, 339745.4, 341444.052, 343142.704, 344841.356, 346540.008, 348238.66, 349937.312, 351635.964, 353334.616, 355033.268, 356731.92, 358430.572, 360129.224, 361827.876, 363526.528, 365225.18, 366923.832, 368622.484, 370321.136, 372019.788, 373718.44, 375417.092, 377115.744, 378814.396, 380513.048, 382211.7, 383910.352, 385609.004, 387307.656, 389006.308, 390704.96, 392403.612, 394102.264, 395800.916, 397499.568, 399198.22, 400896.872, 402595.524, 404294.176, 405992.828, 407691.48, 409390.132, 411088.784, 412787.436, 414486.088, 416184.74, 417883.392, 419582.044, 421280.696, 422979.348, 424678.0, 426376.652, 428075.304, 429773.956, 431472.608, 433171.26, 434869.912, 436568.564, 438267.216, 439965.868, 441664.52, 443363.172, 445061.824, 446760.476, 448459.128, 450157.78, 451856.432, 453555.084, 455253.736, 456952.388, 458651.04, 460349.692, 462048.344, 463746.996, 465445.648, 467144.3, 468842.952, 470541.604, 472240.256, 473938.908, 475637.56, 477336.212, 479034.864, 480733.516, 482432.168, 484130.82, 485829.472, 487528.124, 489226.776, 490925.428, 492624.08, 494322.732, 496021.384, 497720.036, 499418.688, 501117.34, 502815.992, 504514.644, 506213.296, 507911.948, 509610.6, 511309.252, 513007.904, 514706.556, 516405.208, 518103.86, 519802.512, 521501.164, 523199.816, 524898.468, 526597.12, 528295.772, 529994.424, 531693.076, 533391.728, 535090.38, 536789.032, 538487.684, 540186.336, 541884.988, 543583.64, 545282.292, 546980.944, 548679.596, 550378.248, 552076.9, 553775.552, 555474.204, 557172.856, 558871.508, 560570.16, 562268.812, 563967.464, 565666.116, 567364.768, 569063.42, 570762.072, 572460.724, 574159.376, 575858.028, 577556.68, 579255.332, 580953.984, 582652.636, 584351.288, 586049.94, 587748.592, 589447.244, 591145.896, 592844.548, 594543.2, 596241.852, 597940.504, 599639.156, 601337.808, 603036.46, 604735.112, 606433.764, 608132.416, 609831.068, 611529.72, 613228.372, 614927.024, 616625.676, 618324.328, 620022.98, 621721.632, 623420.284, 625118.936, 626817.588, 628516.24, 630214.892, 631913.544, 633612.196, 635310.848, 637009.5, 638708.152, 640406.804, 642105.456, 643804.108, 645502.76, 647201.412, 648900.064, 650598.716, 652297.368, 653996.02, 655694.672, 657393.324, 659091.976, 660790.628, 662489.28, 664187.932, 665886.584, 667585.236, 669283.888, 670982.54, 672681.192, 674379.844, 676078.496, 677777.148, 679475.8, 681174.452, 682873.104, 684571.756, 686270.408, 687969.06, 689667.712, 691366.364, 693065.016, 694763.668, 696462.32, 698160.972, 699859.624, 701558.276, 703256.928, 704955.58, 706654.232, 708352.884, 710051.536, 711750.188, 713448.84, 715147.492, 716846.144, 718544.796, 720243.448, 721942.1, 723640.752, 725339.404, 727038.056, 728736.708, 730435.36, 732134.012, 733832.664, 735531.316, 737229.968, 738928.62, 740627.272, 742325.924, 744024.576, 745723.228, 747421.88, 749120.532, 750819.184, 752517.836, 754216.488, 755915.14, 757613.792, 759312.444, 761011.096, 762709.748, 764408.4, 766107.052, 767805.704, 769504.356, 771203.008, 772901.66, 774600.312, 776298.964, 777997.616, 779696.268, 781394.92, 783093.572, 784792.224, 786490.876, 788189.528, 789888.18, 791586.832, 793285.484, 794984.136, 796682.788, 798381.44, 800080.092, 801778.744, 803477.396, 805176.048, 806874.7, 808573.352, 810272.004, 811970.656, 813669.308, 815367.96, 817066.612, 818765.264, 820463.916, 822162.568, 823861.22, 825559.872, 827258.524, 828957.176, 830655.828, 832354.48, 834053.132, 835751.784, 837450.436, 839149.088, 840847.74, 842546.392, 844245.044, 845943.696, 847642.348], "xaxis": "x", "y": [8.309479350728496e-06, 8.345349250721944e-06, 8.369691946489942e-06, 8.38244036190495e-06, 8.383577547278261e-06, 8.373136650213937e-06, 8.351200521142705e-06, 8.317900958562355e-06, 8.273417602684177e-06, 8.217976489733362e-06, 8.151848282529666e-06, 8.075346196139247e-06, 7.988823640300003e-06, 7.892671602945056e-06, 7.787315801451948e-06, 7.673213630202281e-06, 7.550850934627923e-06, 7.420738643130876e-06, 7.283409289085943e-06, 7.139413455564678e-06, 6.989316175459975e-06, 6.833693319350112e-06, 6.673128002734281e-06, 6.508207043216257e-06, 6.3395174968332695e-06, 6.167643301050095e-06, 5.993162049995231e-06, 5.816641925340276e-06, 5.6386388038517805e-06, 5.459693560114048e-06, 5.280329580270716e-06, 5.101050499901097e-06, 4.922338176372879e-06, 4.744650903233504e-06, 4.568421871454353e-06, 4.394057879659207e-06, 4.2219382928825945e-06, 4.052414246943699e-06, 3.885808093212885e-06, 3.722413076412971e-06, 3.5624932361546523e-06, 3.4062835211698464e-06, 3.2539901036893716e-06, 3.1057908801195616e-06, 2.9618361431102533e-06, 2.822249409274018e-06, 2.6871283862106456e-06, 2.556546062106126e-06, 2.4305519010022463e-06, 2.309173126860892e-06, 2.1924160797624833e-06, 2.0802676279659117e-06, 1.9726966201010525e-06, 1.8696553624473962e-06, 1.771081107054706e-06, 1.676897537365931e-06, 1.5870162389896395e-06, 1.5013381443209709e-06, 1.4197549408083896e-06, 1.3421504337912701e-06, 1.268401855974237e-06, 1.1983811167431866e-06, 1.131955985651021e-06, 1.0689912054959903e-06, 1.0093495314708582e-06, 9.528926938675607e-07, 8.994822827712181e-07, 8.489805540628939e-07, 8.012511568671082e-07, 7.56159783323989e-07, 7.13574742234711e-07, 6.733674587212529e-07, 6.354129025573775e-07, 5.995899482681081e-07, 5.65781670461581e-07, 5.338755781527041e-07, 5.037637920657805e-07, 4.7534316906705296e-07, 4.4851537798226796e-07, 4.231869311034852e-07, 3.9926917568831965e-07, 3.7667824970862084e-07, 3.553350060192945e-07, 3.351649089966227e-07, 3.160979075439461e-07, 2.9806828818576195e-07, 2.810145117737394e-07, 2.648790371142276e-07, 2.4960813460063607e-07, 2.351516926993542e-07, 2.2146301989821483e-07, 2.0849864448498007e-07, 1.962181142828444e-07, 1.845837982330149e-07, 1.7356069148324558e-07, 1.631162254176835e-07, 1.5322008384913714e-07, 1.4384402639121722e-07, 1.349617198358074e-07, 1.2654857818180168e-07, 1.1858161179459246e-07, 1.1103928602279295e-07, 1.0390138945932007e-07, 9.71489119082751e-08, 9.076393200691627e-08, 8.472951435315296e-08, 7.902961590304257e-08, 7.364900132925333e-08, 6.857316696982283e-08, 6.378827294616343e-08, 5.9281082989461266e-08, 5.503891148467207e-08, 5.10495772204723e-08, 4.730136332101747e-08, 4.3782982830404106e-08, 4.048354942255108e-08, 3.739255271703552e-08, 3.449983769448017e-08, 3.1795587722656085e-08, 2.9270310725828035e-08, 2.6914828054350515e-08, 2.4720265638477058e-08, 2.2678047039174365e-08, 2.0779888038871082e-08, 1.901779244600411e-08, 1.7384048818481565e-08, 1.5871227842335465e-08, 1.447218013251094e-08, 1.3180034252601154e-08, 1.1988194779101707e-08, 1.0890340263184634e-08, 9.880420968881474e-09, 8.952656290761698e-09, 8.101531776578125e-09, 7.321795700843842e-09, 6.608455153859231e-09, 5.956771627304025e-09, 5.362256092161629e-09, 4.820663577485416e-09, 4.327987269407988e-09, 3.880452158910406e-09, 3.474508274300969e-09, 3.10682354020673e-09, 2.7742763092695197e-09, 2.4739476157831642e-09, 2.2031132023354076e-09, 1.959235371254819e-09, 1.7399547124379282e-09, 1.543081758071296e-09, 1.3665886129903304e-09, 1.2086006070496746e-09, 1.0673880130315094e-09, 9.41357870393058e-10, 8.290459516514276e-10, 7.291089045116687e-10, 6.403165990438887e-10, 5.615447053796907e-10, 4.917675235905519e-10, 4.300510836860424e-10, 3.7554653007437554e-10, 3.2748380140030367e-10, 2.85165613446527e-10, 2.4796174977845113e-10, 2.1530366204540175e-10, 1.86679379335574e-10, 1.6162872372290217e-10, 1.3973882714283023e-10, 1.2063994298764664e-10, 1.0400154431415356e-10, 8.952869929748389e-11, 7.695871353308435e-11, 6.605802797053015e-11, 5.661936064284792e-11, 4.845907991736493e-11, 4.141479672215501e-11, 3.534316307907617e-11, 3.011786428345911e-11, 2.5627792195258512e-11, 2.1775387331064656e-11, 1.84751377556344e-11, 1.5652223151241674e-11, 1.3241292879837855e-11, 1.1185367334453767e-11, 9.43485239123574e-12, 7.946657311864174e-12, 6.683406998811274e-12, 5.612740064985415e-12, 4.706684737853909e-12, 3.941105170184179e-12, 3.295211270086525e-12, 2.75112568793142e-12, 2.293502103607204e-12, 1.909189441862738e-12, 1.5869371041854396e-12, 1.3171367414242283e-12, 1.0915965013219981e-12, 9.033440688644413e-13, 7.464551748574117e-13, 6.159045797149155e-13, 5.074368456454654e-13, 4.1745449205550686e-13, 3.429213870081133e-13, 2.8127946307743526e-13, 2.3037706011408627e-13, 1.8840739153645078e-13, 1.5385580607592646e-13, 1.2545467473039015e-13, 1.0214487431177631e-13, 8.304296567866993e-14, 6.741327775367065e-14, 5.4644208921137595e-14, 4.4228146511282775e-14, 3.5744483868031145e-14, 2.8845283972509316e-14, 2.3243199686629927e-14, 1.870131425974895e-14, 1.5024612606590325e-14, 1.2052834751802849e-14, 9.654498417397664e-15, 7.721908614904644e-15, 6.166998847672119e-15, 4.917871629269355e-15, 3.915925929609929e-15, 3.1134762722207726e-15, 2.471782881544593e-15, 1.9594248358712445e-15, 1.5509589005977527e-15, 1.2258158460831802e-15, 9.673938125525784e-16, 7.623148625724246e-16, 5.998164267189319e-16, 4.71254045837467e-16, 3.6969577027933155e-16, 2.895919023136834e-16, 2.2650655723179995e-16, 1.7689985305249925e-16, 1.3795148827026657e-16, 1.0741809179542016e-16, 8.351808041766612e-17, 6.483888050348727e-17, 5.0262299382712744e-17, 3.890459950879534e-17, 3.0068461650793165e-17, 2.3204544587940686e-17, 1.788077696493696e-17, 1.3757868027465129e-17, 1.0569811212527198e-17, 8.108389148720336e-18, 6.210879809367107e-18, 4.750319077816297e-18, 3.6278012379347706e-18, 2.766401200942109e-18, 2.1063850073714586e-18, 1.601441915245265e-18, 1.2157251764139972e-18, 9.21531853418685e-19, 6.974867384650777e-19, 5.271232380742618e-19, 3.977763142124681e-19, 2.997203095888653e-19, 2.2549861194788246e-19, 1.6940334318948712e-19, 1.2707217111945637e-19, 9.517640028225549e-20, 7.118007873002466e-20, 5.315426117560745e-20, 3.9634037543602737e-20, 2.9508663000604737e-20, 2.1937265712068344e-20, 1.628428508907459e-20, 1.2070104217695145e-20, 8.933363376412545e-21, 6.602238755991469e-21, 4.872590514177056e-21, 3.5913656596831886e-21, 2.644014329809951e-21, 1.9449666845322674e-21, 1.4304406358553075e-21, 1.053022660044673e-21, 7.775965036379154e-22, 5.782966839091149e-22, 4.362423268373989e-22, 3.378675730150472e-22, 2.737118164537572e-22, 2.3756980848419767e-22, 2.2593084709199346e-22, 2.3766004906090084e-22, 2.7389486136161597e-22, 3.3814805001629215e-22, 4.366258040369365e-22, 5.787876555247196e-22, 7.78195037327743e-22, 1.0537190129524628e-21, 1.4312068055334127e-21, 1.9457433806801486e-21, 2.6446911746645168e-21, 3.5917514687056e-21, 4.872369164522263e-21, 6.600904267719315e-21, 8.930125205028658e-21, 1.2063750106393452e-20, 1.6272983774463406e-20, 2.1918284802504472e-20, 2.947796775462948e-20, 3.958572312816837e-20, 5.3079753017499295e-20, 7.106701109710289e-20, 9.500704998177502e-20, 1.2682127816223551e-19, 1.6903508942882128e-19, 2.249624467371574e-19, 2.989452013656208e-19, 3.9666285930540766e-19, 5.2553286068838815e-19, 6.952269526236333e-19, 9.183362075143802e-19, 1.2112260363271404e-18, 1.5951336266784844e-18, 2.0975741651964275e-18, 2.7541396819787263e-18, 3.610796244648354e-18, 4.726812591693723e-18, 6.178487432287426e-18, 8.06388514857903e-18, 1.050884246741243e-17, 1.3674574200941673e-17, 1.7767287285413448e-17, 2.3050312590583757e-17, 2.9859387588750376e-17, 3.862187511148029e-17, 4.988089029382961e-17, 6.432553688215513e-17, 8.282873433180187e-17, 1.0649445928617376e-16, 1.367166419412592e-16, 1.7525246475301104e-16, 2.2431342612087956e-16, 2.8667827664134233e-16, 3.658328357769181e-16, 4.661427824239758e-16, 5.930668193041456e-16, 7.5341917992057e-16, 9.556923266751547e-16, 1.210452936447308e-15, 1.5308269516267584e-15, 1.933092667052511e-15, 2.4374046154111327e-15, 3.068675507966991e-15, 3.857648802057322e-15, 4.842200736977759e-15, 6.068918060517234e-15, 7.595006335918792e-15, 9.490593873867105e-15, 1.1841508203112837e-14, 1.475261583243501e-14, 1.835183215338774e-14, 2.279492700958623e-14, 2.8271273073067513e-14, 3.5010709119987863e-14, 4.329171902706058e-14, 5.3451160301285217e-14, 6.589581373924971e-14, 8.111606896640661e-14, 9.970210975705275e-14, 1.2236301885589148e-13, 1.4994928523248592e-13, 1.8347926806550554e-13, 2.2417025208015102e-13, 2.734748189907019e-13, 3.331233606000383e-13, 4.0517367146726416e-13, 4.92068683867785e-13, 5.967035459237623e-13, 7.225033961371003e-13, 8.735133549247411e-13, 1.0545024368771809e-12, 1.2710832869743337e-12, 1.5298498604017573e-12, 1.8385353992455516e-12, 2.206193310322675e-12, 2.6434038165790574e-12, 3.162509539403407e-12, 3.777883470033182e-12, 4.506233103716853e-12, 5.366944838698323e-12, 6.382473081102099e-12, 7.578778843494493e-12, 8.985822975653015e-12, 1.0638119516508541e-11, 1.257535500111148e-11, 1.4843079889705777e-11, 1.7493478600499243e-11, 2.0586224915429945e-11, 2.4189429780023436e-11, 2.838068872412524e-11, 3.3248236278601834e-11, 3.889221484167958e-11, 4.5426065444027007e-11, 5.297804775959757e-11, 6.169289649432767e-11, 7.173362094093748e-11, 8.32834539985779e-11, 9.654795630372458e-11, 1.1175728028612852e-10, 1.2916859793346313e-10, 1.490686948035655e-10, 1.71776731347625e-10, 1.9764717088622238e-10, 2.2707287159924573e-10, 2.6048833763893603e-10, 2.98373121943899e-10, 3.4125537051499766e-10, 3.8971549480981165e-10, 4.4438995552307165e-10, 5.059751373534514e-10, 5.752312904250922e-10, 6.529865098541227e-10, 7.401407205516838e-10, 8.3766962976809e-10, 9.466286051479451e-10, 1.0681564312310718e-09, 1.2034788924550674e-09, 1.353912125856355e-09, 1.5208656818998806e-09, 1.7058452272734736e-09, 1.910454819149022e-09, 2.136398676433558e-09, 2.385482370010244e-09, 2.659613351007969e-09, 2.9608007338488384e-09, 3.2911542493180238e-09, 3.6528822822935085e-09, 4.048288909176696e-09, 4.479769851588164e-09, 4.9498072656399954e-09, 5.460963290163443e-09, 6.01587228274439e-09, 6.617231679372409e-09, 7.267791421999744e-09, 7.970341908374131e-09, 8.727700430172868e-09, 9.542696078720336e-09, 1.0418153112388317e-08, 1.1356872796099989e-08, 1.2361613741099039e-08, 1.3435070792187706e-08, 1.4579852529834272e-08, 1.5798457475721924e-08, 1.7093249112246602e-08, 1.8466429848929076e-08, 1.992001409141711e-08, 2.1455800591418077e-08, 2.3075344278200845e-08, 2.477992779389452e-08, 2.6570532975333623e-08, 2.844781254428298e-08, 3.0412062285145894e-08, 3.2463194004338344e-08, 3.460070957803105e-08, 3.682367640456137e-08, 3.9130704584161996e-08, 4.1519926151432504e-08, 4.398897668491673e-08, 4.653497961300946e-08, 4.915453352601217e-08, 5.1843702790358226e-08, 5.459801174275774e-08, 5.7412442719264215e-08, 6.028143814709869e-08, 6.319890689561187e-08, 6.615823504722906e-08, 6.915230120987371e-08, 7.217349644957501e-08, 7.521374887612251e-08, 7.82645528662564e-08, 8.131700285850194e-08, 8.436183160198722e-08, 8.73894526890734e-08, 9.039000714906878e-08, 9.335341382841134e-08, 9.626942323222692e-08, 9.912767445384811e-08, 1.0191775477344537e-07, 1.0462926146510202e-07, 1.0725186531414086e-07, 1.0977537531393025e-07, 1.1218980398434693e-07, 1.1448543273307381e-07, 1.1665287666640523e-07, 1.1868314824857567e-07, 1.2056771920808e-07, 1.2229858009617327e-07, 1.2386829691677594e-07, 1.2527006426831024e-07, 1.2649775446638373e-07, 1.2754596215144196e-07, 1.2841004392714587e-07, 1.290861526228057e-07, 1.2957126582614064e-07, 1.2986320839026184e-07], "yaxis": "y", "type": "scatter", "uid": "bb2cffe5-7892-467c-910c-d5843247f2e6"}, {"legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)", "symbol": "line-ns-open"}, "mode": "markers", "name": "net_influence", "showlegend": false, "x": [416, 1949, 1471, 19314, 1422, 68869, 6524, 972, 386, 1205, 5148, 20827, 4140, 54280, 1232, 4337, 1432, 675, 15, 697, 2873, 8502, 15835, 38244, 312, 3567, 1688, 494, 20033, 3006, 3648, 2528, 2166, 1074, 1558, 717, 90638, 2631, 2298, 15851, 318, 1597, 1113, 849341, 1724, 2195, 1425, 2689, 436, 1190, 1512, 7891, 58, 4064, 118892, 184, 12113, 1145, 42591, 605, 803, 2607, 287, 1630, 1914, 49232, 32672, 771, 169, 140], "xaxis": "x", "y": ["net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence"], "yaxis": "y2", "type": "scatter", "uid": "89f957fc-4fed-44f6-86af-6f2a8e788d49"}], {"barmode": "overlay", "hovermode": "closest", "legend": {"traceorder": "reversed"}, "xaxis": {"anchor": "y2", "domain": [0.0, 1.0], "zeroline": false}, "yaxis": {"anchor": "free", "domain": [0.35, 1], "position": 0.0}, "yaxis2": {"anchor": "x", "domain": [0, 0.25], "dtick": 1, "showticklabels": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("64ad6b41-5d34-4e87-b18e-160f4c52f16e"));});</script>


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


<div id="9534e2da-ab23-4c02-a627-ea858df945a8" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("9534e2da-ab23-4c02-a627-ea858df945a8", [{"domain": {"column": 0}, "hole": 0.4, "labels": ["tesla", "tslaq", "car", "people", "musk", "time", "money", "stocks", "year", "cars"], "name": "Tweet", "values": [35, 35, 10, 9, 8, 7, 7, 6, 6, 6], "type": "pie", "uid": "ba927de8-2b2c-4178-b0ec-4755f2ff54d8"}, {"domain": {"column": 1}, "hole": 0.4, "labels": ["tslaq", "one", "tesla", "get", "incompatible", "car", "elon", "great", "pro", "vw"], "name": "Replies", "values": [7, 4, 4, 3, 3, 3, 2, 2, 2, 2], "type": "pie", "uid": "d306fc93-c02e-46fd-ba97-e5d80e36c36f"}], {"annotations": [{"font": {"size": 20}, "showarrow": false, "text": "Tweet", "x": 0.2, "y": 0.5}, {"font": {"size": 20}, "showarrow": false, "text": "Replies", "x": 0.8, "y": 0.5}], "grid": {"columns": 2, "rows": 1}, "title": "Word Frequency"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("9534e2da-ab23-4c02-a627-ea858df945a8"));});</script>


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


<div id="8c904124-1e2f-4c1f-9809-7eaf57c01b6f" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("8c904124-1e2f-4c1f-9809-7eaf57c01b6f", [{"domain": {"column": 0}, "hole": 0.4, "labels": ["appreciate value", "tesla closes", "tesla model", "every single", "mixed offering", "slv gld", "gld qqq", "billion mixed", "qqq djia", "stocks gold"], "name": "bigrams", "values": [3, 3, 3, 2, 2, 2, 2, 2, 2, 2], "type": "pie", "uid": "1b3b62c5-c439-4c12-9506-9e4286b618d9"}, {"domain": {"column": 1}, "hole": 0.4, "labels": ["intc amd nflx", "tesla closes billion", "billion mixed offering", "offering shares debt", "slv gld qqq", "gld qqq djia", "qqq djia dia", "djia dia spy", "dia spy stockmarket", "spy stockmarket commodities"], "name": "trigrams", "values": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], "type": "pie", "uid": "d71ecc88-ca71-41dc-bd32-319c24ec77cd"}], {"annotations": [{"font": {"size": 20}, "showarrow": false, "text": "bigrams", "x": 0.2, "y": 0.5}, {"font": {"size": 20}, "showarrow": false, "text": "trigrams", "x": 0.8, "y": 0.5}], "grid": {"columns": 2, "rows": 1}, "title": "Word Frequency"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("8c904124-1e2f-4c1f-9809-7eaf57c01b6f"));});</script>


### Sentiment Gauge

Now that we've got the general idea of frequently used words and terms let's take a look at the overall sentiment of all the tweets using TextBlob.  We'll start by grouping all the text together as a single text blob then displaying the calculated polarity and subjectivity of that large string.  Then we'll display the measured polarity and subjectivity as a sentiment guage using the "create_sentiment_guage" function of the TwtrConvo.plots module.

    - polarity: The polarity score is within the range [-1.0, 1.0] and represents positive or negative sentiment.
    - subjectivity: The subjectivity is within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.


```python
fig = TwtrConvo.plots.create_sentiment_gauge(tweet_blob.sentiment.polarity,
                                             tweet_blob.sentiment.subjectivity)
iplot(fig)
```


<div id="c9c3c969-5ea4-4b0c-9b69-1a49012ece94" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("c9c3c969-5ea4-4b0c-9b69-1a49012ece94", [{"direction": "clockwise", "domain": {"x": [0.0, 0.48]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "-1", "0", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "b136a261-142d-47e4-947d-a6697ac6c9ba"}, {"direction": "clockwise", "domain": {"x": [0.0, 0.48]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Polarity", "Negative", "Neutral", "Positive"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "55fa7415-eefb-4391-8d60-058e4eef0b03"}, {"direction": "clockwise", "domain": {"x": [0.52, 1.0]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "0", "0.5", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(178, 255, 102)", "rgb(192, 192, 192)", "rgb(255, 102, 102)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "8aee4af1-b7ab-4786-8d76-a632c42d7d77"}, {"direction": "clockwise", "domain": {"x": [0.52, 1.0]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Subjectivity", "Very Objective", "Neutral", "Very Subjective"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(178, 255, 102)", "rgb(192, 192, 192)", "rgb(255, 102, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "2a0df496-672f-4843-ad92-482cb3a887cd"}], {"annotations": [{"showarrow": false, "text": "0.12", "x": 0.24, "xref": "paper", "y": 0.45, "yref": "paper"}, {"showarrow": false, "text": "0.479", "x": 0.76, "xref": "paper", "y": 0.45, "yref": "paper"}], "shapes": [{"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.23506993102075863 0.5008333185824894 L 0.2649995574746792 0.647902069377241 L 0.24493006897924136 0.4991666814175107 Z", "type": "path", "xref": "paper", "yref": "paper"}, {"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.755008666731067 0.49970573447629146 L 0.7511720342887442 0.6497399980679874 L 0.764991333268933 0.5002942655237085 Z", "type": "path", "xref": "paper", "yref": "paper"}], "xaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}, "yaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("c9c3c969-5ea4-4b0c-9b69-1a49012ece94"));});</script>


### Tweet Metadata

Let's take a look at some of the metadata related to the tweets so that we can get a revised sentiment guage that weights the higher ranked tweets more heavily.  First, we'll dive into some of the metadata then we'll create weights and regenerate the guage.

#### Retweet and Favorite Distributions (Using Boxplots)


```python
fig = TwtrConvo.plots.create_boxplot(tweet_df)
iplot(fig)
```


<div id="d2213016-53f8-4d84-b333-226600622b66" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("d2213016-53f8-4d84-b333-226600622b66", [{"boxpoints": "all", "jitter": 0.5, "line": {"width": 1}, "name": "retweets", "whiskerwidth": 0.2, "x": [31, 8, 15, 7, 14, 6, 4, 16, 5, 4, 11, 7, 6, 3, 7, 5, 3, 2, 8, 31, 6, 7, 2, 4, 51, 4, 4, 6, 18, 10, 6, 7, 1, 1, 4, 6, 2, 4, 1, 3, 2, 1, 31, 26, 3, 2, 3, 2, 9, 2, 3, 1, 1, 7, 1, 3, 1, 2, 8, 2, 2, 3, 1, 1, 3, 3, 4, 2, 383, 1, 2, 1, 2, 6, 1, 1, 1, 9, 3, 37, 1, 1, 3, 2, 2, 2, 1, 1, 1, 1, 3, 0, 1, 3, 8, 1, 1, 1, 1, 2], "type": "box", "uid": "a1ef92da-4697-41a2-afcd-cf15978d3ecc"}, {"boxpoints": "all", "jitter": 0.5, "line": {"width": 1}, "name": "favorites", "whiskerwidth": 0.2, "x": [266, 138, 57, 91, 62, 76, 76, 43, 37, 28, 52, 54, 31, 37, 43, 63, 18, 26, 8, 133, 12, 6, 24, 8, 133, 10, 6, 58, 56, 83, 31, 38, 17, 13, 26, 37, 6, 23, 7, 16, 21, 13, 110, 145, 16, 3, 26, 57, 40, 14, 18, 32, 5, 11, 23, 31, 16, 21, 62, 17, 11, 7, 18, 10, 10, 21, 22, 6, 5374, 17, 6, 2, 30, 37, 4, 11, 7, 69, 19, 147, 54, 6, 1, 2, 5, 31, 10, 3, 1, 1, 20, 33, 16, 9, 62, 8, 4, 13, 13, 11], "type": "box", "uid": "a4a9ab2e-401a-4759-bdc4-5f66968bb438"}], {"title": "Retweets and Favorites"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("d2213016-53f8-4d84-b333-226600622b66"));});</script>


#### Polarity and Subjectivity Distributions (Using Violin Plots)


```python
 fig = TwtrConvo.plots.create_violin_plot(
        tweet_df, ['polarity', 'subjectivity'], 'Sentiment Violin Plot')
iplot(fig)
```


<div id="6c219dfa-1672-41d8-8404-921bf575b278" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("6c219dfa-1672-41d8-8404-921bf575b278", [{"box": {"visible": true}, "jitter": 0, "meanline": {"visible": true}, "name": "polarity", "opacity": 0.6, "points": "all", "y": [0.15, 0.4653409090909091, 0.0, 0.0, -0.16, 0.20000000000000004, 0.06666666666666668, 0.25, 0.3, 0.5, 0.10925925925925926, 0.35, -0.1603846153846154, 0.0, 0.0, 0.13055555555555556, 0.0, 0.2333333333333333, 0.1, 0.18333333333333332, 0.0, 0.23392857142857146, -0.2125, -0.0625, 0.008730158730158732, 0.08499999999999999, 0.21428571428571427, 0.0, 0.20000000000000004, 0.5, 0.08888888888888888, 0.475, 0.0, 0.0, -0.1275, 0.075, 0.3, 0.2375, 0.0, 0.0, 0.0, 0.0375, -0.075, -0.15, 0.0, 0.0, -0.3, 0.0, -0.1, 0.4142857142857143, -0.2, 0.5, 0.43333333333333335, -0.25, 0.5, 0.5083333333333333, 0.325, 0.125, 0.039285714285714285, 0.125, 0.2, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, -0.1, 0.2777777777777778, 0.4875, 0.21428571428571427, 0.25, 0.0, 0.0, 0.0, 0.3333333333333333, 0.5, 0.06666666666666668, 0.14999999999999994, 0.07500000000000001, -0.2, 0.06583333333333333, 0.0, 0.0, 0.04999999999999999, 0.21212121212121213, 0.0, 0.2, -0.1, -0.05, 0.0, 0.0, 0.275, 0.11666666666666665, -0.05, -0.8, 0.2, -0.1607142857142857, 0.7, 0.0, 0.0], "type": "violin", "uid": "cc891946-41cf-4a99-92f9-253df954a41c"}, {"box": {"visible": true}, "jitter": 0, "meanline": {"visible": true}, "name": "subjectivity", "opacity": 0.6, "points": "all", "y": [0.45, 0.5136363636363637, 0.1, 0.0, 0.64, 0.5666666666666667, 0.4888888888888889, 0.2833333333333333, 0.1, 0.5, 0.3444444444444445, 0.35, 0.32884615384615384, 0.0, 0.0, 0.4777777777777778, 0.3, 0.16666666666666666, 0.4, 0.4666666666666666, 0.35, 0.5714285714285714, 0.525, 0.2375, 0.4892857142857143, 0.23833333333333334, 0.42857142857142855, 0.3333333333333333, 0.5333333333333333, 0.5, 0.6577777777777778, 0.75, 0.3, 0.0, 0.29500000000000004, 0.475, 0.4444444444444445, 1.0, 0.0, 0.0, 0.1, 0.6166666666666667, 0.75, 0.4, 0.75, 0.0, 0.6, 0.75, 0.1, 0.5321428571428571, 0.35, 0.55, 0.8333333333333334, 0.4, 1.0, 0.5458333333333333, 0.3, 0.5777777777777778, 0.35595238095238096, 0.2847222222222222, 0.5, 0.0, 0.6428571428571429, 0.0, 0.0, 0.0, 0.65, 0.7000000000000001, 0.8083333333333333, 0.6428571428571429, 0.65, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5166666666666667, 0.7250000000000001, 0.14166666666666666, 0.6, 0.7583333333333334, 0.4000000000000001, 0.0, 0.65, 0.3181818181818182, 0.0, 0.4, 0.0, 0.4, 0.4, 0.0, 0.625, 0.6833333333333332, 0.175, 1.0, 0.6, 0.6071428571428571, 0.6000000000000001, 0.0, 0.0], "type": "violin", "uid": "8796576d-e8cc-470c-a6c2-e283ae1e10c4"}], {"title": "Sentiment Violin Plot", "yaxis": {"zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("6c219dfa-1672-41d8-8404-921bf575b278"));});</script>


#### Correlation Between these Distributions (Using 2d Contour Plots)


```python
fig = TwtrConvo.plots.create_contour(tweet_df)
iplot(fig)
```


<div id="34cbf824-5c6e-4d5c-90b1-e313290a8d23" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("34cbf824-5c6e-4d5c-90b1-e313290a8d23", [{"colorscale": "Blues", "reversescale": true, "x": [31, 8, 15, 7, 14, 6, 4, 16, 5, 4, 11, 7, 6, 3, 7, 5, 3, 2, 8, 31, 6, 7, 2, 4, 51, 4, 4, 6, 18, 10, 6, 7, 1, 1, 4, 6, 2, 4, 1, 3, 2, 1, 31, 26, 3, 2, 3, 2, 9, 2, 3, 1, 1, 7, 1, 3, 1, 2, 8, 2, 2, 3, 1, 1, 3, 3, 4, 2, 383, 1, 2, 1, 2, 6, 1, 1, 1, 9, 3, 37, 1, 1, 3, 2, 2, 2, 1, 1, 1, 1, 3, 0, 1, 3, 8, 1, 1, 1, 1, 2], "xaxis": "x", "y": [0.15, 0.4653409090909091, 0.0, 0.0, -0.16, 0.20000000000000004, 0.06666666666666668, 0.25, 0.3, 0.5, 0.10925925925925926, 0.35, -0.1603846153846154, 0.0, 0.0, 0.13055555555555556, 0.0, 0.2333333333333333, 0.1, 0.18333333333333332, 0.0, 0.23392857142857146, -0.2125, -0.0625, 0.008730158730158732, 0.08499999999999999, 0.21428571428571427, 0.0, 0.20000000000000004, 0.5, 0.08888888888888888, 0.475, 0.0, 0.0, -0.1275, 0.075, 0.3, 0.2375, 0.0, 0.0, 0.0, 0.0375, -0.075, -0.15, 0.0, 0.0, -0.3, 0.0, -0.1, 0.4142857142857143, -0.2, 0.5, 0.43333333333333335, -0.25, 0.5, 0.5083333333333333, 0.325, 0.125, 0.039285714285714285, 0.125, 0.2, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, -0.1, 0.2777777777777778, 0.4875, 0.21428571428571427, 0.25, 0.0, 0.0, 0.0, 0.3333333333333333, 0.5, 0.06666666666666668, 0.14999999999999994, 0.07500000000000001, -0.2, 0.06583333333333333, 0.0, 0.0, 0.04999999999999999, 0.21212121212121213, 0.0, 0.2, -0.1, -0.05, 0.0, 0.0, 0.275, 0.11666666666666665, -0.05, -0.8, 0.2, -0.1607142857142857, 0.7, 0.0, 0.0], "yaxis": "y", "type": "histogram2dcontour", "uid": "cb6c0a76-7f74-4be8-8cea-6a5b30d8f242"}, {"marker": {"color": "rgba(0,0,0,1)"}, "xaxis": "x2", "y": [0.15, 0.4653409090909091, 0.0, 0.0, -0.16, 0.20000000000000004, 0.06666666666666668, 0.25, 0.3, 0.5, 0.10925925925925926, 0.35, -0.1603846153846154, 0.0, 0.0, 0.13055555555555556, 0.0, 0.2333333333333333, 0.1, 0.18333333333333332, 0.0, 0.23392857142857146, -0.2125, -0.0625, 0.008730158730158732, 0.08499999999999999, 0.21428571428571427, 0.0, 0.20000000000000004, 0.5, 0.08888888888888888, 0.475, 0.0, 0.0, -0.1275, 0.075, 0.3, 0.2375, 0.0, 0.0, 0.0, 0.0375, -0.075, -0.15, 0.0, 0.0, -0.3, 0.0, -0.1, 0.4142857142857143, -0.2, 0.5, 0.43333333333333335, -0.25, 0.5, 0.5083333333333333, 0.325, 0.125, 0.039285714285714285, 0.125, 0.2, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, -0.1, 0.2777777777777778, 0.4875, 0.21428571428571427, 0.25, 0.0, 0.0, 0.0, 0.3333333333333333, 0.5, 0.06666666666666668, 0.14999999999999994, 0.07500000000000001, -0.2, 0.06583333333333333, 0.0, 0.0, 0.04999999999999999, 0.21212121212121213, 0.0, 0.2, -0.1, -0.05, 0.0, 0.0, 0.275, 0.11666666666666665, -0.05, -0.8, 0.2, -0.1607142857142857, 0.7, 0.0, 0.0], "type": "histogram", "uid": "81d6a920-75b9-44fa-9f0c-cf0086d9e678"}, {"marker": {"color": "rgba(0,0,0,1)"}, "x": [31, 8, 15, 7, 14, 6, 4, 16, 5, 4, 11, 7, 6, 3, 7, 5, 3, 2, 8, 31, 6, 7, 2, 4, 51, 4, 4, 6, 18, 10, 6, 7, 1, 1, 4, 6, 2, 4, 1, 3, 2, 1, 31, 26, 3, 2, 3, 2, 9, 2, 3, 1, 1, 7, 1, 3, 1, 2, 8, 2, 2, 3, 1, 1, 3, 3, 4, 2, 383, 1, 2, 1, 2, 6, 1, 1, 1, 9, 3, 37, 1, 1, 3, 2, 2, 2, 1, 1, 1, 1, 3, 0, 1, 3, 8, 1, 1, 1, 1, 2], "yaxis": "y2", "type": "histogram", "uid": "5ceb10e7-cb7a-47c0-9702-e885ee6f98c4"}], {"bargap": 0, "hovermode": "closest", "showlegend": false, "title": "Retweets vs. Polarity", "xaxis": {"domain": [0.0, 0.85], "showgrid": false, "title": "retweets", "zeroline": false}, "yaxis": {"domain": [0.0, 0.85], "showgrid": false, "title": "polarity", "zeroline": false}, "xaxis2": {"domain": [0.85, 1.0], "showgrid": false, "zeroline": false}, "yaxis2": {"domain": [0.85, 1.0], "showgrid": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("34cbf824-5c6e-4d5c-90b1-e313290a8d23"));});</script>



```python
fig = TwtrConvo.plots.create_contour(tweet_df, title='Favorites vs. Polarity', xaxes=['favorites'],
                                     colors=['Electric'])
iplot(fig)
```


<div id="c26a3526-d3e9-4ed3-be70-6cd6543c7aa4" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("c26a3526-d3e9-4ed3-be70-6cd6543c7aa4", [{"colorscale": "Electric", "reversescale": true, "x": [266, 138, 57, 91, 62, 76, 76, 43, 37, 28, 52, 54, 31, 37, 43, 63, 18, 26, 8, 133, 12, 6, 24, 8, 133, 10, 6, 58, 56, 83, 31, 38, 17, 13, 26, 37, 6, 23, 7, 16, 21, 13, 110, 145, 16, 3, 26, 57, 40, 14, 18, 32, 5, 11, 23, 31, 16, 21, 62, 17, 11, 7, 18, 10, 10, 21, 22, 6, 5374, 17, 6, 2, 30, 37, 4, 11, 7, 69, 19, 147, 54, 6, 1, 2, 5, 31, 10, 3, 1, 1, 20, 33, 16, 9, 62, 8, 4, 13, 13, 11], "xaxis": "x", "y": [0.15, 0.4653409090909091, 0.0, 0.0, -0.16, 0.20000000000000004, 0.06666666666666668, 0.25, 0.3, 0.5, 0.10925925925925926, 0.35, -0.1603846153846154, 0.0, 0.0, 0.13055555555555556, 0.0, 0.2333333333333333, 0.1, 0.18333333333333332, 0.0, 0.23392857142857146, -0.2125, -0.0625, 0.008730158730158732, 0.08499999999999999, 0.21428571428571427, 0.0, 0.20000000000000004, 0.5, 0.08888888888888888, 0.475, 0.0, 0.0, -0.1275, 0.075, 0.3, 0.2375, 0.0, 0.0, 0.0, 0.0375, -0.075, -0.15, 0.0, 0.0, -0.3, 0.0, -0.1, 0.4142857142857143, -0.2, 0.5, 0.43333333333333335, -0.25, 0.5, 0.5083333333333333, 0.325, 0.125, 0.039285714285714285, 0.125, 0.2, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, -0.1, 0.2777777777777778, 0.4875, 0.21428571428571427, 0.25, 0.0, 0.0, 0.0, 0.3333333333333333, 0.5, 0.06666666666666668, 0.14999999999999994, 0.07500000000000001, -0.2, 0.06583333333333333, 0.0, 0.0, 0.04999999999999999, 0.21212121212121213, 0.0, 0.2, -0.1, -0.05, 0.0, 0.0, 0.275, 0.11666666666666665, -0.05, -0.8, 0.2, -0.1607142857142857, 0.7, 0.0, 0.0], "yaxis": "y", "type": "histogram2dcontour", "uid": "6edeb9f7-7797-4110-8258-27f8f2ab734d"}, {"marker": {"color": "rgba(0,0,0,1)"}, "xaxis": "x2", "y": [0.15, 0.4653409090909091, 0.0, 0.0, -0.16, 0.20000000000000004, 0.06666666666666668, 0.25, 0.3, 0.5, 0.10925925925925926, 0.35, -0.1603846153846154, 0.0, 0.0, 0.13055555555555556, 0.0, 0.2333333333333333, 0.1, 0.18333333333333332, 0.0, 0.23392857142857146, -0.2125, -0.0625, 0.008730158730158732, 0.08499999999999999, 0.21428571428571427, 0.0, 0.20000000000000004, 0.5, 0.08888888888888888, 0.475, 0.0, 0.0, -0.1275, 0.075, 0.3, 0.2375, 0.0, 0.0, 0.0, 0.0375, -0.075, -0.15, 0.0, 0.0, -0.3, 0.0, -0.1, 0.4142857142857143, -0.2, 0.5, 0.43333333333333335, -0.25, 0.5, 0.5083333333333333, 0.325, 0.125, 0.039285714285714285, 0.125, 0.2, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, -0.1, 0.2777777777777778, 0.4875, 0.21428571428571427, 0.25, 0.0, 0.0, 0.0, 0.3333333333333333, 0.5, 0.06666666666666668, 0.14999999999999994, 0.07500000000000001, -0.2, 0.06583333333333333, 0.0, 0.0, 0.04999999999999999, 0.21212121212121213, 0.0, 0.2, -0.1, -0.05, 0.0, 0.0, 0.275, 0.11666666666666665, -0.05, -0.8, 0.2, -0.1607142857142857, 0.7, 0.0, 0.0], "type": "histogram", "uid": "7201f17d-cb04-446e-abaf-54a50083c412"}, {"marker": {"color": "rgba(0,0,0,1)"}, "x": [266, 138, 57, 91, 62, 76, 76, 43, 37, 28, 52, 54, 31, 37, 43, 63, 18, 26, 8, 133, 12, 6, 24, 8, 133, 10, 6, 58, 56, 83, 31, 38, 17, 13, 26, 37, 6, 23, 7, 16, 21, 13, 110, 145, 16, 3, 26, 57, 40, 14, 18, 32, 5, 11, 23, 31, 16, 21, 62, 17, 11, 7, 18, 10, 10, 21, 22, 6, 5374, 17, 6, 2, 30, 37, 4, 11, 7, 69, 19, 147, 54, 6, 1, 2, 5, 31, 10, 3, 1, 1, 20, 33, 16, 9, 62, 8, 4, 13, 13, 11], "yaxis": "y2", "type": "histogram", "uid": "7cab24dd-951b-4708-abe0-d13eb03266cf"}], {"bargap": 0, "hovermode": "closest", "showlegend": false, "title": "Favorites vs. Polarity", "xaxis": {"domain": [0.0, 0.85], "showgrid": false, "title": "favorites", "zeroline": false}, "yaxis": {"domain": [0.0, 0.85], "showgrid": false, "title": "polarity", "zeroline": false}, "xaxis2": {"domain": [0.85, 1.0], "showgrid": false, "zeroline": false}, "yaxis2": {"domain": [0.85, 1.0], "showgrid": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("c26a3526-d3e9-4ed3-be70-6cd6543c7aa4"));});</script>



```python
fig = TwtrConvo.plots.create_contour(tweet_df, title='Net Influence vs. Polarity', xaxes=['net_influence'],
                                     colors=['Greens'])
iplot(fig)
```


<div id="87bdb8b3-76e2-4033-bdad-1822f229f66b" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("87bdb8b3-76e2-4033-bdad-1822f229f66b", [{"colorscale": "Greens", "reversescale": true, "x": [90638, 54280, 54280, 54280, 15835, 12113, 12113, 4064, 19314, 54280, 3006, 3567, 8502, 19314, 3006, 3006, 20827, 15851, 49232, 2607, 7891, 849341, 3648, 20033, 1949, 6524, 68869, 2631, 1688, 1558, 2166, 1512, 5148, 7891, 1724, 1422, 4140, 1630, 42591, 2528, 2631, 3006, 697, 675, 2166, 118892, 1422, 1232, 697, 1914, 1205, 1724, 4337, 972, 2195, 717, 2528, 1113, 416, 1190, 1471, 1432, 1597, 2528, 803, 605, 494, 1630, 184, 1422, 1471, 32672, 436, 287, 2689, 1074, 1425, 140, 386, 58, 436, 1425, 2873, 2689, 771, 287, 717, 2298, 38244, 32672, 169, 12113, 436, 318, 15, 605, 1145, 416, 416, 312], "xaxis": "x", "y": [0.15, 0.4653409090909091, 0.0, 0.0, -0.16, 0.20000000000000004, 0.06666666666666668, 0.25, 0.3, 0.5, 0.10925925925925926, 0.35, -0.1603846153846154, 0.0, 0.0, 0.13055555555555556, 0.0, 0.2333333333333333, 0.1, 0.18333333333333332, 0.0, 0.23392857142857146, -0.2125, -0.0625, 0.008730158730158732, 0.08499999999999999, 0.21428571428571427, 0.0, 0.20000000000000004, 0.5, 0.08888888888888888, 0.475, 0.0, 0.0, -0.1275, 0.075, 0.3, 0.2375, 0.0, 0.0, 0.0, 0.0375, -0.075, -0.15, 0.0, 0.0, -0.3, 0.0, -0.1, 0.4142857142857143, -0.2, 0.5, 0.43333333333333335, -0.25, 0.5, 0.5083333333333333, 0.325, 0.125, 0.039285714285714285, 0.125, 0.2, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, -0.1, 0.2777777777777778, 0.4875, 0.21428571428571427, 0.25, 0.0, 0.0, 0.0, 0.3333333333333333, 0.5, 0.06666666666666668, 0.14999999999999994, 0.07500000000000001, -0.2, 0.06583333333333333, 0.0, 0.0, 0.04999999999999999, 0.21212121212121213, 0.0, 0.2, -0.1, -0.05, 0.0, 0.0, 0.275, 0.11666666666666665, -0.05, -0.8, 0.2, -0.1607142857142857, 0.7, 0.0, 0.0], "yaxis": "y", "type": "histogram2dcontour", "uid": "1786fc30-8df6-4d70-87d0-5e5c10c5384e"}, {"marker": {"color": "rgba(0,0,0,1)"}, "xaxis": "x2", "y": [0.15, 0.4653409090909091, 0.0, 0.0, -0.16, 0.20000000000000004, 0.06666666666666668, 0.25, 0.3, 0.5, 0.10925925925925926, 0.35, -0.1603846153846154, 0.0, 0.0, 0.13055555555555556, 0.0, 0.2333333333333333, 0.1, 0.18333333333333332, 0.0, 0.23392857142857146, -0.2125, -0.0625, 0.008730158730158732, 0.08499999999999999, 0.21428571428571427, 0.0, 0.20000000000000004, 0.5, 0.08888888888888888, 0.475, 0.0, 0.0, -0.1275, 0.075, 0.3, 0.2375, 0.0, 0.0, 0.0, 0.0375, -0.075, -0.15, 0.0, 0.0, -0.3, 0.0, -0.1, 0.4142857142857143, -0.2, 0.5, 0.43333333333333335, -0.25, 0.5, 0.5083333333333333, 0.325, 0.125, 0.039285714285714285, 0.125, 0.2, 0.0, 0.21428571428571427, 0.0, 0.0, 0.0, -0.1, 0.2777777777777778, 0.4875, 0.21428571428571427, 0.25, 0.0, 0.0, 0.0, 0.3333333333333333, 0.5, 0.06666666666666668, 0.14999999999999994, 0.07500000000000001, -0.2, 0.06583333333333333, 0.0, 0.0, 0.04999999999999999, 0.21212121212121213, 0.0, 0.2, -0.1, -0.05, 0.0, 0.0, 0.275, 0.11666666666666665, -0.05, -0.8, 0.2, -0.1607142857142857, 0.7, 0.0, 0.0], "type": "histogram", "uid": "33bb4b72-6548-4c26-979f-23fc55dcd045"}, {"marker": {"color": "rgba(0,0,0,1)"}, "x": [90638, 54280, 54280, 54280, 15835, 12113, 12113, 4064, 19314, 54280, 3006, 3567, 8502, 19314, 3006, 3006, 20827, 15851, 49232, 2607, 7891, 849341, 3648, 20033, 1949, 6524, 68869, 2631, 1688, 1558, 2166, 1512, 5148, 7891, 1724, 1422, 4140, 1630, 42591, 2528, 2631, 3006, 697, 675, 2166, 118892, 1422, 1232, 697, 1914, 1205, 1724, 4337, 972, 2195, 717, 2528, 1113, 416, 1190, 1471, 1432, 1597, 2528, 803, 605, 494, 1630, 184, 1422, 1471, 32672, 436, 287, 2689, 1074, 1425, 140, 386, 58, 436, 1425, 2873, 2689, 771, 287, 717, 2298, 38244, 32672, 169, 12113, 436, 318, 15, 605, 1145, 416, 416, 312], "yaxis": "y2", "type": "histogram", "uid": "af0b0e3b-fa29-4fa6-b922-d8c1e2f01628"}], {"bargap": 0, "hovermode": "closest", "showlegend": false, "title": "Net Influence vs. Polarity", "xaxis": {"domain": [0.0, 0.85], "showgrid": false, "title": "net_influence", "zeroline": false}, "yaxis": {"domain": [0.0, 0.85], "showgrid": false, "title": "polarity", "zeroline": false}, "xaxis2": {"domain": [0.85, 1.0], "showgrid": false, "zeroline": false}, "yaxis2": {"domain": [0.85, 1.0], "showgrid": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("87bdb8b3-76e2-4033-bdad-1822f229f66b"));});</script>


#### Weight the sentiment and regenerate the guage with our weighted values

Finally we'll weight the polarity and subjectivity based on our meta data of retweets, favorites, and net_influence using the "get_weighted_sentiment" function in the twtrconvo module.  For the sake of the example we'll use the default in which each is weighted equally, however by using the "weights" keyword you could weight each parameter differently based on previous analysis results.


```python
weighted_sentiment = TwtrConvo.twtrconvo.get_weighted_sentiment(tweet_df)

fig = TwtrConvo.plots.create_sentiment_gauge(
        weighted_sentiment[0], weighted_sentiment[1])
iplot(fig)
```


<div id="2b42549b-4a8d-422b-939e-beebedc534d3" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("2b42549b-4a8d-422b-939e-beebedc534d3", [{"direction": "clockwise", "domain": {"x": [0.0, 0.48]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "-1", "0", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "9e212a22-5056-456e-a44f-c247e4f8eb67"}, {"direction": "clockwise", "domain": {"x": [0.0, 0.48]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Polarity", "Negative", "Neutral", "Positive"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "3b650fde-79f5-4014-bc00-493bf05df821"}, {"direction": "clockwise", "domain": {"x": [0.52, 1.0]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "0", "0.5", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(178, 255, 102)", "rgb(192, 192, 192)", "rgb(255, 102, 102)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "e829f41b-c4b5-43a9-b8b9-80c69fcede7e"}, {"direction": "clockwise", "domain": {"x": [0.52, 1.0]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Subjectivity", "Very Objective", "Neutral", "Very Subjective"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(178, 255, 102)", "rgb(192, 192, 192)", "rgb(255, 102, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "ad449f4d-d59c-49d8-8aca-3274b20605a7"}], {"annotations": [{"showarrow": false, "text": "0.081", "x": 0.24, "xref": "paper", "y": 0.45, "yref": "paper"}, {"showarrow": false, "text": "0.186", "x": 0.76, "xref": "paper", "y": 0.45, "yref": "paper"}], "shapes": [{"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.23503161270339643 0.5005613623348144 L 0.25684087004443357 0.6490516188981069 L 0.24496838729660356 0.49943863766518554 Z", "type": "path", "xref": "paper", "yref": "paper"}, {"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.7568042271247344 0.4961546085076137 L 0.6446382552284124 0.5958731862579684 L 0.7631957728752656 0.5038453914923863 Z", "type": "path", "xref": "paper", "yref": "paper"}], "xaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}, "yaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("2b42549b-4a8d-422b-939e-beebedc534d3"));});</script>


## Top 5 Future Upgrades

1. Backend database to store data so that time series sentiment analysis can be added
2. Pair with financial data and build Neural Network for predicting price movement based on sentiment
3. Create financial and sentiment comparisons between multiple companies
4. Create a web application by embedding plotly plots into dash dashboard with a drop down for supported companies
5. Set up unit testing and organize dependencies so the library can be added to PyPI and pip installed
