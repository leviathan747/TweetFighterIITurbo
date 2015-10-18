from twython import Twython
from sentiment140 import Sentiment140API

CONSUMER_KEY = "IMhoOLI5hEv2UU1xvskOFMiPy"
CONSUMER_SECRET = "4QcaLsu04V3ZvaVDtaTbmUqYkKI0B9VuBCoiY1HjgNNuEh54kB"
ACCESS_KEY = "3982575449-b2oc18sUhI5emOThl2dxqv3whBPzNkbRyMeIGFy"
ACCESS_SECRET = "XngnYbt98UR5eK0B7y1TRYFebTdkoM8HvlLqMExu2E7hE"
SENT_APP_ID = "levi@roxsoftware.com"

class TweetFighter:

    APP_KEY = None
    APP_SECRET = None
    SENT_APP_ID = None
    twitter_api = None
    
    def __init__(self, tw_appid, tw_appsecret, sent_appid):
        self.APP_KEY = tw_appid
        self.APP_SECRET = tw_appsecret
        self.SENT_APP_ID = sent_appid
        self.init_twython()

    #------------------------------------------------------------------------#
    #   get twython instance                                                 #
    #------------------------------------------------------------------------#
    def init_twython(self):
        # check
        if ( self.APP_KEY == None or self.APP_SECRET == None ):
            print 'error in init_twython'
            return

        # get an access token
        self.twitter_api = Twython(self.APP_KEY, self.APP_SECRET, oauth_version=2)
        ACCESS_TOKEN = self.twitter_api.obtain_access_token()

        # get a new twitter handle with the access token
        self.twitter_api = Twython(self.APP_KEY, access_token=ACCESS_TOKEN)

    #------------------------------------------------------------------------#
    #   get tweets                                                           #
    #------------------------------------------------------------------------#
    def get_tweets(self, kw, max_attempts, target):

        if ( kw == None or self.twitter_api == None ):
            print 'error in get_tweets'
            return None

        tweets                          =   []
        MAX_ATTEMPTS                    =   max_attempts
        COUNT_OF_TWEETS_TO_BE_FETCHED   =   target
        next_max_id                     =   0

        for i in range(0, MAX_ATTEMPTS):

            if ( COUNT_OF_TWEETS_TO_BE_FETCHED < len(tweets) ):
                break       # we got our tweet quota

            #----------------------------------------------------------------#
            # STEP 1: Query Twitter
            # STEP 2: Save the returned tweets
            # STEP 3: Get the next max_id
            #----------------------------------------------------------------#

            # STEP 1: Query Twitter
            if(0 == i):
                # Query twitter for data. 
                results    = self.twitter_api.search(q=kw,count='100')
            else:
                # After the first call we should have max_id from result of previous call. Pass it in query.
                results    = self.twitter_api.search(q=kw,count ='100', include_entities='true',max_id=next_max_id)

            # STEP 2: Save the returned tweets
            for result in results['statuses']:
                result['query'] = kw
                tweets.append(result)

            # STEP 3: Get the next max_id
            try:
                # Parse the data returned to get max_id to be passed in consequent call.
                next_results_url_params    = results['search_metadata']['next_results']
                next_max_id        = next_results_url_params.split('max_id=')[1].split('&')[0]
            except:
                # No more next pages
                break

        print 'returning tweets'
        return tweets


    #------------------------------------------------------------------------#
    #   analyze sentiment                                                    #
    #------------------------------------------------------------------------#
    def analyze_tweets(self, tweets):
        if ( self.SENT_APP_ID == None or tweets == None ):
            print "error in analyze_tweets"
            return None
        sent140 = Sentiment140API(appid=self.SENT_APP_ID)
        analyzed_tweets = sent140.bulk_classify_json(tweets)
        print 'returning analyzed tweets'
        return analyzed_tweets

    #------------------------------------------------------------------------#
    #   tweet fight                                                          #
    #------------------------------------------------------------------------#
    def tweet_fight(self, kw1, kw2):

        # get tweets for first keyword
        tweets1 = self.analyze_tweets( self.get_tweets(kw1, 10, 5000) )

        # get tweets for second keyword
        tweets2 = self.analyze_tweets( self.get_tweets(kw2, 10, 5000) )

        print 'done'
        print 'tweets1 len: ', len(tweets1)
        print 'tweets2 len: ', len(tweets2)
            
        # return concatenation of the two
        return [tweets1, tweets2]

if __name__ == '__main__':
    tweet_fighter = TweetFighter(CONSUMER_KEY, CONSUMER_SECRET, SENT_APP_ID)
    results = tweet_fighter.tweet_fight('cubs', 'mets')
