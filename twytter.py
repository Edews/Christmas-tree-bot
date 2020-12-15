import RPi.GPIO as GPIO
import time
import tweepy
from threading import Thread
from threading import Timer

# coding=utf-8

#here is where you need to add your own keys from the Twitter API
auth = tweepy.OAuthHandler('API key', 'secret')
auth.set_access_token('Access token', 'secret')
api = tweepy.API(auth)

channel = 20

def turn_off():
    GPIO.output(channel,GPIO.LOW)
    GPIO.cleanup()

def newTimer():
    global t
    t = Timer(3,turn_off)
newTimer()

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            print(status.author.screen_name + " just used the hashtag #christmas")
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(channel, GPIO.OUT)

            GPIO.output(channel,GPIO.HIGH)
            t.cancel()
            newTimer()
            t.start()

        except KeyboardInterrupt:
            t.cancel()
            GPIO.cleanup()

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

#here is where the filter actually starts. You can change it to either a simple
#string for keywords, or use follow= tag followed by a Twitter ID.
myStream.filter(track=['#christmas'])
