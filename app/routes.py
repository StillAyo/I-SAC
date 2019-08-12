from app import app
from pytz import utc
from flask import render_template, redirect, flash, jsonify, request
#from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import pusher
import json
from pymemcache.client import base
import resilient
from app.alienvault import alienVault
from app.resilientConn import resilientAPI
from app.mispConn import mispAPI
from bs4 import BeautifulSoup
import configparser
import requests
import time
import re
import os

pusher_client = pusher.Pusher(
        app_id="837791",
        key="2e0f7cfc70c03aaac02d",
        secret="995ea9e63e923dab3049",
        cluster="eu",
        ssl=True)
global basedir
basedir = os.path.abspath(os.path.dirname(__file__))

scheduler=BackgroundScheduler(timezone=utc)
client = base.Client(('localhost', 11211))

def convertFromEpoch(epoch_time):
    new_time = time.strftime('%Y-%m-%d', time.localtime(epoch_time))
    return new_time

def configs():
    cfgfile = open("config.cfg", 'w')
    Config = configparser.ConfigParser()
    # add the settings to the structure of the file, and lets write it out...
    Config.add_section('misp')
    Config.set('misp', 'url', 'https://localhost:8443')
    Config.set('misp', 'key', 'keyhere')
    Config.set('misp', 'verify_cert', 'False')

    Config.add_section('resilient')
    Config.set('resilient', 'org', 'GSMA')
    Config.set('resilient', 'port', '443')
    Config.set('resilient', 'email', 'ayooluokun@outlook.com')
    Config.set('resilient', 'password', 'pws')
    Config.set('resilient', 'host ', 'gsma.resilientsystems.com')
    Config.write(cfgfile)


""" class to get all the info from the different api's
saves each instance of incident/feed to a file
later reads from that file and extracts the key info to be displayed on the events feed page
"""
class InfoCollector():
    eventFeeds =[]

    def __init__(self):
        pass

    def save_feed(self, feed):
        # list_of_feeds = []
        # for i in feed:
        #     list_of_feeds.append(feed)
       # print(json.dumps(list_of_feeds, indent=4))
        with open('eventfeeds.json', 'w') as write_file:
            json.dump(feed, write_file)
        #  write_file.write(",\n")

    def retrieve_key_info(self):
        with open('eventfeeds.json', 'r') as read_file:
            data = json.load(read_file)

        key_info = []
        #print(data[0])
        for i in data:
            #print(json.dumps(i, indent=4))
            tempFeed = {}

            try:
                # resilient info gathering
                feed_id = i['id']
                # remove html tags from text
                event_name=BeautifulSoup(i['description']).get_text()
                org_name=i['properties']['gsma_member']
                date=i['create_date']
                tlp=i['severity_code']
                category=i['incident_type_ids'][0]
                tempFeed.update({"id": feed_id, 'eventName': event_name, 'orgName': org_name,
                                 'date': self.convertFromEpoch(date), 'tlp': tlp, 'category': category})

                key_info.append(tempFeed)
            except KeyError:
                try:
                    # alien vault info gathering
                    feed_id = i['author']['id']
                    event_name = i['name']
                    org_name = i['author_name']
                    tlp = i['TLP']
                    category = i['industries'][0]
                    date = i['created'][0:10]

                    tempFeed.update({"id": feed_id, 'eventName': event_name, 'orgName': org_name,
                                     'date': date, 'tlp': tlp, 'category': category})
                    key_info.append(tempFeed)
                except KeyError:
                    #misp key info gathering
                   ## attributes = i['Event']['Attribute']
                    feed_id = i['id']
                    event_name = i['info']
                    org_name = i['Orgc']['name']
                    tlp = i['EventTag'][0]['Tag']['name'][4:]
                    try:
                        category = (i['EventTag'][1]['Tag']['name'][30:]).replace('"','')
                    except:
                        category="Null"
                    date = i['date']
                    tempFeed.update({"id": feed_id, 'eventName': event_name, 'orgName': org_name,
                                     'date': date, 'tlp': tlp, 'category': category})
                    key_info.append(tempFeed)
        #print(key_info)
        # testing something#
        # temp={}
        # temp['data'] = key_info
        with open('keyfeed.json', 'w') as write_file:
            json.dump(key_info, write_file)
            # json.dump(temp, write_file)

        # with open('keyfeed.json', 'r') as read_file:
        #     real_info = json.load(read_file)

        # existing_feed_ids = [id['id'] for id in key_info]
        # client.set('ids', existing_feed_ids)
        #return real_info
        return key_info
       # return key_info

    def convertFromEpoch(self, epoch_time):
        new_time = time.strftime('%Y-%m-%d', time.localtime(epoch_time/1000))
        return new_time




def fetch_data_from_api():
    headers = {
        'X-OTX-API-KEY': '4dcb5c735bcbc704ab7c3744df540e5d8caece6089684dcb68feb2c733a1b5d9'
    }
    api_object = InfoCollector()

    otx_object = alienVault(headers)
    otx_feed = otx_object.fetch_feed()

    resilient_object = resilientAPI()
    resilient_feed = resilient_object.fetch_incident(resilient_object.client_connection())

    misp_object = mispAPI()
    misp_feed = misp_object.get_events()


    api_object.save_feed(otx_feed + resilient_feed + misp_feed)
    api_object.retrieve_key_info()

    #print(json.dumps(api_object.retrieve_key_info(), indent=4))
    # pusher_client.trigger('feed_check', 'new-feed', {'data': feed})

def fetch_keyinfo():
    eventFeed = (requests.get("http://127.0.0.1:5000/key_feeds.json")).json()

    #get current list of id from cache. send to function to convert from bytes then ascii then back to list
    existing_feed_ids = convert_from_ascii((client.get('ids')).decode("ascii"))

    print(json.dumps(eventFeed, indent=4))
    print("STORED IN CACHE IS: {}".format(existing_feed_ids))
    print(type(existing_feed_ids))

    #new events
    new_events = [i for i in eventFeed if not (int(i['id']) in existing_feed_ids)]

    print(json.dumps(new_events, indent=4))

    print(len(new_events))

    new_events_ids = [int(li['id']) for li in new_events]

    existing_feed_ids = existing_feed_ids+new_events_ids
    print("NOW STORED IN CACHE AFTER CHECK IS: {}".format(existing_feed_ids))


    pusher_client.trigger('feed_check', 'new-feed', {'data': new_events, 'ids': existing_feed_ids})
    pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
    client.set('ids', existing_feed_ids)


def convert_from_ascii(ascii_list):
    regEx = re.findall(r"[\w]+", ascii_list)
    list_of_ids=list(map(int, regEx))
    return list_of_ids


scheduler.add_job(fetch_data_from_api, 'interval', seconds=40, max_instances=3)
scheduler.add_job(fetch_keyinfo, 'interval', seconds=55, max_instances=3)

scheduler.start()

@app.route('/')
@app.route('/home')


def home():
    return render_template('splashPage.html', title='Welcome')


@app.route('/explore', methods=["POST", "GET"])
def explore():
    if request.method == "POST":
        testing = request.form["searchInput"]
        print(testing)
        return redirect("/explore", code=302)
    else:
        ## misp feed, with data saved in json file
        with open(os.path.join(basedir, 'static', 'data', 'data_file.json')) as read_file:
            data = json.load(read_file)

        # attributes = data['Event']['Attribute']
        # eventFeed=[
        #     {
        #         'idNo': data['Event']['id'],
        #         'eventName': data['Event']['info'],
        #         'orgName': data['Event']['Org']['name'],
        #         'tlp': data['Event']['Tag'][0]['name'],
        #         'category': attributes[0]['category'],
        #         'date': data['Event']['date']
        #     }
        # ]

        headers = {
            'X-OTX-API-KEY': '4dcb5c735bcbc704ab7c3744df540e5d8caece6089684dcb68feb2c733a1b5d9'
        }
        api_object = InfoCollector()

        otx_object = alienVault(headers)
        otx_feed = otx_object.fetch_feed()

        resilient_object = resilientAPI()
        resilient_feed = resilient_object.fetch_incident(resilient_object.client_connection())

        misp_object = mispAPI()
        # misp_client = misp_object.client_init(misp_object.get_credentials())
        #misp_client = misp_object.client_init()
        misp_feed = misp_object.get_events()

        #temp=misp_feed.extend((resilient_feed, otx_feed))

        #api_object.save_feed([otx_feed, resilient_feed, misp_feed])
        api_object.save_feed(otx_feed+resilient_feed+misp_feed)
        feeds = api_object.retrieve_key_info()

        existing_feed_ids = [id['id'] for id in feeds]
        client.set('ids', existing_feed_ids)

        #eventFeed = api_object.retrieve_key_info()
        eventFeed = (requests.get("http://127.0.0.1:5000/key_feeds.json")).json()

        #print(eventFeed)

        # otxFeed=otxApi()
        # eventFeed.append(otxFeed)
        #
        # resilientFeed=getResilientIncident(resilientConnection())
        # eventFeed.append(resilientFeed)

        return render_template('Events.html', title='Welcome', event=eventFeed)



@app.route('/submit')

def submit():
    return render_template('submit.html', title="Submit")


@app.route('/analyse')
def analyse():
    return render_template('analytics.html')


@app.route('/key_feeds.json',  methods=["GET", "POST"])
def get_feeds():
    with open('keyfeed.json', 'r') as read_file:
        feed = json.load(read_file)
    # feed_ids=[]
    # for feed in feeds['data']:
    #     feed_ids.append(feed['id'])
    #
    # print(feed_ids)

    return jsonify(feed)
#scheduler.add_job(get_feeds, 'interval', minutes=1)


