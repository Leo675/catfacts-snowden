#/usr/bin/python

from __future__ import print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from ConfigParser import SafeConfigParser
import json
import re
import shutil

config = SafeConfigParser()
config.read('config.ini')

#Unsubscribe string, case sensitive
unsub_str='@Snowden Meow, I <3 catfacts'

#Twitter API credentials: Fill them into config.ini, or replace the config.gets with yours.
access_token = config.get('api_credentials', 'access_token')
access_token_secret = config.get('api_credentials', 'access_token_secret')
consumer_key = config.get('api_credentials', 'consumer_key')
consumer_secret = config.get('api_credentials', 'consumer_secret')

#creates the numbers file if it doesnt exist.
open('numbers.txt', 'a').close
open('user_log.txt', 'a').close

class StdOutListener(StreamListener):
    def on_data(self, data):
        if '"text":' in data:
            tweet = json.loads(data)
            regex = '[^0][\s\(\-.]?([2-9]{1}[0-9]{2})[\s\)\-.]?[\s\(\-.]?([0-9]{3})[\s\)\-.]?[\s\(\-.]?([0-9]{4})[^0-9]'
            number = re.search(regex, tweet['text'])
            if number is not None:
                raw_number = number.group(1)+number.group(2)+number.group(3)
                fh = open('numbers.txt', 'r+a')
                if raw_number not in fh.read():
                    print(tweet['text'].encode('utf-8'))
                    print(raw_number)
                    print(raw_number+':'+tweet['user']['id_str'], file=fh)
            #This is the unsub condition, feel free to remove the entire elif condition to disable it
            elif unsub_str in tweet['text']:
                with open("numbers.txt","r") as input:
                    with open("tmp_numbers.txt","wb") as output: 
                        for line in input:
                            if tweet['user']['id_str'] not in line:
                                output.write(line)
                shutil.move('tmp_numbers.txt', 'numbers.txt')
            
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['my number is', 'her number is', 'his number is', 'call me', 'text me', '@snowden Meow, I <3 catfacts'])
