from urllib.request import urlopen
import json
import os

class URItool:

    URIlink = "http://localhost:9200/expevents1/"

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
        filepath = os.path.join('/usr/share/logstash/bin', 'searchresults.log')

        with open(filepath, 'a')as f:
            f.truncate(0)
            f.write(json.dumps(events))

