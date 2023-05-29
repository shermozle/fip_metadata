#!/usr/bin/python

import requests, json, re, time, urllib, os

host = os.getenv('HOST', '')
port = os.getenv('PORT', '')
user = os.getenv('USER', '')
password = os.getenv('PASSWORD', '')
mount = os.getenv('MOUNT', '')

sleep_timer = 10
while True:
    try:
        clients = requests.get('http://' + user + ':' + password + '@' + host + ':' + port + '/admin/listclients?mount=' + mount)
    except Exception as e:
        print("Error connecting to icecast: " + str(e))
    pattern = re.compile("<Listeners>0</Listeners>")
    searchResult = pattern.search(clients.text)
    if searchResult == None:
        print("We have a listener")
        getUrl = 'https://www.fip.fr/latest/api/graphql?operationName=Now&variables=%7B%22bannerPreset%22%3A%221400x1400%22%2C%22stationId%22%3A7%2C%22previousTrackLimit%22%3A3%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22e3c5dd582094a2c8390fe6a1e60cc73c9b13cba27c10aa969c643915fb9dd7f4%22%7D%7D'
        try:
            response = requests.get(getUrl)
        except Exception as e:
            print("Get url error: " + str(e))
        try:
            data = json.loads(response.text)
            metadata = (data['data']['now']['playing_item']['title'] + ' - ' + data['data']['now']['playing_item']['subtitle']).encode('utf-8')
            print(metadata)
        except Exception as e:
            print("Error:" + str(e))
            print(json.dumps(data))
        try:
            requests.get('http://' + user + ':' + password + '@' + host + ':' + port + '/admin/metadata.xsl?song=' + str(urllib.parse.quote(metadata)) + '&mount=' + urllib.parse.quote(mount) + '&mode=updinfo&charset=UTF-8')
            
        except Exception as e:
            print("Well that didn't work eh: " + str(e))
    else:
        print("Nobody listening")
    time.sleep(sleep_timer)
