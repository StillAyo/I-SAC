import resilient
import configparser

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
        list_of_ids=[2120,2121]
        #incident_id = 2120
        temp = []
        for incident_id in list_of_ids:
            url = "/incidents/{}?handle_format=names".format(incident_id)
            response = client.get(url)
            assert response
            temp.append(response)

        return temp