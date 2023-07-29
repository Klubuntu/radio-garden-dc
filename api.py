import requests
from urllib.request import urlopen


def fetch_station_id_url(url):
    if url:
       station_id = url.split("/")[5]
       return station_id
    else:
       return "Invalid Radio Garden URL"

def fetch_radio_stations(query):
    url = f'https://radio.garden/api/search?q={query}'
    try:
        response = requests.get(url)
        response.raise_for_status()

        # If the request is successful, the response content will be in JSON format.
        data = response.json()
        return data.get('hits')
    except requests.exceptions.RequestException as e:
        print("Error occurred: {e}")
        return None

def get_stations_by_region(data, region: str):
    result = []
    if 'hits' in data:
        for station in data['hits']:
            if 'code' in station.get('_source', {}):
                if station['_source']['code'] == region.upper():
                    result.append(station['_source'])
    return result

def get_first_valid_url(response):
    if response[0].get('_source'):
        for x in response:
            url = x.get('_source').get("url")
            if "/listen" in url:
                return x
    else:
        for x in response:
            url = x.get("url")
            if "/listen" in url:
                return x

def get_first_station(data):
    if data:
        try:
            response = data.get('hits')
        except:
            print("[ERROR] Invalid response from Radio Garden API")
            return None
        tmp = response[0].get('_source')["type"]
        if tmp == "place":
            print(f"[DEBUG] Place not supported")
            print("[DEBUG] Searching for another URL")
            response2 = get_first_valid_url(response)
            print("[DEBUG] Found another URL")
        else:
            response2 = response[0]
        try:
            result = {
                'id': response2.get('_id'),
                'name': response2.get('_source')["title"],
                'region': response2.get('_source')["code"],
                'url': response2.get('_source')["url"],
            }
        except:
            return "Station not found"
        return result
    else:
        return None

def get_first_station_region(data):
    if data:
        try:
            response = data
        except:
            print("[ERROR] Invalid response from Radio Garden API")
            return None

        tmp = data[0].get("type")
        if tmp == "place":
            print("[DEBUG] Place not supported")
            print("[DEBUG] Searching for another URL")
            response2 = get_first_valid_url(response)
            if response2:
                print("[DEBUG] Found another URL")
                print(response2)
            else:
                print("[DEBUG] No valid URLs found in the response.")
                return None
        else:
            response2 = response[0]

        try:
            result = {
                'name': response2.get("title"),
                'region': response2.get("code"),
                'url': response2.get("url"),
            }
        except:
            return "Station not found"
        return result

def get_channel_id(data):
    if data:
        return data.get("url").split("/")[3]
    else:
        return None       


def get_channel_station(chanid):
    if chanid:
        response = requests.get(f'https://radio.garden/api/ara/content/channel/{chanid}')
        response.raise_for_status()
        result = response.json().get('data')
        export = {
            "type": result.get('type'),
            "name": result.get('title'),
            "website": result.get('website'),
            "place": {
                "id": result.get('place').get('id'),
                "name": result.get('place').get('title'),
            },
            "country": {
                "id": result.get('country').get('id'),
                "name": result.get('country').get('title'),
            }
        }
        return export
    else:
        return None

def get_channel_station_broadcast(chanid):
    if chanid:
        url= f'https://radio.garden/api/ara/content/listen/{chanid}/channel.mp3'
        response = urlopen(url)
        result = response.geturl()
        return result
    else:
        return None

def get_channel_station_broadcast_head(chanid):
    if chanid:
        url= f'https://radio.garden/api/ara/content/listen/{chanid}/channel.mp3'
        response = requests.head(url)
        response.raise_for_status() 
        result = response.headers.get('location')
        return result
    else:
        return None  

### TEST MODE ###
# Replace 'search_query' with your desired search query.
# search_query = 'kutx'
# radio_data = fetch_radio_stations(search_query)
# first_elm = get_first_station(radio_data)
# channel_id = get_channel_id(first_elm)
# channel_data = get_channel_station(channel_id)
# broadcast_data = get_channel_station_broadcast_head(channel_id)
# broadcast_test = get_channel_station_broadcast_head("f0BzGx42")
# print(broadcast_test)