
'''
API Key: AIzaSyB_djwAiUd0Vt3gQgnPxR37gjenE0j3dTU

Part 1
Retrieve source and destination from front end
Find places of interest between source and destination and retrieve their location using Client.geocode() - will get lat, long of that place

Part 2
Compute some logically feasable paths between the source and destination having the places of interest as intermediate points

Part 3
For each path
	Convert the tuples of lat - long to a road route: use Client.snap_to_road() 
Return this list of paths to the front end
'''

# implementing Part 1 for feature 1
import googlemaps, sys, re
from pprint import pprint

try:
	import urllib2
except:
	print("Run with Python2")
	exit()

api_key='AIzaSyB_djwAiUd0Vt3gQgnPxR37gjenE0j3dTU'

url='https://maps.googleapis.com/maps/api/geocode/json?address=__HOLDER__&key=%s' %api_key

gmaps=googlemaps.Client(api_key) # initialize client

def get_points_of_interest(src, dest):

	def url_translate(address): 
		return url.replace('__HOLDER__', re.sub(" ", "+", address))

	src=eval(urllib2.urlopen(url_translate(src)).read())
	dest=eval(urllib2.urlopen(url_translate(dest)).read())

	try:
		src_coord=src['results'][0]['geometry']['location'].values()
		dest_coord=dest['results'][0]['geometry']['location'].values()

	except:
		print("Error")
		exit()

	
	roads=set()
	points_of_interest=[]

	for s in gmaps.directions(src_coord, dest_coord)[0]['legs'][0]['steps']: 
		roads=roads.union(set(re.findall(r"<b>(.*?)</b>", s['html_instructions'])) - {'north', 'south', 'east', 'west', 'left', 'right'})

	for road in roads:
		print(road)

		for result in gmaps.places("tourism near "+road)['results']: 
			print(result['name'])	
			try:
				points_of_interest.append((result['place_id'], result['name'], result['rating']))
			except: 
				continue 	# don't bother with seedy places

	return points_of_interest


if __name__=="__main__":
	get_points_of_interest('Bangalore', 'Mangalore')



