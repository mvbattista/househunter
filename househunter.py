import requests
from pprint import pprint
from geopy.distance import great_circle
from geopy.geocoders import Nominatim


def _get_lirr_stations():
    url = 'http://web.mta.info/developers/data/lirr/lirr_gtfs.json'
    raw_data = requests.get(url).json()
    result = {}

    for stop in raw_data['gtfs']['stops']:
        coords = (stop['stop_lat'], stop['stop_lon'])
        result[coords] = stop['stop_name']
        print('{stop_name} - {stop_lat},{stop_lon}'.format(**stop))

    return result


all_stations = _get_lirr_stations()
geolocator = Nominatim(user_agent='househunter')
location = geolocator.geocode('Roosevelt Field Mall, Garden City, NY 11530')
home = (location.latitude, location.longitude)
# home = (40.720721, -73.685203)
within_mile = [{'name': all_stations[c],
                'distance': great_circle(home, c).miles}
               for c in all_stations.keys()
               if great_circle(home, c).miles < 1]
pprint(within_mile)
pprint(home)