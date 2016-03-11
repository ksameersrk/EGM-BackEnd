"""
    A program to return a list of places of interest based on the user's location.

    Get location of 1 or more users.
    Return names of places based on the type of places requested.
    Return a list of tuples of coordinates of all the
        places of interest.

   Prerequisites : a google API key with the Google Places services activated
                    for it.
"""

from googleplaces import GooglePlaces,types,lang
from define_circle import make_circle
import re
try:
    import urllib2
except:
    print("Run with python2")

#api_key =
api_key = 'AIzaSyCJg4Ezwp-xEMiQlpeuGJxofCL2HOb031s'
#using Shiva's API key

google_places = GooglePlaces(api_key)   #initialize
url = 'https://maps.googleapis.com/maps/api/geocode/json?address=__HOLDER__'

def url_translate(address):

    #modifies the url to contain the location entered by user
    return url.replace('__HOLDER__',re.sub(" ","+",address))

def get_coordinates(location):

    #returns coordinates of location specified in variable 'location'
    location = eval(urllib2.urlopen(url_translate(location)).read())
    loc_coord = location['results'][0]['geometry']['location'].values()
    return loc_coord

def get_coordinates_of_users(list_of_locations):

    #to get coordinates of the users' locations
    #points is a list of tuples
    #tuple contains lat and long of users loc respectively
    points = list()
    for i in list_of_locations:
        points.append(tuple(get_coordinates(i)))

    return points

def display_places_names(query_results):

    #displays names of places of interests
    for places in query_results.places:
        print(places.name)

def display_places_details(query_results):
    for place in query_results.places:
        place.get_details()
        print(place.details)


def get_coordinates_of_places(query_results):

    #computes the coordinates of places of interest
    #returns a list of tuples
    coords_places = list()
    for places in query_results.places:
        coords_places.append((places.geo_location[u'lat'],places.geo_location[u'lng']))

    return coords_places

if __name__ == "__main__":
    num_users = int(input("Enter the number of users."))
    if(num_users == 0):
        print("Enter 1 or more number of users.")

    elif(num_users == 1):
        user_location = 'Connaught Place, New Delhi'
        query_results = google_places.nearby_search(
                location=user_location, radius=200000,
                types=[types.TYPE_FOOD]
                )
        #display_places_names(query_results)
        #coordinates_of_places = get_coordinates_of_places(query_results)
        #display_places_details(query_results)

    elif(num_users>1):
        #take list of locations from front end
        locations = ["Koramangala, Bangalore","MG Road, Bangalore","Jayanagar, Bangalore"]
        points = get_coordinates_of_users(locations)

        #smallest circle covering all the given users
        circle = make_circle(points)
        query_results = google_places.nearby_search(
                lat_lng={'lat':circle[0], 'lng':circle[1]},
                radius=circle[2]*100000, sensor=False, keyword=None,
                types=[types.TYPE_FOOD]
                )

        #display_places_names(query_results)


        #coordinates_of_places is a list of tuples
        #first arg of tuple is lat
        #second arg is long
        coordinates_of_places = get_coordinates_of_places(query_results)
        #print(coordinates_of_places)

