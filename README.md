# Improve Customer Experience through Mining Social Media

## Why?

People flock to social media(Twitter, Facebook, LinkedIn, Google+, etc) for many different reasons. Thanks to the development of mobile technologies, people can communicate with their friends and families, share opinions and ideas about their experience, and discuss significant occurring events and activities. 


Mining those data (posts,tweets, shares, etc) that related to customer experience of services from FedEx and our competitors empowers us to quickly resolve our current customer issues and offer in-time unique personalized marketing experiences for potential new customers:

* Customers define quality, which requires us to listen to the Vice of Customer(VOC) and to do right things automatically and in-timely when we know what our customers want and expect. Through mining the social media data, we can learn customer concerns and response quickly and appropriately to resolve the issues. It is a critical way to give customers a sense of worth and importance and keep strong customer loyalty.

* Identifying users who bad service experience from our competitors and recognizing their issues, we can provide personalized/targeted marketing and advertising opportunities that can address their concerns. 


## How?

There are two major steps need to do:

* Retrieve data - Major social media platforms, like Twitter, Facebook, LinkedIn, provide developer API's which can be used to query historical data as well as streaming data from their platform. Most of the queried data are in JSON format, which is easy to be stored and parsed.
* Analyze data - Big Data platform, like Hadoop, Spark and NoSQL, provide advanced toolkits and systems to process and analyze the social media data. 


### Start with Twitter

We start with Twitter to explore opportunities of applying existing technologies and platforms to mining social media data.

Twiter can be described as a real-time, highly social micro-blogging service that allows users to post short status updates, called _tweets_, that posted on timelines. Tweets many include one or more entities in 140 characters of content and reference to one or more places that map to locations in the real world. 

From the [Twitter Statistics](http://www.statisticbrain.com/twitter-statistics/), Twitter has over 695 million registered users and over 342 million of them are active users.



### Available API from Twitter

Twitter provides clean and well-documented API and rich developer tools, that can be used to retrieve data:


* [REST Search API](https://dev.twitter.com/rest/public/search)
   * Allow queries against recent or popular Tweets that published in the past 7 days.
   * Focus on relevance and not completeness. This means that some Tweets and users may be missing from search results.
   * **[API Rate Limits](https://dev.twitter.com/rest/public/rate-limits)**:
      *   User Auth - **180 Requests per 15 minutes window and 100 tweets per request.** The grand total limit is 18,000 tweets/15 mins, that is, if you download 18K tweets before 15 mins, you won’t be able to get any more results until your 15 min. window expires and you search again.
      *   Application Auth - **450 Requests per 15 minutes window and 100 tweets per request.**
* [Streaming API](https://dev.twitter.com/streaming/overview)
   * Access to Tweet data real-time (low latency) but only get Tweets from the point of a query placed (go forward in time)
   * Get the tweet as long as defined event triggered
   * **[API Rate Limits](https://dev.twitter.com/streaming/overview/connecting)** - Twitter does not make public the number of connection attempts which will cause a rate limiting to occur, but there is some tolerance for testing and development.
* [Gnip](http://support.gnip.com/apis/) 
   * Twitter’s enterprise API platform that provides commercial-grade access to the real-time and historical Twitter data as well as analytic functions to generate insights from the retrieved data.

### Available Libraries for Analysis

* Open Source Natural Language Processing (NLP) libraries:
	* Natural Language Toolkit (NLTK): a Python library that provides modules for processing text, classifying, tokenizing, stemming, tagging, parsing, and more.
	* MALLET: a Java package that provides Latent Dirichlet Allocation, document classification, clustering, topic modeling, information extraction, and more. 
	* Apache OpenNLP: a machine learning toolkit that provides tokenizers, sentence segmentation, part-of-speech tagging, named entity extraction, chunking, parsing, coreference resolution, and more.
	* Stanford NLP: a suite of NLP tools that provide part-of-speech tagging, the named entity recognizer, coreference resolution system, sentiment analysis, and more.



