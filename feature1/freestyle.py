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
gmaps = googlemaps.Client(API_KEY)  # initialize client

''' Defining template URL strings '''
URL_dir = 'https://maps.googleapis.com/maps/api/directions/json?origin=__SRC__&destination=__DEST__&key=%s' % API_KEY  # 1) template URL string for quering the directions API
URL_geo = 'https://maps.googleapis.com/maps/api/geocode/json?address=__ADD__&key=%s' %API_KEY # 3) template URL string for quering the geocoding API
URL_rev_geo = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=__LATLNG__&result_type=administrative_area_level_1&key=%s' %API_KEY  # 2) template URL string for quering the reverse-geocoding API


def get_geocoded_address(address):
	''' Converts a human readable address into its correponding latlng coordinates and returns it as a list '''
	geocoded_json_result = eval(urllib2.urlopen(URL_geo.replace('__ADD__', address.replace(" ", "+"))).read())	# send geocoding query

	# Status check
	if geocoded_json_result['status'] == "ZERO_RESULTS": 
		raise Exception("No valid latlng coordinates for given address")	
	
	elif geocoded_json_result['status'] != "OK":
		raise Exception("Error during geocoding")

	# Extract the {'lat': ..., 'lng': ...} dict from the json reply and return coordinates '''
	return OrderedDict(geocoded_json_result['results'][0]['geometry']['location']).values()
 
    
def get_points_of_interest(source, dest):
    ''' Return major points of interest and rest stops between a given source and destination '''
    # Convert the source and destination coordinates (returned from get_geocoded_address()) into objects of the pseudoclass 'Coordinates' 
    src_coord = Coordinates(*get_geocoded_address(source)) 
    dest_coord = Coordinates(*get_geocoded_address(dest))
    
    # Send a directions query with the given source and destination coordinates. This seems redundant but is necessary to extract the bounding coordinates for the source and destination
    route_json_result = eval(urllib2.urlopen(URL_dir.replace('__SRC__', googlemaps.convert.latlng(src_coord)).replace('__DEST__', googlemaps.convert.latlng(dest_coord))).read()) 

    # Status check
    if route_json_result["status"] != "OK":
        return {}
    
    # Extract bounding-box coordinates from 'bounds' property
    bounds = route_json_result["routes"][0]["bounds"]
    bounds_northeast, bounds_southwest = Coordinates(*OrderedDict(bounds["northeast"]).values()), Coordinates(*OrderedDict(bounds["southwest"]).values())
    center = get_midpoint(bounds_northeast, bounds_southwest) # get the center point coordinate between the bounding-box coordinates
    radius = get_distance(center, bounds_northeast) # get the length of the half-diagonal between the two bounding-box coordinates

	# Send a reverse geocoding query for the center coordinate. This is needed to bias the places query results. The query will return only the English readable administrative level 1 address (in other words, the name of the state or union territory in which the coordinates reside)
    place_bias_json_result = eval(urllib2.urlopen(URL_rev_geo.replace('__LATLNG__', googlemaps.convert.latlng(list(center)))).read()) 

    # Status check
    if place_bias_json_result['status'] != "OK":
        return {}

    # Extract the state/union territory name
    place_bias = place_bias_json_result['results'][0]['address_components'][0]['long_name']

    # Send a places query to find points of interest with the given location and radius biases
    places_json_result = gmaps.places("tourism, restaurants " + place_bias , location=list(src_coord), radius=radius)

    # Status check
    if places_json_result["status"] != "OK":
        return {}

    results = places_json_result['results']
    
    points_of_interest  = {}

    # Fill in points of interest, leaving out places with low ratings and tourism agencies
    for result in results:
        if 'tour' in result['name'].lower() or 'travels' in result['name'].lower(): 
            continue
        try:
            if result['rating'] >= 4.0:
                points_of_interest[result['name']] = result
        except: 
            continue    # don't bother with seedy places

    return points_of_interest


def get_best_route(source, dest, waypoints=None):
    ''' Input: Assumes that the json dictionary sent from get_points_of_interest() is returned back in the same format
        Output: Returns the original route if no waypoints have been specified, otherwise queries the google server for a new route passing through all specified waypoints 
    '''
    # Convert the source and destination coordinates (returned from get_geocoded_address()) into objects of the pseudoclass 'Coordinates' 
    src_coord = Coordinates(*get_geocoded_address(source))
    dest_coord = Coordinates(*get_geocoded_address(dest))
    
    # Test if there are no specified waypoints, and return the json result of a very simple directions query
    if waypoints == None or len(waypoints) == 0: 
        return eval(urllib2.urlopen(URL_geo.replace('__LATLNG__', googlemaps.convert.latlng(list(center)))).read())

    waypoint_latlng_list = []

    # Extracy coordinates of each waypoint from the waypoints dictionary
    for waypoint in waypoints.keys():
        waypoint_latlng_list.append(waypoints[waypoint]['geometry']['location'])

    # Googlemaps queries sent through URLs have length restrictions. This is solved by encoding the coordinates into a polyline string and then passing the string as a parameter in a directions query
    waypoint_polyline_str = googlemaps.convert.encode_polyline(waypoint_latlng_list)

    # Send a directions query with the given source, destination coordinates, and waypoints list encoded as a polyline
    route_json_result = eval(urllib2.urlopen(URL_dir.replace('__SRC__', googlemaps.convert.latlng(src_coord)).replace('__DEST__', googlemaps.convert.latlng(dest_coord)) + '&waypoints=optimize:true|enc:' + waypoint_polyline_str + ':').read())

    # Status check
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
	pprint(get_best_route("Bangalore, Karnataka, India", "Mysore, Karnataka, India", get_points_of_interest("Bangalore, Karnataka, India", "Mysore, Karnataka, India")))

