import requests

class alienVault():
   # url = 'https://otx.alienvault.com/api/v1/pulses/5d120d47d09d67b4d8dc5241'

    def __init__(self, headers):
        self.headers = headers

    def fetch_feed(self):
        urls = ['https://otx.alienvault.com/api/v1/pulses/5d120d47d09d67b4d8dc5241',
                'https://otx.alienvault.com/api/v1/pulses/5d1a082d99fb2fc0010e1294']
        temp = []
        for url in urls:
            response = requests.get(url, headers=self.headers)
            response_json = response.json()
            temp.append(response_json)
       # print(json.dumps(response_json, indent=4))
        #return response_json
        return temp

    def send_feed(self,feed):
        with open('eventfeeds.json', 'a+') as write_file:
            json.dump(feed, write_file)
            write_file.write("\n")