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
        sent_proportions = []
        combined_kwl = []
        for i in range(3):
            sent_proportions.append(self._find_sent_proportions(sentiments_kwl1[i], sentiments_kwl2[i]))
            combined_kwl.append(partitioned_kwl1[i] + partitioned_kwl2[i])
        #sent_proportions is now a list of three proportion lists [p1, 1-p1]
        #combined_kwl is a list of three lists, where each list the combined tweets for
        #that specific window
        interact_proportions = []
        attack_sequences = []
        for i in range(3):
            interact_proportions.append(self._find_interaction_proportions(combined_kwl[i]))
        for i in range(3):
            attack_sequences.append(self._generate_attack_sequence(sent_proportions[i],interact_proportions[i], 10))
        return attack_sequences

    def _get_attacker(self, order_list):
        return random.choice(order_list)

    def _get_attack(self, attack_list,classes):
        #return a random attack by choosing an attack class from the
        #weighted attack list, and then choosing randomly from that
        #class
        return random.choice(classes[random.choice(attack_list)])

    def _generate_attack_sequence(self, sent_proportions, interact_proportions, num):
        attack_sequence = []
        #generate the weighted list to choice the order from
        order_list = ['a'] * int(math.floor(100 * sent_proportions[0]))
        order_list += ['b'] * int(math.floor(100 * sent_proportions[1]))
        
        #the different kinds of attacks
        attack0 = '00' 
        attack1 = '01'
        attack2 = '02'
        attack3 = '03'
        attack4 = '04'
        attack5 = '05'
        attack6 = '06'
        attack7 = '07'
        attack8 = '08'
        attack9 = '09'
        attack10 = '10'
        attack11 = '11'

        #the different classes of attacks
        class0 = [attack4, attack5]
        class1 = [attack0, attack2]
        class2 = [attack1, attack3, attack6]
        class3 = [attack9, attack10]
        class4 = [attack8]
        class5 = [attack7]
        class6 = [attack11]
        classes = [class0, class1, class2, class3, class4, class5, class6]

        attack_list = [0] * int(math.floor(100*interact_proportions[0]))
        attack_list += [1] * int(math.floor(100*interact_proportions[1]))
        attack_list += [2] * int(math.floor(100*interact_proportions[2]))
        attack_list += [3] * int(math.floor(100*interact_proportions[3]))
        attack_list += [4] * int(math.floor(100*interact_proportions[4]))
        attack_list += [5] * int(math.floor(100*interact_proportions[5]))
        attack_list += [6] * int(math.floor(100*interact_proportions[6]))

        for i in range(num):
            attack_sequence.append(self._get_attacker(order_list))
            attack_sequence.append(self._get_attack(attack_list, classes))
        return attack_sequence       
    
    def _partition_tweets(self, list_of_tweets):
        #tweets are in reverse chronological order, reverse that
        list_of_tweets = list_of_tweets[::-1]
        list1 = list_of_tweets[0:len(list_of_tweets)/3]
        list2 = list_of_tweets[len(list_of_tweets)/3:2*len(list_of_tweets)/3]
        list3 = list_of_tweets[2*len(list_of_tweets)/3:3*len(list_of_tweets)/3]
        return [list1, list2, list3] 
   
    def _find_interaction_proportions(self, list_of_tweets):
        interactions_list = []
        for tweet in list_of_tweets:
            favorite = int(tweet["favorite_count"])
            retweet = int(tweet["retweet_count"])
            interaction = favorite + retweet
            interactions_list.append(retweet)
        total_interactions = sum(interactions_list)
        total_interactions += 0.0
        proportions = [curr/total_interactions for curr in interactions_list]
        proportions = self._bucketize_interaction_proportions(proportions)
        return proportions

    def _find_net_sentiment(self, list_of_tweets):
        s_net_iment = 0
        for tweet in list_of_tweets:
            polarity = int(tweet["polarity"])
            s_net_iment += -1 if (polarity == 0) else 0 if (polarity == 2) else 1
        return s_net_iment

    def _find_sent_proportions(self, s_net_iment1, s_net_iment2):
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
   
    def _bucketize_interaction_proportions(self, interaction_proportions):
        bucket0 = bucket1 = bucket2 = bucket3 = bucket4 = bucket5 = bucket6 = 0
        for proportion in interaction_proportions:
            if 0 <= proportion < .14:
                bucket0 += 1
            elif .14 <= proportion < .28:
                bucket1 += 1
            elif .28 <= proportion < .43:
                bucket2 += 1
            elif .43 <= proportion < .57:
                bucket3 += 1
            elif .57 <= proportion < .71:
                bucket4 += 1
            elif .71 <= proportion < .87:
                bucket5 += 1
            elif .87 <= proportion:
                bucket6 += 1
        buckets = [bucket0, bucket1, bucket2, bucket3, bucket4, bucket5, bucket6]
        total_buckets = sum(buckets)
        total_buckets += 0.0
        bucketized_proportions = [bucket/total_buckets for bucket in buckets]
        return bucketized_proportions
            


