import json
import random
import math
from tweet_fighter import TweetFighter

class ControlGeneratorAPI:
    kwl1 = None
    kwl2 = None

    def __init__(self, kwl1, kwl2):
        self.kwl1 = kwl1
        self.kwl2 = kwl2

    def generate_attack_sequences(self):
        partitioned_kwl1 = self._partition_tweets(self.kwl1)
        partitioned_kwl2 = self._partition_tweets(self.kwl2)
        #partitioned_kwln is now a list of three tweet lists
        #one for each round
        sentiments_kwl1 = [self._find_net_sentiment(kwl) for kwl in partitioned_kwl1]
        sentiments_kwl2 = [self._find_net_sentiment(kwl) for kwl in partitioned_kwl2]
        #sentiments_kwln is now a list of three sentiment counts
        #one for each round 
        proportions = []
        for i in range(3):
            proportions.append(self._find_proportions(sentiments_kwl1[i], sentiments_kwl2[i]))
        #proportions is now a list of three proportion lists [p1, 1-p1]
        attack_sequences = [self._randomize_weighted_order(p, 10) for p in proportions]
        return attack_sequences

    def _partition_tweets(self, list_of_tweets):
        #tweets are in reverse chronological order, reverse that
        list_of_tweets = list_of_tweets[::-1]
        list1 = list_of_tweets[0:len(list_of_tweets)/3]
        list2 = list_of_tweets[len(list_of_tweets)/3:2*len(list_of_tweets)/3]
        list3 = list_of_tweets[2*len(list_of_tweets)/3:3*len(list_of_tweets)/3]
        return [list1, list2, list3] 
    
    def _find_net_sentiment(self, list_of_tweets):
        s_net_iment = 0
        for tweet in list_of_tweets:
            polarity = int(tweet["polarity"])
            s_net_iment += -1 if (polarity == 0) else 0 if (polarity == 2) else 1
        return s_net_iment

    def _find_proportions(self, s_net_iment1, s_net_iment2):
        total_sentiment = 0
        if s_net_iment1 < 0 and s_net_iment2 >= 0:
            return [0,1]
        elif s_net_iment1 >= 0 and s_net_iment2 < 0:
            return [1,0]
        elif s_net_iment1 > 0 and s_net_iment2 > 0:
            total_sentiment = s_net_iment1 + s_net_iment2 + 0.0
            return [s_net_iment1/total_sentiment, s_net_iment2/total_sentiment]
        elif s_net_iment1 < 0 and s_net_iment2 < 0:
            total_sentiment = s_net_iment1 + s_net_iment2 + 0.0
            return [s_net_iment2/total_sentiment, s_net_iment1/total_sentiment]
        else:
            return [0.5, 0.5] 
    
    def _randomize_weighted_order(self, proportions, num):
        attack_order = []
        data_list = ['1'] * int(math.floor(100 * proportions[0]))
        data_list += ['2'] * int(math.floor(100 * proportions[1]))
        for i in range(num):
            attack_order.append(random.choice(data_list))
        return attack_order       

tweet_fighter = TweetFighter('F6krcMh2bSdFEWiwCO5BFoNnO', 'myQxPYEA3MHEbl3S7CfmZqg9kuMrISYeGJsmYToRK6LSKiejNP', 'levi@roxsoftware.com')
results = tweet_fighter.tweet_fight("Cubs", "Mets")
generator = ControlGeneratorAPI(results[0], results[1])
print generator.generate_attack_sequences()
