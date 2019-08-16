import resilient
import configparser
import json

class resilientAPI():
    def __init__(self):
        pass

    def client_connection(self):
        config = configparser.ConfigParser()
        section = "resilient"

        config.read("config.cfg")
        host = config.get(section, 'host')
        port = config.get(section, 'port')
        email = config.get(section, 'email')
        password = config.get(section, 'password')
        org = config.get(section, 'org')
        url = "https://{0}:{1}".format(host, port or 443)
        client = resilient.SimpleClient(org_name=org,
                                        base_url=url,
                                        verify=False)

        userinfo = client.connect(email, password)
        assert userinfo
        print("working")
        return client

    def fetch_incident(self, client):
        list_of_ids=[2120,2121,2125,2127]
        #incident_id = 2120
        temp = []
        for incident_id in list_of_ids:
            url2 = "/incidents/{}?handle_format=names".format(incident_id)
            response = client.get(url2)
            print(json.dumps(response, indent=4))
            assert response
            temp.append(response)

        return temp

# new_incident={
#     "name": "Attempted take down on my O2 mobile app",
#     "description": "Unknown user from poland attempted to change core configuration settings relating to how plans are displayed to customers  ",
#     "severity_code": "Low",
#     "country": "United Kingdom",
#     "org_handle": "O2",
#     "org_id": 200,
#     "reporter": "Ayo",
#     "properties": {
#         "gsma_region": ["Europe"],
#         "technology_impacted": ["Applications"],
#         "network_location": ["Home network"],
#         "contact_email": "ayooluokun@outlook.com",
#         "countermeasures":"Identified entry point and resolved"
#     },
#     "incident_type_ids":["Information gathering"],
#     "discovered_date":1565953160000
# }
