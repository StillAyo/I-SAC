import requests, json, os
from elasticsearch import Elasticsearch


class Searching:
    def __init__(self,search_term):
        self.search_term = search_term

    def find_results(self):

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
        try:
            query = es.search(index='key_feeds', body={
                'query': {
                    'multi_match': {
                        'query': self.search_term,
                        'fields': ["category", "eventName", "id", "orgName", "tlp"]
                    }
                }
            })
        except:
            print(self.search_term['category'])
            query = es.search(index='key_feeds', body={
                'query': {
                    'bool':{
                        'must':[
                            {
                                'terms': {
                                    'category': self.search_term['category'],

                                }
                            },
                            {
                                'terms':{
                                    'orgName': self.search_term['orgName']
                                }
                            },
                            {
                                'terms': {
                                    'tlp': self.search_term['tlp']
                                }
                            }
                        ]
                    }
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


#print(res.content)


# with open("keyfeed.json", "r") as read_file:
#     events=json.load(read_file)
#
# i=1
#for elem in events['data']:
#    print(json.dumps(elem, indent=4))
#    res=es.index(index='key_feeds',doc_type='events',id=i,body=elem)
#    i=i+1
   # print(res['created'])
#res=es.get(index='key_feeds',doc_type='events',id=3)
#res2 = es.search(index='key_feeds',body={'query':{'match':{'orgName':'GSMA'}}})


#print(res3['hits']['hits']['_source'])


#print(json.dumps(res, indent=4))
#print(json.dumps(res2['hits']['hits'], indent=4))