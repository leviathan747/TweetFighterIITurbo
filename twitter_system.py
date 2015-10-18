from twython import Twython, TwythonStreamer
from twython import TwythonError
import random
import re

from tweet_fighter import *
from controlgenerator import *


CONSUMER_KEY = "blah0"
CONSUMER_SECRET = "blah1"
ACCESS_KEY = "blah2"
ACCESS_SECRET = "blah3"
SENT_APP_ID = "blah4"

twitter = Twython(CONSUMER_KEY , CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
pattern1 = re.compile(r'.*? (.*?) vs (.*?)\. Thanks!')

tweet_fighter = TweetFighter(CONSUMER_KEY, CONSUMER_SECRET, SENT_APP_ID)
results = []

class MyStreamer(TwythonStreamer):
	def gimme_some():
		print "HEYAAAAAAAAA"

	def on_success(self, data):
		if 'text' in data:
			username = data['user']['screen_name']
			if username != "tweetfight2":
				searchObj = pattern1.search(data['text'])
				if searchObj:
					status = "hey dummy {}  vs {} coming up soon".format(searchObj.group(1), searchObj.group(2))
					results = tweet_fighter.tweet_fight(searchObj.group(1), searchObj.group(2))
					attacks = ControlGeneratorAPI(results[0], results[1])
					print attacks.generate_attack_sequences()
				else:
					status = "hey dummy {}".format(random.random())

				name = "@{0} ".format(username)
				twitter.update_status(status=name+status)

	def on_error(self, status_code, data):
		print (status_code)

if __name__ == '__main__':
	stream = MyStreamer(CONSUMER_KEY , CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
	try:
		stream.user()
	except TwythonError as err:
		print(err)




#twitter.update_status(status="Hello from Python! :)")
