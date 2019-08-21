import xlrd
import json
from collections import OrderedDict

class displayHighRisk:
    def __init__(self):
        pass

    def retrieveData(self):
        res = requests.get('http://localhost:9200')
        es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        # #search specific field
        # res3 = es.search(index='key_feeds', body={
        #     'query': {
        #         'match_phrase': {
        #             "orgName": self.search_term
        #         }
        #     }
        # })

        query = es.search(index='high_risk_ranges', body={
            'query': {
                'match_all': {}
            }
        })
        results = {}
        temp = []

        for hit in query['hits']['hits']:
            # print(hit['_source']
            temp.append(hit['_source'])

        results['data'] = temp
        print(results)
        return results

