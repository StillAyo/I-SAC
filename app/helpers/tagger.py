from attackcti import attack_client
from textblob import TextBlob
from pandas import *
from pandas.io.json import json_normalize
import json
text="SS7"

class Tagger():

    def __init__(self,event_text):
        self.event_text = event_text

    def do(self):
        phrases = TextBlob(self.event_text).noun_phrases
        tagging = []
        lift = attack_client()
        all_mobile = lift.get_mobile()

        for t in all_mobile['techniques']:
            for phrase in phrases:
                if phrase in t['name'].lower():
                    tagging = ((t['name'],t['description']))

        return tagging
