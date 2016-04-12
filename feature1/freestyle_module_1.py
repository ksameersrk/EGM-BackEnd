'''
    04/03/16
    FEATURE 1 (MODULE 1)
    Get src - destination
    Return places
'''


from collections import OrderedDict, namedtuple
from pprint import pprint

import googlemaps
import math
import sys

try:
    import urllib2
except:
    print('Run with python2.7')
    exit()

Coordinates = namedtuple('coordinate', ['lat', 'lng'])

API_KEY = 'AIzaSyCQd3oHe34SNelQzLuT6KSdA3ajCqt-gp8'

URL_dir = 'https://maps.googleapis.com/maps/api/directions/json?origin=__ORIGIN__&destination=__DEST__&key=%s' % API_KEY  # template URL string

URL_geo = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=__LATLNG__&result_type=administrative_area_level_1&key=%s' %API_KEY

gmaps = googlemaps.Client(API_KEY)  # initialize client


def get_points_of_interest(src_coord, dest_coord):
    
    src_coord = Coordinates(*src_coord)
    dest_coord = Coordinates(*dest_coord)
    
    #print(URL_dir.replace('__ORIGIN__', googlemaps.convert.latlng(src_coord)).replace('__DEST__', googlemaps.convert.latlng(dest_coord)))
    
    route_json_result = eval(urllib2.urlopen(URL_dir.replace('__ORIGIN__', googlemaps.convert.latlng(src_coord)).replace('__DEST__', googlemaps.convert.latlng(dest_coord))).read())

    if route_json_result["status"] != "OK":
        return {}
    
    bounds = route_json_result["routes"][0]["bounds"]
    bounds_northeast, bounds_southwest = Coordinates(*OrderedDict(bounds["northeast"]).values()), Coordinates(*OrderedDict(bounds["southwest"]).values())
    center = get_midpoint(bounds_northeast, bounds_southwest)
    radius = get_distance(center, bounds_northeast)
    
    #print(URL_geo.replace('__LATLNG__', googlemaps.convert.latlng(list(center))))
    
    place_bias_json_result = eval(urllib2.urlopen(URL_geo.replace('__LATLNG__', googlemaps.convert.latlng(list(center)))).read())

    if place_bias_json_result['status'] != "OK":
        return {}

    place_bias = place_bias_json_result['results'][0]['address_components'][0]['long_name']

    places_json_result = gmaps.places("tourism, restaurants " + place_bias , location=list(src_coord), radius=radius)

    if places_json_result["status"] != "OK":
        return {}

    results = places_json_result['results']

    for result in results:
        if 'tour' in result['name'].lower() or 'travels' in result['name'].lower(): 
            continue
        try:
            if result['rating'] >= 4.0:
                points_of_interest[result['name']] = [result['place_id'], result['geometry']['location'].values(), result['rating']]
        except: 
            continue    # don't bother with seedy places
    
    #print(points_of_interest)

    return points_of_interest


def get_midpoint(coord_1, coord_2):
    d_lng =  math.radians(coord_2.lng - coord_1.lng)

    lat_1, lng_1 = map(math.radians, coord_1)
    lat_2 = math.radians(coord_2.lat)

    x = math.cos(lat_2) * math.cos(d_lng)
    y = math.cos(lat_2) * math.sin(d_lng)
    
    lat_3 = math.atan2(math.sin(lat_1) + math.sin(lat_2), math.sqrt((math.cos(lat_1) + x) * (math.cos(lat_1) + x) + y**2))
    lng_3 = lng_1 + math.atan2(y, math.cos(lat_1) + x)

    #print(list(map(math.degrees, [lat_3, lng_3])))

    return Coordinates(*map(math.degrees, [lat_3, lng_3]))


def get_distance(coord_1, coord_2):
    t_coord_1 = Coordinates(*map(math.radians, coord_1))
    t_coord_2 = Coordinates(*map(math.radians, coord_2))

    d_lat, d_lng = (t_coord_2.lat - t_coord_1.lat), (t_coord_2.lng - t_coord_1.lng) 
    temp = math.sin(d_lat / 2)**2 + math.cos(t_coord_1.lat) * math.cos(t_coord_2.lat) * math.sin(d_lng / 2)**2

    return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))


if __name__=="__main__":
    user_source = OrderedDict({u'lat': 12.9715987, u'lng': 77.5945627})
    user_dest = {u'lat': 12.2958104, u'lng': 76.6393805}
    
    pprint(get_points_of_interest(user_source.values(), user_dest.values()))






