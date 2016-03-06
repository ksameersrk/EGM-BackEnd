from googleplaces import GooglePlaces, types, lang
from define_circle import make_circle
import re

try:
	import urllib2
except:
	print("Run with python2")

#api_key = 'AIzaSyCCz-xlpsIZ4vctgEcWEJKMFWTGuJkzJLM'
api_key = 'AIzaSyCJg4Ezwp-xEMiQlpeuGJxofCL2HOb031s' #using Shiva's API key.

google_places = GooglePlaces(api_key)	#initialize

url='https://maps.googleapis.com/maps/api/geocode/json?address=__HOLDER__'  # make a class and put this in -- later

def url_translate(address): #modifies the url to contain the location we are searching for
	return url.replace('__HOLDER__', re.sub(" ", "+", address))

def get_coordinates(location):  #returns the coordinates of the location specified in variable 'location'
	location = eval(urllib2.urlopen(url_translate(location)).read())
	loc_coord = location['results'][0]['geometry']['location'].values()
	return loc_coord

def get_coord_users(list_of_locations): #to get the coords of the users' locations
	points = list()
	for i in list_of_locations:
            points.append(tuple(get_coordinates(i)))
        #points is a list of tuples - containing (x, y) coords of all users
	return points

def display_names_places(query_results): #displays names of places - provide functions for other such functionality
    for places in query_results.places:
        print(places.name)

if __name__ == "__main__":
        num_users = int(input("Enter the number of users: "))
        #use switch case, instead of if stts -- later
	if(num_users == 0):
	    print("Enter 1 or more number of users.")
	    
        #elif(num_users == 1):
            ''' 
            
            	complete this
            
            '''
            
	elif(num_users > 1):
            #take input(list of locations) from front end
            locations = ["Koramangala, Bangalore","MG Road, Bangalore","Jayanagar, Bangalore"] # for testing

            points = get_coord_users(locations)
            circle = make_circle(points)	#smallest circle, covering all the given users.
            query_results = google_places.nearby_search(lat_lng = {'lat':circle[0], 'lng':circle[1]}, radius = circle[2]*100000, sensor=False, keyword=None, types=[types.TYPE_FOOD])
            # query_results = google_places.nearby_search(location="Koramangala, Bangalore",radius=2000,types=[types.TYPE_GAS_STATIONS])

            display_names_places(query_results)


