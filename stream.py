#/usr/bin/python
# -*- coding: utf-8 -*-
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

#number file names
main_numbers='numbers.txt'
bad_meowers='bad_meow.txt'
tmp_numbers='tmp_numbers.txt'

#Unsubscribe string, case sensitive
unsub_str='Meow, I &lt;3 catfacts'

#Twitter API credentials: Fill them into config.ini, or replace the config.gets with yours.
access_token = config.get('api_credentials', 'access_token')
access_token_secret = config.get('api_credentials', 'access_token_secret')
consumer_key = config.get('api_credentials', 'consumer_key')
consumer_secret = config.get('api_credentials', 'consumer_secret')

#creates the numbers file if it doesnt exist.
open(main_numbers, 'a').close
open(bad_meowers, 'a').close
open(tmp_numbers, 'a').close

def unsubscribe(file_name, unsub_id):
    with open(file_name,"r") as input:
        with open(tmp_numbers,"wb") as output: 
            for line in input:
                if ':'+unsub_id not in line:
                    output.write(line)
    shutil.move(tmp_numbers, file_name)
    open(tmp_numbers, 'a').close
    
    
class StdOutListener(StreamListener):
        
    def on_data(self, data):
        if '"text":' in data:
            tweet = json.loads(data)
            regex = '[^0][\s\(\-.]?([2-9]{1}[0-9]{2})[\s\)\-.]?[\s\(\-.]?([0-9]{3})[\s\)\-.]?[\s\(\-.]?([0-9]{4})[^0-9]'
            number = re.search(regex, tweet['text'])
            if 'Meow' in tweet['text']:
                print("\n"+tweet['text']+"\n")
            if number is not None:
                raw_number = number.group(1)+number.group(2)+number.group(3)
                fh = open(main_numbers, 'r+a')
                if raw_number not in fh.read():
                    print(tweet['text'].encode('utf-8'))
                    print(raw_number)
                    print(raw_number+':'+tweet['user']['id_str'], file=fh)
            #This is the unsub condition, feel free to remove the entire elif condition to disable it
            elif unsub_str in tweet['text'].encode('utf-8'):
                unsubscribe(main_numbers, tweet['user']['id_str'])
                print('REMOVING NUMBER '+tweet['user']['id_str']+' from '+main_numbers)
                unsubscribe(bad_meowers, tweet['user']['id_str'])
                print('REMOVING NUMBER '+tweet['user']['id_str']+' from '+bad_meowers)
                
            elif '@snowden' in tweet['text'].lower():
                fh = open(bad_meowers, 'r+a')
                with open(main_numbers,"r") as input:
                    for line in input:
                        if ':'+tweet['user']['id_str'] in line:
                            if line not in fh.read():
                                print(line, file=fh, end="")              

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['my number is', 'her number is', 'his number is', 'call', 'text', '@snowden Meow'])
