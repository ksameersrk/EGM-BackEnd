'''
    API Key: Shiva: AIzaSyB_djwAiUd0Vt3gQgnPxR37gjenE0j3dTU
            Sharon: AIzaSyAZ0yEBve1U580KqocYg-4YwbjoieoriYY
    Part 1
    Retrieve source and destination from front end
    Find places of interest between source and destination and retrieve their location using Client.geocode() - will get lat, long of that place
    
    Part 2
    Compute some logically feasable paths between the source and destination having the places of interest as intermediate points
    
    Part 3
    For each path
    Convert the tuples of lat - long to a road route: use Client.snap_to_road()
    Return this list of paths to the front end
    
    04/03/16
    Module 1
    Get src destination
    Return places
    
    Module 2
    Get places
    Return route
'''

import googlemaps, sys, re
from pprint import pprint

try:
    import urllib2
except:
    print('Run with python2')
    exit()

api_key='AIzaSyAZ0yEBve1U580KqocYg-4YwbjoieoriYY'

url='https://maps.googleapis.com/maps/api/geocode/json?address=__HOLDER__&key=%s' %api_key

gmaps=googlemaps.Client(api_key) # initialize client


def url_translate(address):
  
    return url.replace('__HOLDER__', re.sub(" ", "+", address))


def get_best_route(src, dest, waypoints=None):
  
    src=eval(urllib2.urlopen(url_translate(src)).read())
    src_coord=src['results'][0]['geometry']['location'].values()

    dest=eval(urllib2.urlopen(url_translate(dest)).read())
    dest_coord=dest['results'][0]['geometry']['location'].values()

    #get route
    route = gmaps.directions(src_coord, dest_coord, waypoints=waypoints, optimize_waypoints=True)

    return route

if __name__=="__main__":
    #input - source, destination, list of places
    #output - route

    user_source = 'Bangalore'
    user_dest = 'Mysore'
    user_dict_places = {u'Bekal Fort': [u'ChIJW4IkcJmApDsRcbLXdzA6qd8', [12.3926108, 75.0327804], 4.4], u'Brindavan Gardens': [u'ChIJXcr-CeF4rzsRsrbm4H66X5E',[12.4241482, 76.573025],4], u'Mysore Palace': [u'ChIJ-aH5AxFwrzsRDdokoeK6f8M',[12.3051351, 76.6551483],4.5], u'Mysore Zoo': [u'ChIJlXcOBCNwrzsRy79sy0wzV-o', [12.3024314, 76.663752], 4.3]}

    name_waypoints = []
    list_waypoints = []

    for i in user_dict_places.keys():
        name_waypoints.append(i)
        list_waypoints.append(user_dict_places[i][1])

    '''print("LIST")
    print(name_waypoints)'''

    final_route = get_best_route(user_source, user_dest, waypoints=list_waypoints)[0]

    '''print("FINAL")
    print(final_route['waypoint_order'])'''

    #pprint(finalRoute)







