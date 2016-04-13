'''
    04/03/16
    FEATURE 1
    
    get_places_of_interest():
        Get src - destination
        Return places
        
    get_best_route():
        Get src - destination, waypoints
        Return optimized route
    
'''

from collections import OrderedDict, namedtuple
from pprint import pprint

import copy
import googlemaps
import math
import sys

try:
    import urllib2
except:
    print('Run with python2.7')
    exit()

Coordinates = namedtuple('Coordinate', ['lat', 'lng']) # initialise a pesudo class for handling latlng coordinates

''' Defining public variables '''
API_KEY = 'AIzaSyCQd3oHe34SNelQzLuT6KSdA3ajCqt-gp8' # API key - use it, don't abuse it
URL_dir = 'https://maps.googleapis.com/maps/api/directions/json?origin=__SRC__&destination=__DEST__&key=%s' % API_KEY  # template URL string for quering the directions API
URL_rev_geo = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=__LATLNG__&result_type=administrative_area_level_1&key=%s' %API_KEY  # template URL string for quering the geocoding API
URL_geo = 'https://maps.googleapis.com/maps/api/geocode/json?address=__ADD__&key=%s' %API_KEY
gmaps = googlemaps.Client(API_KEY)  # initialize client


def get_geocoded_address(address):
	geocoded_json_result = eval(urllib2.urlopen(URL_geo.replace('__ADD__', address.replace(" ", "+")).read()))

	if geocoded_json_result['status'] == "ZERO_RESULTS":
		raise Exception("No valid latlng coordinates for given address")	
	
	elif geocoded_json_result['status'] != "OK":
		raise Exception("Error during geocoding")

	return OrderedDict(geocoded_json_result['results'][0]['geometry']['location']).values()
 
    
def get_points_of_interest(source, dest):
    ''' Return major points of interest and rest stops between a given source and destination '''
    src_coord = Coordinates(*get_geocoded_address(source))
    dest_coord = Coordinates(*get_geocoded_address(dest))
    public_src_coord = copy.deepcopy(src_coord)
    public_dest_coord = copy.deepcopy(dest_coord)
    
    #print(URL_dir.replace('__SRC__', googlemaps.convert.latlng(src_coord)).replace('__DEST__', googlemaps.convert.latlng(dest_coord)))
    
    route_json_result = eval(urllib2.urlopen(URL_dir.replace('__SRC__', googlemaps.convert.latlng(src_coord)).replace('__DEST__', googlemaps.convert.latlng(dest_coord))).read())

    if route_json_result["status"] != "OK":
        return {}
    
    bounds = route_json_result["routes"][0]["bounds"]
    bounds_northeast, bounds_southwest = Coordinates(*OrderedDict(bounds["northeast"]).values()), Coordinates(*OrderedDict(bounds["southwest"]).values())
    center = get_midpoint(bounds_northeast, bounds_southwest)
    radius = get_distance(center, bounds_northeast)
    
    #print(URL_geo.replace('__LATLNG__', googlemaps.convert.latlng(list(center))))
    
    place_bias_json_result = eval(urllib2.urlopen(URL_rev_geo.replace('__LATLNG__', googlemaps.convert.latlng(list(center)))).read())

    if place_bias_json_result['status'] != "OK":
        return {}

    place_bias = place_bias_json_result['results'][0]['address_components'][0]['long_name']

    places_json_result = gmaps.places("tourism, restaurants " + place_bias , location=list(src_coord), radius=radius)

    if places_json_result["status"] != "OK":
        return {}

    results = places_json_result['results']
    
    points_of_interest  = {}

    for result in results:
        if 'tour' in result['name'].lower() or 'travels' in result['name'].lower(): 
            continue
        try:
            if result['rating'] >= 4.0:
                points_of_interest[result['name']] = result
        except: 
            continue    # don't bother with seedy places
    
    #print(points_of_interest)

    return points_of_interest


def get_best_route(source, dest, waypoints=None):
    ''' Input: Assumes that the JSON dictionary sent from get_points_of_interest() is returned back in the same format
        Output: Returns the original route if no waypoints have been specified, otherwise queries the google server for a new route passing through all specified waypoints 
    '''
    src_coord = Coordinates(*get_geocoded_address(source))
    dest_coord = Coordinates(*get_geocoded_address(dest))
    
    if wayoints == None or len(waypoints) == 0: 
        return eval(urllib2.urlopen(URL_geo.replace('__LATLNG__', googlemaps.convert.latlng(list(center)))).read())

    waypoint_latlng_list = []

    for waypoint in waypoints.keys():
        waypoint_latlng_list.append(waypoints[waypoint]['geometry']['location'])

    waypoint_polyline_str = googlemaps.convert.encode_polyline(waypoint_latlng_list)

    route_json_result = eval(urllib2.urlopen(URL_dir.replace('__SRC__', googlemaps.convert.latlng(src_coord)).replace('__DEST__', googlemaps.convert.latlng(dest_coord)) + '&waypoints=optimize:true|' + waypoint_polyline_str).read())

    if route_json_result["status"] != "OK":
        raise Exception("Error generating route")

    return route_json_result


def get_midpoint(coord_1, coord_2):
    ''' Finds and returns the coordinates of the midpoint between two points '''
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
    ''' Computes the great-circle distance between two coordinates '''
    t_coord_1 = Coordinates(*map(math.radians, coord_1))
    t_coord_2 = Coordinates(*map(math.radians, coord_2))

    d_lat, d_lng = (t_coord_2.lat - t_coord_1.lat), (t_coord_2.lng - t_coord_1.lng) 
    temp = math.sin(d_lat / 2)**2 + math.cos(t_coord_1.lat) * math.cos(t_coord_2.lat) * math.sin(d_lng / 2)**2

    return 6373.0 * (2 * math.atan2(math.sqrt(temp), math.sqrt(1 - temp)))


if __name__=="__main__":
	''' For testing '''
	#user_source = OrderedDict({u'lat': 12.9715987, u'lng': 77.5945627}) # Bangalore
    #user_dest = OrderedDict({u'lat': 12.2958104, u'lng': 76.6393805}) # Mysore
	pprint(get_points_of_interest("Bangalore, Karnataka, India", "Mysore, Karnataka, India"))






