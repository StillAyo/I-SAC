from urllib.request import urlopen
import json
import os
from app.helpers.uritool import *


class Searcher():
    def __init__(self,search_term):
        self.search_term = search_term

    def do(self):
        tool = URItool()
        link = tool.get_link() + "_search?q={}".format(self.search_term)
        print(link)
        tool.conduct(link)
