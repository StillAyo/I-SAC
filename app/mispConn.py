from pymisp import ExpandedPyMISP
import json
import requests

class mispAPI():
    def __init__(self):
        pass


    def client_init(self):



        url = 'https://10.20.40.1:8443'
        key = 'lByYShZqpJUFZXumBWPqmpD5Ii2QKQxns82iULG2'
        verify = False

        return ExpandedPyMISP(url, key, verify)



    def get_events(self):
        # events_id=[13,14,15,16,17,18,19,20,22,27,32,34]
        headers = {
            'Authorization': 'lByYShZqpJUFZXumBWPqmpD5Ii2QKQxns82iULG2',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        response = requests.get('https://10.20.40.1:8443/events/index', headers=headers, verify=False)

        response_json =response.json()

        return response_json
