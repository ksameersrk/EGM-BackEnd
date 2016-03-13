The entire implementation is done via function calls.
There are no classes.

USAGE - 
In the main section - 
    function call - put_everything_in_dictionary()
    function args - coordinates_of_places,points,details
    output - place_dictionary - is a dictionary.
        place_dictionary["places_lat"] - gives a list of latitudes of all places
        e.g. for i in place_dictionary["places_lat"]:
                #i - latitude values in float   
        place_dictionary["places_long"] - list of longitudes of all places
        place_dictionary["users_lat"] - list of latitudes of all users(1 value if single user).
        place_dictionary["users_long"] - list of longitudes of all users(1 value if single user).
        place_dictionary["all_details"] - list of lists 
                                        -  every list contains details of all the places.   
            -(important) Order of details is - Name,Rating,Address,Url
            which correspond to a single place. Any of these values may be 'None', 
            in which case the list will have "" against those values.
