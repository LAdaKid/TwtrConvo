
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

ticker = 'SQ'

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
    0    238  1123683790260514816       StockTwits   
    1    266  1123682520040660993  CNBCClosingBell   
    2    187  1123687046973992960        alsabogal   
    3    112  1123699101915394051       _SeanDavid   
    4     93  1123708151323332609         dee_bosa   
    
                                                   tweet  \
    0  $SQ reports earnings:\n\nEPS $0.11 vs. est $0....   
    1  After hours earnings movers: $FIT $SQ $QCOM ht...   
    2  $SQ - easy to say after the fact but fact that...   
    3  Square Earnings: $SQ\n\n$959M net rev, +43% y/...   
    4  40 minutes into the Square analyst call before...   
    
                                                    text  favorites  retweets  \
    0  SQ reports earnings EPS 0 11 vs est 0 08 Revs ...         22         6   
    1            After hours earnings movers FIT SQ QCOM         10         5   
    2  SQ easy to say after the fact but fact that it...         19         3   
    3  Square Earnings SQ 959M net rev 43 y y Guided ...         30        14   
    4  40 minutes into the Square analyst call before...         17         8   
    
       followers  following  net_influence  net_influencerank  retweetsrank  \
    0     610456     123548         486908              271.0         269.5   
    1      93327         64          93263              269.0         266.5   
    2      46071        198          45873              263.0         259.5   
    3      10508       2345           8163              242.5         273.0   
    4      15455       3426          12029              248.0         272.0   
    
       favoritesrank   rank  
    0          268.0  808.5  
    1          256.0  791.5  
    2          266.5  789.0  
    3          270.0  785.5  
    4          264.5  784.5  


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

    StockTwits (22 Favorites, 6 Retweets, Net Influence 486908) : 
     $SQ reports earnings:
    
    EPS $0.11 vs. est $0.08
    Revs $489 million vs. est $478 million
    
    https://t.co/UkuWHXfbRG 
    
    CNBCClosingBell (10 Favorites, 5 Retweets, Net Influence 93263) : 
     After hours earnings movers: $FIT $SQ $QCOM https://t.co/uGXkapNpAG 
    
    alsabogal (19 Favorites, 3 Retweets, Net Influence 45873) : 
     $SQ - easy to say after the fact but fact that it couldn't rally with other payment names &amp; also couldn't hold 200d + saw somewhere Dorsey was making sales was crappy setup for earnings..analysts talk to company and do their due diligence...nothing bullish apparently came from it 
    
    _SeanDavid (30 Favorites, 14 Retweets, Net Influence 8163) : 
     Square Earnings: $SQ
    
    $959M net rev, +43% y/y
    Guided +43% rev growth 19'
    Sub rev 24% of total, highest ever
    Cash App volume +2.5X
    Highest avg loan size
    Acceleration in Cash App
    49% large sellers
    Hardware rev +26.3%, deceleration
    Partnered w/ Sumitomo in Japan
    $1.6B cash! https://t.co/fVt8LcI6GU 
    
    dee_bosa (17 Favorites, 8 Retweets, Net Influence 12029) : 
     40 minutes into the Square analyst call before we got a direct question on:
    - decelerating large merchant growth
    - weaker than expected Q2 guidance
    - weaker than expected GMV growth
    $SQ https://t.co/Wl1KDLDdIM 
    


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



<div id="354e1a77-3610-4ea8-b2a9-dc08fa0f3ebe" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("354e1a77-3610-4ea8-b2a9-dc08fa0f3ebe", [{"domain": {"column": 0}, "hole": 0.4, "labels": ["square", "earnings", "guidance", "yoy", "rev", "q1", "revenue", "vs", "growth", "adj"], "name": "Tweets", "values": [18, 16, 12, 9, 8, 8, 7, 7, 7, 7], "type": "pie", "uid": "48af9a4f-1492-437f-82e0-4b648337a7fb"}, {"domain": {"column": 1}, "hole": 0.4, "labels": ["great", "day", "could", "run", "twlo", "long", "today", "base", "would", "puru"], "name": "Replies", "values": [3, 3, 3, 3, 2, 2, 2, 2, 2, 2], "type": "pie", "uid": "637f9c35-8a80-4e5f-bc7a-e45621687602"}], {"annotations": [{"font": {"size": 20}, "showarrow": false, "text": "Tweets", "x": 0.2, "y": 0.5}, {"font": {"size": 20}, "showarrow": false, "text": "Replies", "x": 0.8, "y": 0.5}], "grid": {"columns": 2, "rows": 1}, "title": "Word Frequency"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("354e1a77-3610-4ea8-b2a9-dc08fa0f3ebe"));});</script>


### Sentiment Gauge

Using TextBlob we will get a general sentiment of all the tweets and display it on a guage using plotly.


```python
fig = TwtrConvo.plots.create_sentiment_gauge(tweet_blob)
iplot(fig)
```


<div id="974174a7-7882-4e74-baa3-bc1ce26c6a7e" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("974174a7-7882-4e74-baa3-bc1ce26c6a7e", [{"direction": "clockwise", "domain": {"x": [0.0, 0.48]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "-1", "0", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "dfd7868d-c2c0-4a61-9fd3-e32f0fee7d75"}, {"direction": "clockwise", "domain": {"x": [0.0, 0.48]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Polarity", "Negative", "Neutral", "Positive"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(255, 102, 102)", "rgb(192, 192, 192)", "rgb(178, 255, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "5ba6a360-d682-4360-bd3d-512c5a6f77d7"}, {"direction": "clockwise", "domain": {"x": [0.52, 1.0]}, "hole": 0.4, "hoverinfo": "none", "labels": ["-", "0", "0.5", "1"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(178, 255, 102)", "rgb(192, 192, 192)", "rgb(255, 102, 102)"], "line": {"width": 0}}, "name": "Gauge", "rotation": 108, "showlegend": false, "textinfo": "label", "textposition": "outside", "values": [40, 20, 20, 20], "type": "pie", "uid": "82f3bc17-1ec7-47bd-a900-a71bf1ac969f"}, {"direction": "clockwise", "domain": {"x": [0.52, 1.0]}, "hole": 0.3, "hoverinfo": "none", "labels": ["Subjectivity", "Very Objective", "Neutral", "Very Subjective"], "marker": {"colors": ["rgb(255, 255, 255)", "rgb(178, 255, 102)", "rgb(192, 192, 192)", "rgb(255, 102, 102)"]}, "name": "Gauge", "rotation": 90, "showlegend": false, "textinfo": "label", "textposition": "inside", "values": [50, 16.666666666666668, 16.666666666666668, 16.666666666666668], "type": "pie", "uid": "0b72d554-104a-4fcc-8b5b-28aaa5a4057e"}], {"annotations": [{"showarrow": false, "text": "0.085", "x": 0.24, "xref": "paper", "y": 0.45, "yref": "paper"}, {"showarrow": false, "text": "0.482", "x": 0.76, "xref": "paper", "y": 0.45, "yref": "paper"}], "shapes": [{"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.23503529482811533 0.5005930451553312 L 0.25779135465993575 0.6489411551565396 L 0.24496470517188465 0.4994069548446688 Z", "type": "path", "xref": "paper", "yref": "paper"}, {"fillcolor": "rgba(44, 160, 101, 0.5)", "line": {"width": 0.5}, "path": "M 0.755006285051948 0.49974937873673275 L 0.7524813621019824 0.649811448441561 L 0.764993714948052 0.5002506212632672 Z", "type": "path", "xref": "paper", "yref": "paper"}], "xaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}, "yaxis": {"showgrid": false, "showticklabels": false, "zeroline": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("974174a7-7882-4e74-baa3-bc1ce26c6a7e"));});</script>


### Boxplots

Let's take a look at spread of retweets and favorites from the top ranked tweets.


```python
fig = TwtrConvo.plots.create_boxplot(tweet_df)
iplot(fig)
```


<div id="85aa0cc5-6bf0-4d53-87e5-3bbfe5ad68f1" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("85aa0cc5-6bf0-4d53-87e5-3bbfe5ad68f1", [{"boxpoints": "all", "fillcolor": "rgba(255, 65, 54, 0.5)", "jitter": 0.5, "line": {"width": 1}, "marker": {"color": "rgba(255, 65, 54, 0.5)", "size": 2}, "name": "retweets", "whiskerwidth": 0.2, "x": [6, 5, 3, 14, 8, 6, 6, 3, 2, 2, 3, 2, 3, 5, 3, 4, 2, 1, 2, 1, 6, 3, 3, 3, 2, 4, 1, 1, 1, 1, 2, 2, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 2, 2, 1, 2, 1, 0, 1, 0], "type": "box", "uid": "8b552334-45a5-487d-8cb2-9b5f7a9e8876"}, {"boxpoints": "all", "fillcolor": "rgba(93, 164, 214, 0.5)", "jitter": 0.5, "line": {"width": 1}, "marker": {"color": "rgba(93, 164, 214, 0.5)", "size": 2}, "name": "favorites", "whiskerwidth": 0.2, "x": [22, 10, 19, 30, 17, 10, 34, 6, 9, 9, 4, 35, 4, 63, 4, 12, 16, 9, 17, 11, 2, 6, 2, 9, 13, 2, 4, 8, 7, 5, 2, 4, 27, 8, 13, 19, 1, 5, 9, 5, 9, 4, 5, 5, 4, 6, 3, 5, 4, 5], "type": "box", "uid": "1ac8f911-7754-4ef5-b99d-284aa5486178"}], {"title": "Retweets and Favorites"}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("85aa0cc5-6bf0-4d53-87e5-3bbfe5ad68f1"));});</script>


### Distribution Plot

Next let's take a look at the overall net influence of the top tweets.  In order to do this we'll look at the distribution with the bins 0, 500, 1000 and 5000.


```python
fig = TwtrConvo.plots.create_distplot(tweet_df)
iplot(fig)
```


<div id="1cb307ef-a1ab-40ad-8d04-ccee6137cbc0" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("1cb307ef-a1ab-40ad-8d04-ccee6137cbc0", [{"autobinx": false, "histnorm": "probability density", "legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)"}, "name": "net_influence", "opacity": 0.7, "x": [486908, 93263, 45873, 8163, 12029, 19793, 5648, 665758, 665758, 41623, 68807, 4888, 58472, 3322, 17156, 3445, 4291, 8163, 2486, 4647, 19758, 2699, 19758, 1910, 1910, 10325, 4616, 1910, 1910, 1910, 4157, 1211, 12020, 92941, 12020, 6740, 38071, 58472, 460, 26077, 7698, 62623, 374, 373, 846, 196, 874, 5275, 373, 4616], "xaxis": "x", "xbins": {"end": 665758.0, "size": 0.0, "start": 196.0}, "yaxis": "y", "type": "histogram", "uid": "8b8ed451-8473-4169-b894-c19434689972"}, {"legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)"}, "mode": "lines", "name": "net_influence", "showlegend": false, "x": [196.0, 1527.124, 2858.248, 4189.371999999999, 5520.496, 6851.62, 8182.744, 9513.868, 10844.992, 12176.116, 13507.24, 14838.364, 16169.488, 17500.612, 18831.736, 20162.86, 21493.984, 22825.108, 24156.232, 25487.356, 26818.48, 28149.604, 29480.728, 30811.852, 32142.976, 33474.1, 34805.224, 36136.348, 37467.472, 38798.596, 40129.72, 41460.844, 42791.968, 44123.092, 45454.216, 46785.34, 48116.464, 49447.588, 50778.712, 52109.836, 53440.96, 54772.084, 56103.208, 57434.332, 58765.456, 60096.58, 61427.704, 62758.828, 64089.952, 65421.076, 66752.2, 68083.324, 69414.448, 70745.572, 72076.696, 73407.82, 74738.944, 76070.068, 77401.192, 78732.316, 80063.44, 81394.564, 82725.688, 84056.812, 85387.936, 86719.06, 88050.184, 89381.308, 90712.432, 92043.556, 93374.68, 94705.804, 96036.928, 97368.052, 98699.176, 100030.3, 101361.424, 102692.548, 104023.672, 105354.796, 106685.92, 108017.044, 109348.168, 110679.292, 112010.416, 113341.54, 114672.664, 116003.788, 117334.912, 118666.036, 119997.16, 121328.284, 122659.408, 123990.532, 125321.656, 126652.78, 127983.904, 129315.028, 130646.152, 131977.276, 133308.4, 134639.524, 135970.648, 137301.772, 138632.896, 139964.02, 141295.144, 142626.268, 143957.392, 145288.516, 146619.64, 147950.764, 149281.888, 150613.012, 151944.136, 153275.26, 154606.384, 155937.508, 157268.632, 158599.756, 159930.88, 161262.004, 162593.128, 163924.252, 165255.376, 166586.5, 167917.624, 169248.748, 170579.872, 171910.996, 173242.12, 174573.244, 175904.368, 177235.492, 178566.616, 179897.74, 181228.864, 182559.988, 183891.112, 185222.236, 186553.36, 187884.484, 189215.608, 190546.732, 191877.856, 193208.98, 194540.104, 195871.228, 197202.352, 198533.476, 199864.6, 201195.724, 202526.848, 203857.972, 205189.096, 206520.22, 207851.344, 209182.468, 210513.592, 211844.716, 213175.84, 214506.964, 215838.088, 217169.212, 218500.336, 219831.46, 221162.584, 222493.708, 223824.832, 225155.956, 226487.08, 227818.204, 229149.328, 230480.452, 231811.576, 233142.7, 234473.824, 235804.948, 237136.072, 238467.196, 239798.32, 241129.444, 242460.568, 243791.692, 245122.816, 246453.94, 247785.064, 249116.188, 250447.312, 251778.436, 253109.56, 254440.684, 255771.808, 257102.932, 258434.056, 259765.18, 261096.304, 262427.428, 263758.552, 265089.676, 266420.8, 267751.924, 269083.048, 270414.172, 271745.296, 273076.42, 274407.544, 275738.668, 277069.792, 278400.916, 279732.04, 281063.164, 282394.288, 283725.412, 285056.536, 286387.66, 287718.784, 289049.908, 290381.032, 291712.156, 293043.28, 294374.404, 295705.528, 297036.652, 298367.776, 299698.9, 301030.024, 302361.148, 303692.272, 305023.396, 306354.52, 307685.644, 309016.768, 310347.892, 311679.016, 313010.14, 314341.264, 315672.388, 317003.512, 318334.636, 319665.76, 320996.884, 322328.008, 323659.132, 324990.256, 326321.38, 327652.504, 328983.628, 330314.752, 331645.876, 332977.0, 334308.124, 335639.248, 336970.372, 338301.496, 339632.62, 340963.744, 342294.868, 343625.992, 344957.116, 346288.24, 347619.364, 348950.488, 350281.612, 351612.736, 352943.86, 354274.984, 355606.108, 356937.232, 358268.356, 359599.48, 360930.604, 362261.728, 363592.852, 364923.976, 366255.1, 367586.224, 368917.348, 370248.472, 371579.596, 372910.72, 374241.844, 375572.968, 376904.092, 378235.216, 379566.34, 380897.464, 382228.588, 383559.712, 384890.836, 386221.96, 387553.084, 388884.208, 390215.332, 391546.456, 392877.58, 394208.704, 395539.828, 396870.952, 398202.076, 399533.2, 400864.324, 402195.448, 403526.572, 404857.696, 406188.82, 407519.944, 408851.068, 410182.192, 411513.316, 412844.44, 414175.564, 415506.688, 416837.812, 418168.936, 419500.06, 420831.184, 422162.308, 423493.432, 424824.556, 426155.68, 427486.804, 428817.928, 430149.052, 431480.176, 432811.3, 434142.424, 435473.548, 436804.672, 438135.796, 439466.92, 440798.044, 442129.168, 443460.292, 444791.416, 446122.54, 447453.664, 448784.788, 450115.912, 451447.036, 452778.16, 454109.284, 455440.408, 456771.532, 458102.656, 459433.78, 460764.904, 462096.028, 463427.152, 464758.276, 466089.4, 467420.524, 468751.648, 470082.772, 471413.896, 472745.02, 474076.144, 475407.268, 476738.392, 478069.516, 479400.64, 480731.764, 482062.888, 483394.012, 484725.136, 486056.26, 487387.384, 488718.508, 490049.632, 491380.756, 492711.88, 494043.004, 495374.128, 496705.252, 498036.376, 499367.5, 500698.624, 502029.748, 503360.872, 504691.996, 506023.12, 507354.244, 508685.368, 510016.492, 511347.616, 512678.74, 514009.864, 515340.988, 516672.112, 518003.236, 519334.36, 520665.484, 521996.608, 523327.732, 524658.856, 525989.98, 527321.104, 528652.228, 529983.352, 531314.476, 532645.6, 533976.724, 535307.848, 536638.972, 537970.096, 539301.22, 540632.344, 541963.468, 543294.592, 544625.716, 545956.84, 547287.964, 548619.088, 549950.212, 551281.336, 552612.46, 553943.584, 555274.708, 556605.832, 557936.956, 559268.08, 560599.204, 561930.328, 563261.452, 564592.576, 565923.7, 567254.824, 568585.948, 569917.072, 571248.196, 572579.32, 573910.444, 575241.568, 576572.692, 577903.816, 579234.94, 580566.064, 581897.188, 583228.312, 584559.436, 585890.56, 587221.684, 588552.808, 589883.932, 591215.056, 592546.18, 593877.304, 595208.428, 596539.552, 597870.676, 599201.8, 600532.924, 601864.048, 603195.172, 604526.296, 605857.42, 607188.544, 608519.668, 609850.792, 611181.916, 612513.04, 613844.164, 615175.288, 616506.412, 617837.536, 619168.66, 620499.784, 621830.908, 623162.032, 624493.156, 625824.28, 627155.404, 628486.528, 629817.652, 631148.776, 632479.9, 633811.024, 635142.148, 636473.272, 637804.396, 639135.52, 640466.644, 641797.768, 643128.892, 644460.016, 645791.14, 647122.264, 648453.388, 649784.512, 651115.636, 652446.76, 653777.884, 655109.008, 656440.132, 657771.256, 659102.38, 660433.504, 661764.628, 663095.752, 664426.876], "xaxis": "x", "y": [5.235380131272898e-06, 5.254995460067164e-06, 5.272737581363527e-06, 5.288589545500363e-06, 5.30253649697726e-06, 5.314565697761028e-06, 5.324666546569401e-06, 5.33283059409174e-06, 5.339051554117055e-06, 5.343325310550761e-06, 5.345649920312735e-06, 5.346025612120333e-06, 5.344454781171133e-06, 5.340941979751174e-06, 5.335493903805284e-06, 5.328119375516866e-06, 5.318829321954902e-06, 5.307636749856444e-06, 5.294556716622551e-06, 5.279606297615595e-06, 5.262804549855154e-06, 5.244172472218622e-06, 5.223732962261428e-06, 5.20151076977982e-06, 5.177532447247006e-06, 5.151826297260633e-06, 5.124422317146447e-06, 5.095352140869203e-06, 5.064648978407624e-06, 5.032347552755441e-06, 4.998484034715238e-06, 4.963095975655758e-06, 4.926222238407016e-06, 4.887902926470401e-06, 4.848179311723257e-06, 4.807093760799371e-06, 4.764689660327757e-06, 4.721011341212937e-06, 4.6761040021398535e-06, 4.630013632486048e-06, 4.5827869348226806e-06, 4.534471247184327e-06, 4.485114465285406e-06, 4.434764964858336e-06, 4.383471524285482e-06, 4.33128324769328e-06, 4.2782494886728736e-06, 4.224419774787055e-06, 4.16984373301848e-06, 4.114571016308764e-06, 4.05865123133242e-06, 4.002133867643684e-06, 3.9450682283279035e-06, 3.8875033622827105e-06, 3.829487998247289e-06, 3.7710704806911135e-06, 3.7122987076662906e-06, 3.6532200707202543e-06, 3.593881396958092e-06, 3.5343288933361606e-06, 3.474608093260975e-06, 3.4147638055596522e-06, 3.3548400658804166e-06, 3.294880090573997e-06, 3.23492623309901e-06, 3.1750199429868093e-06, 3.1152017273937753e-06, 3.0555111152614994e-06, 2.995986624098146e-06, 2.9366657293869694e-06, 2.8775848366211803e-06, 2.8187792559574215e-06, 2.7602831794736233e-06, 2.702129661010686e-06, 2.6443505985713082e-06, 2.5869767192434694e-06, 2.530037566610494e-06, 2.473561490604357e-06, 2.4175756397539053e-06, 2.3621059557749296e-06, 2.307177170444669e-06, 2.252812804699257e-06, 2.199035169888812e-06, 2.1458653711214454e-06, 2.093323312624332e-06, 2.041427705047162e-06, 1.990196074630802e-06, 1.939644774161779e-06, 1.8897889956313848e-06, 1.8406427845165486e-06, 1.7922190555984374e-06, 1.74452961023371e-06, 1.6975851549926676e-06, 1.6513953215781773e-06, 1.6059686879390415e-06, 1.5613128004916358e-06, 1.5174341973640047e-06, 1.474338432577191e-06, 1.432030101079415e-06, 1.3905128645497565e-06, 1.3497894778892658e-06, 1.3098618163188009e-06, 1.2707309030046141e-06, 1.232396937134354e-06, 1.1948593223682076e-06, 1.1581166955919018e-06, 1.1221669559004931e-06, 1.0870072937442235e-06, 1.0526342201700744e-06, 1.0190435960952064e-06, 9.862306615510118e-07, 9.541900648391685e-07, 9.229158915437641e-07, 8.924016933463082e-07, 8.626405165932038e-07, 8.33624930568046e-07, 8.053470554238954e-07, 7.777985897334803e-07, 7.509708376180725e-07, 7.248547354185245e-07, 6.99440877874723e-07, 6.747195437824143e-07, 6.506807210990042e-07, 6.273141314725879e-07, 6.046092541709927e-07, 5.825553493901464e-07, 5.611414809235189e-07, 5.403565381767451e-07, 5.201892575138391e-07, 5.006282429236429e-07, 4.816619859972702e-07, 4.6327888520937176e-07, 4.4546726449803404e-07, 4.282153911399803e-07, 4.115114929195683e-07, 3.9534377459176265e-07, 3.7970043364089454e-07, 3.645696753385411e-07, 3.499397271052972e-07, 3.357988521825553e-07, 3.221353626216878e-07, 3.089376315991683e-07, 2.961941050672909e-07, 2.8389331275111444e-07, 2.7202387850320614e-07, 2.6057453002857744e-07, 2.495341079929759e-07, 2.388915745283719e-07, 2.286360211500965e-07, 2.1875667610061724e-07, 2.0924291113540469e-07, 2.0008424776675802e-07, 1.9127036298177803e-07, 1.8279109445096975e-07, 1.746364452441675e-07, 1.667965880706427e-07, 1.5926186906037269e-07, 1.5202281110350445e-07, 1.450701167650706e-07, 1.3839467079199022e-07, 1.3198754222931287e-07, 1.258399861625713e-07, 1.1994344510295643e-07, 1.1428955003186346e-07, 1.088701211211553e-07, 1.0367716814525258e-07, 9.870289060091137e-08, 9.393967755026836e-08, 8.93801072024307e-08, 8.501694624857589e-08, 8.08431489651882e-08, 7.685185609970938e-08, 7.303639355252255e-08, 6.939027086881116e-08, 6.590717955345625e-08, 6.258099122174363e-08, 5.9405755598256863e-08, 5.637569837593039e-08, 5.3485218946834765e-08, 5.07288880158553e-08, 4.8101445108022285e-08, 4.559779597983806e-08, 4.321300994454174e-08, 4.094231712084753e-08, 3.87811056142861e-08, 3.672491863988234e-08, 3.4769451594506366e-08, 3.2910549086841816e-08, 3.1144201932532306e-08, 2.9466544121685655e-08, 2.787384976554111e-08, 2.636253002873913e-08, 2.4929130053271377e-08, 2.357032587983623e-08, 2.2282921371980206e-08, 2.1063845148066302e-08, 1.9910147525781956e-08, 1.881899748357715e-08, 1.778767964310902e-08, 1.681359127646534e-08, 1.5894239341641862e-08, 1.502723754946093e-08, 1.4210303464838369e-08, 1.3441255645035661e-08, 1.2718010817271399e-08, 1.2038581097812208e-08, 1.1401071254418785e-08, 1.080367601378478e-08, 1.024467741537941e-08, 9.72244221288415e-09, 9.235419324203003e-09, 8.782137330822597e-09, 8.361202027104677e-09, 7.971294019905951e-09, 7.611166378743618e-09, 7.279642336553985e-09, 6.9756130409303854e-09, 6.698035355572678e-09, 6.445929711534767e-09, 6.218378007718898e-09, 6.014521559935622e-09, 5.83355909772598e-09, 5.67474480802833e-09, 5.537386424665649e-09, 5.42084336253001e-09, 5.324524895250029e-09, 5.2478883750431595e-09, 5.190437493378649e-09, 5.151720581008576e-09, 5.1313289458630915e-09, 5.128895247252536e-09, 5.144091904772749e-09, 5.176629540271135e-09, 5.226255451199528e-09, 5.292752113655582e-09, 5.375935713397632e-09, 5.475654703107931e-09, 5.591788384176736e-09, 5.7242455112842095e-09, 5.87296291806825e-09, 6.037904162185294e-09, 6.219058188096037e-09, 6.416438005940346e-09, 6.6300793849043915e-09, 6.860039559528455e-09, 7.10639594745573e-09, 7.3692448771807736e-09, 7.648700324420655e-09, 7.94489265580232e-09, 8.257967378636538e-09, 8.58808389563022e-09, 8.93541426347753e-09, 9.300141954362465e-09, 9.682460619503984e-09, 1.008257285397812e-08, 1.050068896215808e-08, 1.0937025723226638e-08, 1.1391805156329522e-08, 1.1865253285059276e-08, 1.235759890108154e-08, 1.2869072326841749e-08, 1.3399904177418947e-08, 1.3950324121724529e-08, 1.452055964337645e-08, 1.511083480171367e-08, 1.572136899355132e-08, 1.6352375716412106e-08, 1.700406133410697e-08, 1.7676623845672343e-08, 1.83702516588067e-08, 1.908512236908295e-08, 1.982140154634443e-08, 2.057924152982141e-08, 2.1358780233632177e-08, 2.2160139964454636e-08, 2.29834262532744e-08, 2.3828726703229163e-08, 2.4696109855678586e-08, 2.5585624076733645e-08, 2.6497296466575996e-08, 2.743113179398996e-08, 2.838711145861353e-08, 2.936519248349104e-08, 3.036530654057876e-08, 3.13873590119138e-08, 3.2431228089208075e-08, 3.3496763914669513e-08, 3.4583787765884606e-08, 3.569209128761608e-08, 3.682143577338193e-08, 3.79715514996789e-08, 3.914213711570311e-08, 4.0332859091396734e-08, 4.1543351226614036e-08, 4.2773214224153086e-08, 4.402201532933963e-08, 4.528928803877982e-08, 4.6574531880811593e-08, 4.7877212270092146e-08, 4.919676043864681e-08, 5.053257344558818e-08, 5.188401426757768e-08, 5.3250411971960803e-08, 5.4631061974349316e-08, 5.60252263822561e-08, 5.743213442621173e-08, 5.88509829796003e-08, 6.028093716825507e-08, 6.172113107064187e-08, 6.317066850924624e-08, 6.462862393354272e-08, 6.609404339470207e-08, 6.756594561193915e-08, 6.904332313016063e-08, 7.052514356831503e-08, 7.201035095758519e-08, 7.349786716830258e-08, 7.498659342418997e-08, 7.647541190227005e-08, 7.796318741650598e-08, 7.944876918296192e-08, 8.093099266400278e-08, 8.240868148877717e-08, 8.388064944695526e-08, 8.534570255243116e-08, 8.680264117342856e-08, 8.825026222519554e-08, 8.968736142121871e-08, 9.11127355786415e-08, 9.252518497333264e-08, 9.392351573982444e-08, 9.53065423111158e-08, 9.667308989313127e-08, 9.802199696842701e-08, 9.935211782354935e-08, 1.0066232509428065e-07, 1.0195151232284951e-07, 1.0321859652103545e-07, 1.0446252073297604e-07, 1.0568225659136527e-07, 1.0687680686064135e-07, 1.0804520796068089e-07, 1.0918653246445487e-07, 1.102998915630608e-07, 1.113844374915159e-07, 1.1243936590869458e-07, 1.1346391822480172e-07, 1.1445738386980523e-07, 1.1541910249630131e-07, 1.1634846611035747e-07, 1.1724492112395928e-07, 1.1810797032280202e-07, 1.1893717474328819e-07, 1.1973215545273721e-07, 1.2049259522697662e-07, 1.212182401196634e-07, 1.2190890091788147e-07, 1.2256445447877525e-07, 1.2318484494220964e-07, 1.237700848146962e-07, 1.2432025592007987e-07, 1.2483551021276733e-07, 1.2531607044955662e-07, 1.2576223071643915e-07, 1.2617435680705505e-07, 1.265528864498137e-07, 1.2689832938102253e-07, 1.2721126726172005e-07, 1.2749235343625818e-07, 1.2774231253104506e-07, 1.279619398922315e-07, 1.2815210086149144e-07, 1.2831372988943488e-07, 1.2844782948657151e-07, 1.285554690121312e-07, 1.2863778330143396e-07, 1.2869597113289206e-07, 1.2873129353611886e-07, 1.2874507194299807e-07, 1.2873868618396327e-07, 1.2871357233211027e-07, 1.286712203981508e-07, 1.2861317187958217e-07, 1.2854101716782128e-07, 1.2845639281740637e-07, 1.2836097868172832e-07, 1.282564949200935e-07, 1.2814469888125687e-07, 1.2802738186889187e-07, 1.2790636579477708e-07, 1.2778349972577813e-07, 1.2766065633100752e-07, 1.2753972823580914e-07, 1.2742262428948984e-07, 1.2731126575397177e-07, 1.2720758242076825e-07, 1.2711350866392295e-07, 1.2703097943674363e-07, 1.2696192622036972e-07, 1.2690827293237458e-07, 1.2687193180377004e-07, 1.2685479923292508e-07, 1.268587516250265e-07, 1.2688564122583048e-07, 1.2693729195852836e-07, 1.2701549527263873e-07, 1.271220060138764e-07, 1.2725853832399675e-07, 1.2742676157962504e-07, 1.2762829637907636e-07, 1.2786471058616085e-07, 1.281375154399198e-07, 1.284481617391867e-07, 1.2879803611078668e-07, 1.2918845737009683e-07, 1.29620672982568e-07, 1.3009585563468137e-07, 1.306150999226582e-07, 1.3117941916706803e-07, 1.3178974236129336e-07, 1.324469112615985e-07, 1.331516776263235e-07, 1.3390470061148037e-07, 1.347065443297619e-07, 1.3555767557969653e-07, 1.3645846175138262e-07, 1.3740916891491788e-07, 1.3840996009731172e-07, 1.3946089375331501e-07, 1.4056192243523993e-07, 1.4171289166646214e-07, 1.429135390229009e-07, 1.4416349342636288e-07, 1.4546227465321833e-07, 1.4680929306142988e-07, 1.4820384953851795e-07, 1.496451356725779e-07, 1.511322341479952e-07, 1.5266411936702587e-07, 1.5423965829791257e-07, 1.55857611549717e-07, 1.5751663467353295e-07, 1.5921527968924306e-07, 1.6095199683645537e-07, 1.6272513654774258e-07, 1.6453295164178044e-07, 1.6637359973345378e-07, 1.6824514585748134e-07, 1.7014556530157799e-07, 1.7207274664465686e-07, 1.740244949950588e-07, 1.759985354232749e-07, 1.7799251658313638e-07, 1.8000401451493698e-07, 1.8203053662347306e-07, 1.8406952582351106e-07, 1.8611836484472367e-07, 1.8817438068769515e-07, 1.9023484922215667e-07, 1.9229699991820096e-07, 1.9435802070083098e-07, 1.96415062917813e-07, 1.9846524641046197e-07, 2.00505664676644e-07, 2.025333901149796e-07, 2.0454547933895363e-07, 2.0653897854937167e-07, 2.0851092895339205e-07, 2.1045837221815041e-07, 2.123783559468405e-07, 2.1426793916496894e-07, 2.1612419780440454e-07, 2.179442301727721e-07, 2.1972516239569798e-07, 2.2146415381942084e-07, 2.2315840236130447e-07, 2.248051497958594e-07, 2.2640168696398455e-07, 2.2794535889326988e-07, 2.2943356981738016e-07, 2.3086378808274156e-07, 2.3223355093099672e-07, 2.335404691459707e-07, 2.3478223155419572e-07, 2.359566093683908e-07, 2.3706146036366251e-07, 2.3809473287660088e-07, 2.390544696178835e-07, 2.3993881128946064e-07, 2.4074599999789404e-07, 2.414743824559367e-07, 2.421224129649883e-07, 2.426886561716273e-07, 2.431717895920106e-07, 2.4357060589854057e-07, 2.438840149638246e-07, 2.441110456575964e-07, 2.442508473929228e-07, 2.443026914186879e-07, 2.4426597185602256e-07], "yaxis": "y", "type": "scatter", "uid": "2fd54569-f958-47fc-930f-92cb592cc7db"}, {"legendgroup": "net_influence", "marker": {"color": "rgb(31, 119, 180)", "symbol": "line-ns-open"}, "mode": "markers", "name": "net_influence", "showlegend": false, "x": [486908, 93263, 45873, 8163, 12029, 19793, 5648, 665758, 665758, 41623, 68807, 4888, 58472, 3322, 17156, 3445, 4291, 8163, 2486, 4647, 19758, 2699, 19758, 1910, 1910, 10325, 4616, 1910, 1910, 1910, 4157, 1211, 12020, 92941, 12020, 6740, 38071, 58472, 460, 26077, 7698, 62623, 374, 373, 846, 196, 874, 5275, 373, 4616], "xaxis": "x", "y": ["net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence", "net_influence"], "yaxis": "y2", "type": "scatter", "uid": "9d684f48-89c7-4028-9529-5d7c6582ccc2"}], {"barmode": "overlay", "hovermode": "closest", "legend": {"traceorder": "reversed"}, "xaxis": {"anchor": "y2", "domain": [0.0, 1.0], "zeroline": false}, "yaxis": {"anchor": "free", "domain": [0.35, 1], "position": 0.0}, "yaxis2": {"anchor": "x", "domain": [0, 0.25], "dtick": 1, "showticklabels": false}}, {"showLink": true, "linkText": "Export to plot.ly", "plotlyServerURL": "https://plot.ly"})});</script><script type="text/javascript">window.addEventListener("resize", function(){window._Plotly.Plots.resize(document.getElementById("1cb307ef-a1ab-40ad-8d04-ccee6137cbc0"));});</script>

