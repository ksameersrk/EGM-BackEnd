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
                place_dictionary["users_lat"] - list of latitudes of all users(only 1 value in case of single user).
                place_dictionary["users_long"] - list of longitudes of all users(only 1 value in case of single user).
                place_dictionary["all_details"] - list of some details of all the places.
                                            -(important) Order of details is - 'Url','Rating','Name','Address' 
                                                which correspond to a single place. Any of these values may be 'None', 
                                                in which case the list will have "" against those values.
                                                The next four values are for the next place in the list and so on.

                                                    
