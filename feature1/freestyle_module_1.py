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

api_key='AIzaSyCJg4Ezwp-xEMiQlpeuGJxofCL2HOb031s'

url='https://maps.googleapis.com/maps/api/geocode/json?address=__HOLDER__&key=%s' %api_key

gmaps=googlemaps.Client(api_key) # initialize client


def url_translate(address):
   
    return url.replace('__HOLDER__', re.sub(" ", "+", address))


def get_points_of_interest(src, dest):    
   
    src=eval(urllib2.urlopen(url_translate(src)).read())
    src_coord=src['results'][0]['geometry']['location'].values()
    
    dest=eval(urllib2.urlopen(url_translate(dest)).read())
    dest_coord=dest['results'][0]['geometry']['location'].values()
    
    roads=set()
    points_of_interest={}
    
    directions=gmaps.directions(src_coord, dest_coord)
    for s in directions[0]['legs'][0]['steps']:
        roads=roads.union(set(re.findall(r"<b>(.*?)</b>", s['html_instructions'])) - {'north', 'south', 'east', 'west', 'left', 'right'})
    
    for road in roads:
        #print(road)
        
        for result in gmaps.places("tourism on "+road, location=src_coord, radius=directions[0]['legs'][0]['distance']['value']//2.5)['results']:
            
            if 'tour' in result['name'].lower() or 'travels' in result['name'].lower(): continue

            try:
                points_of_interest[result['name']]=[result['place_id'], result['geometry']['location'].values(), result['rating']]
                print("hola")
            except: 
                continue 	# don't bother with seedy places
           
    if len(points_of_interest) is 0: return {}
    
    sum = 0
    for waypoint, waypoint_details in points_of_interest.items():
        sum = sum + waypoint_details[-1]
    
    avg = sum // len(points_of_interest)
    
    final_result_dict = {}
    
    for waypoint, waypoint_details in points_of_interest.items():
        if waypoint_details[-1] >= avg:
            final_result_dict[waypoint]=waypoint_details
    
    return final_result_dict

if __name__=="__main__":
    #input - source, destination
    #find average rating
    #pull out places with rating greater than the average
    #output - list of places

    user_source = 'Bangalore'
    user_dest = 'Mysore'
    
    pprint(get_points_of_interest(user_source, user_dest))

