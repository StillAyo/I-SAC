from pymisp import ExpandedPyMISP
import json
import requests

class mispAPI():
    def __init__(self):
        pass

    # def get_credentials(self):
    #     config = configparser.ConfigParser()
    #     section = "misp"
    #
    #     config.read("config.cfg")
    #     url = config.get(section, 'url')
    #     key = config.get(section, 'key')
    #     verify = config.get(section, 'verify_cert')
    #
    #     credentials={
    #         "url":url,
    #         "key":key,
    #         "verify":verify
    #     }
    #     return credentials

    def client_init(self):
        # config = configparser.ConfigParser()
        # section = "misp"
        #
        # config.read("config.cfg")
        # url = config.get(section, 'url')
        # key = config.get(section, 'key')
        # verify = config.get(section, 'verify_cert')


        url = 'https://localhost:8443'
        key = 'mido1GDovbeloNmqv3gXEo1F9AtA8arKbPRLQDAR'
        verify = False

        return ExpandedPyMISP(url, key, verify)

    # def get_events(self, misp_client):
    #     #events_id=[13,14,15,16,17,18,19,20,22,27,32,34]
    #     events_id = [15, 29, 38]
    #
    #     tempHold = []
    #     for x in events_id:
    #         event = misp_client.get_event(x)
    #         try:
    #             if event['errors'][0] == 404:
    #                 print("Error, event wth id {} not available".format(x))
    #         except KeyError:
    #             tempHold.append(event)

    def get_events(self):
        # events_id=[13,14,15,16,17,18,19,20,22,27,32,34]
        headers = {
            'Authorization': 'mido1GDovbeloNmqv3gXEo1F9AtA8arKbPRLQDAR',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        response = requests.get('https://localhost:8443/events/index', headers=headers, verify=False)

        response_json =response.json()
        #print(json.dumps(response_json, indent=4))
        # events_id = [15, 29, 38, ]
        #
        # tempHold = []
        # for x in events_id:
        #     event = misp_client.get_event(x)
        #     try:
        #         if event['errors'][0] == 404:
        #             print("Error, event wth id {} not available".format(x))
        #     except KeyError:
        #         tempHold.append(event)
        return response_json
       # tempFeed.append(event)
        #return event
        #return tempHold