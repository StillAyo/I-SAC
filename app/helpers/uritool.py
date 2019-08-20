from urllib.request import urlopen
import json
import os

class URItool:

    URIlink = "http://localhost:9200/test2/"

    def __init__(self):
        pass

    def get_link(self):
        return self.URIlink

    def conduct(self,link):
        print(link)
        f = urlopen(link)
        elastic_event_json = f.read()
        elastic_event_parsed = json.loads(elastic_event_json)
        event_json = elastic_event_parsed['hits']['hits']
        number_events = len(event_json)

        events = {"data": []}
        for i in range(0, number_events):
            try:
                events["data"].append(event_json[i]['_source']['data'])
            except:
                del event_json[i]
        filepath = os.path.join('/home/vagrant/I-SAC', 'results.json')
        if not os.path.exists('/home/vagrant/I-SAC'):
            os.makedirs('/home/vagrant/I-SAC')

        with open(filepath, 'a')as f:
        # with open('results.json', 'a')as f:
            f.truncate(0)
            f.write(json.dumps(events))

