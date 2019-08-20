from urllib.request import urlopen
import json
import os
from uritool import *


class Filterer():

    def __init__(self,filter_terms):
        self.filter_terms = sorted(filter_terms.keys(), key = lambda x:x.lower())

    def do(self):
        tool = URItool()
        link = tool.get_link() + "_search?q="
        for term in self.filter_terms.keys():
            for filter in self.filter_terms[term]:
                link = link + "{}:{} AND ".format(term, filter)

        print(link)
        tool.conduct(link)


tlp
category
id
orgName