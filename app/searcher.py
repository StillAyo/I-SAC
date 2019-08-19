from urllib.request import urlopen
import json
import os
from uritool import *


class Searcher():

    def __init__(self,search_term):
        search_term = search_term

    tool = URItool()
    link = tool.get_link() + "_search?q={}".format(search_term)
    print(link)
    tool.conduct(link)
