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

api_key = 'AIzaSyCyr22Z9rtPUYH5QpeBuIPU_2ITgCSBG78'

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


def get_details_of_all_places(query_results,num_places=5):
    '''
        Returns a list of dictionaries.
        Every dictionary has details about
            a place.
    '''
    count = 0;
    details = list()
    for place in query_results.places:
        if(count == num_places):
            break
        place.get_details()
        details.append({
            "Name":str(place.name), "Rating":float(place.rating),
            "Address":str(place.formatted_address), "Url":str(place.url)
            })
        count += 1

    return details

def display_details_of_all_places(details):
    '''
        Input - list of dictionaries about
                details of places.
        Output - displays details of places.
    '''
    for details_dict in details:
        print(details_dict["Name"])
        print(details_dict["Rating"])
        print(details_dict["Address"])
        print(details_dict["Url"])
        print(details_dict["Photo_url"])
        print("*****************")

    print()

def get_details_of_single_place(query_results, place_):

    '''
        gets details of place specified in the arg.
    '''
    details = dict()
    details["Name"] = query_results.places[place_].name
    details["Rating"] = query_results.places[place_].rating
    details["Address"] = query_results.places[place_].formatted_address
    details["Url"] = query_results.places[place_].url;
    return details

def display_details_of_single_place(details_dict):

    print(details_dict["Name"])
    print(details_dict["Rating"])
    print(details_dict["Address"])
    print(details_dict["Url"])

def get_coordinates_of_places(query_results, num_places = 5):

    #computes the coordinates of places of interest
    #returns a list of tuples
    count = 0;
    coords_places = list()
    for places in query_results.places:
        if(count == num_places):
            break
        coords_places.append((float(places.geo_location[u'lat']),
            float(places.geo_location[u'lng'])))
        count += 1

    return coords_places

def put_everything_in_dictionary(coordinates_of_places,points,details):

    '''
        put everything passed in the list arguments
        into a dictionary.
    '''
    dictionary = dict()
    places_lat = list()
    places_long = list()
    users_lat = list()
    users_long = list()
    all_details = list()
    for tups in coordinates_of_places:
        places_lat.append(tups[0])
        places_long.append(tups[1])
    for tups in points:
        users_lat.append(tups[0])
        users_long.append(tups[1])
    for dicts in details:
        all_details.append(dicts["Name"])
        all_details.append(dicts["Rating"])
        all_details.append(dicts["Address"])
        all_details.append(dicts["Url"])

    dictionary["places_lat"] = places_lat
    dictionary["places_long"] =  places_long
    dictionary["users_lat"] = users_lat
    dictionary["users_long"] = users_long
    dictionary["all_details"] = all_details

    return dictionary

if __name__ == "__main__":
    num_users = int(input("Enter the number of users."))
    if(num_users == 0):
        print("Enter 1 or more number of users.")

    elif(num_users == 1):
        user_location = 'Connaught Place, New Delhi'
        search_radius = int(input("Enter the radius for search"))
        query_results = google_places.nearby_search(
                location=user_location, radius=search_radius,
                types=[types.TYPE_FOOD]
                )

        locations = list()
        locations.append(user_location)

	coordinates_of_places = get_coordinates_of_places(query_results,num_places=3)
        points = get_coordinates_of_users(locations)
        details = get_details_of_all_places(query_results,num_places=3)

        #place_dictionary is a dict of everything about all
        # the places
        place_dictionary = put_everything_in_dictionary(coordinates_of_places,
                points,details)
        print(place_dictionary)

        #display_details_of_all_places(details)
        #display_places_names(query_results)
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
        coordinates_of_places = get_coordinates_of_places(query_results,num_places=3)
        details = get_details_of_all_places(query_results,num_places=3)
        place_dictionary = put_everything_in_dictionary(coordinates_of_places,
                points,details)
        print(place_dictionary)







