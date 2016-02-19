class ResponseGenerator:
    def generate_response(self, data):
        # Not enough query, ask again
        if data["enough_entities"] == False:
            return "Pardon me, please state your question one more time."
        # No restaurants found
        if len(data["recv"]["rest"]) == 0:
            return "I am sorry, I could not find any restaurants."
        # Found restaurant(s)
        count = len(data["recv"]["rest"])
        if count > 1:
            response_str = "There are " + str(count) " + " restaurants found. "
        else:
            response_str = "There is one restaurant found. "
        # iterate each restaurant's details
        idx = 1;
        for rest in data["recv"]["rest"]:
            # found access to restaurant
            if "access" in rest:
                access = rest["access"]
                # found nearby train line
                if "line" in access and self.is_str( access["line"] ):
                    # found the restaurant's name and nearby train line
                     if "name" in rest and self.is_str( rest["name"] ):
                        if count > 1:
                            response_str += "Restaurant number " + str(idx) + " is called " + rest["name"] + "."
                        else:
                            response_str += "The restaurant name is " + rest["name"] + "."
                        response_str += "Near there, there is a train line called " + access["line"] + " which should be taken to get there."
                    # could not find the restaurant's name, but nearby train line
                    else:
                        if count > 1:
                            response_str += "I could not find the name of restaurant number " + str(idx) + "."
                        else:
                            response_str += "I could not find the name of the restaurant."
                        response_str += "But, near there, there is a train line called " + access["line"] + " which should be taken to get there."
                    # found nearby train line and station
                    if "station" in access and self.is_str( access["station"] ):
                        response_str += "Furthermore, there is also a nearby train station called " + access["station"] + "."
                        # found nearby train line and station and walking minutes from the nearby station
                        if "walk" in access and self.is_str( access["walk"] ):
                            response_str += "From there you can get to the place on foot within " + str(access["walk"]) + " minutes."
                    else:
                        # found nearby train line and walking minutes from its nearby station
                        if "walk" in access and self.is_str( access["walk"] ):
                            response_str += "And, from its nearest station you can get there on foot within " + str(access["walk"]) + " minutes."
                # could not find nearby train line
                else:
                    # found nearby train station
                    if "station" in access and self.is_str( access["station"] ):
                        # found the restaurant's name
                         if "name" in rest and self.is_str( rest["name"] ):
                            if count > 1:
                                response_str += "Restaurant number " + str(idx) + " is called " + rest["name"] + "."
                            else:
                                response_str += "The restaurant name is " + rest["name"] + "."
                            response_str += "Near there, there is a train station called " + access["line"] + "."
                        # could not find the restaurant's name
                        else:
                            if count > 1:
                                response_str += "I could not find the name of restaurant number " + str(idx) + "."
                            else:
                                response_str += "I could not find the name of the restaurant."
                            response_str += "But, near there, there is a train station called " + access["station"] + "."
                        # found  walking minutes from the nearby station
                        if "walk" in access and self.is_str( access["walk"] ):
                            response_str += "And from there you can get to the place on foot within " + str(access["walk"]) + " minutes."
                    # could not find nearby train station
                    else:
                        # found walking minutes from nearby train station
                        if "walk" in access and self.is_str( access["walk"] ):
                            # found the restaurant's name
                             if "name" in rest and self.is_str( rest["name"] ):
                                if count > 1:
                                    response_str += "Restaurant number " + str(idx) + " is called " + rest["name"] + "."
                                else:
                                    response_str += "The restaurant name is " + rest["name"] + "."
                                response_str += "If you try to walk from its nearest station, it will take about " + str(access["walk"]) + " minutes."
                            # could not find the restaurant's name
                            else:
                                if count > 1:
                                    response_str += "I could not find the name of restaurant number " + str(idx) + "."
                                else:
                                    response_str += "I could not find the name of the restaurant."
                                response_str += "But, if you try to walk from its nearest station, it will take about " + str(access["walk"]) + " minutes."
                        # could not find name and access for this restaurant
                        else:
                            if count > 1:
                                response_str += "I am sorry, I could not find the name and access details for the restaurant number " + str(idx)
                            else:
                                response_str += "I am sorry, I could not find the name and access details for this restaurant.
            # could not find access for this restaurant
            else:
                # found restaurant's name
                 if "name" in rest and self.is_str( rest["name"] ):
                    if count > 1:
                        response_str += "Restaurant number " + str(idx) + " is called " + rest["name"] + "."
                    else:
                        response_str += "The restaurant name is " + rest["name"] + "."
                    response_str += "But, I am sorry, I could not find the access detail to get there."
                # could not find restaurant's name
                else:
                    if count > 1:
                        response_str += "I am sorry, I could not find the name and access details for the restaurant number " + str(idx)
                    else:
                        response_str += "I am sorry, I could not find the name and access details for this restaurant.
            idx += 1
        return response_str
