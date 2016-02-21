
from trapepper.lib import ActionType
from trapepper.util import log

# DIALOGS
def count_restaurant(data):
    # TODO
    count = len(data["recv"]["rest"])
    if count > 1:
        response_str = "There are " + str(count) + " restaurants found. "
    else:
        response_str = "There is one restaurant found. "
    return response_str

def ask_more_entity(action):
    # TODO
    missing_entity = action.args.strip()
    if missing_entity == "location":
        return "すみません。場所は教えてください。"
    else:
        raise NotImplementedError()

def pardon():
    # TODO
    return "すみません。わかりませんでした。"

def no_matching_restaurant():
    return "I am sorry, I could not find any restaurants."

# ROUTINES
def add_response(response, data):
    if type(data) == str:
        response.append(data)
    elif type(data) == list or type(data) == tuple:
        response[len(response):] = list(data)
    else:
        response.append(data)

def casual_chat(dialog):
    if dialog == "hello":
        return "こんにちは。"
    elif dialog == "bye":
        return "バイバイ。"
    else:
        return "That's interesting."

def is_missing_entity(action):
    return action.args is not None and len(action.args) > 0

def is_restaurant_empty(data):
    return len(data["recv"]["rest"]) == 0

class ResponseGenerator:
    
        
    def generate_response(self, action, data):
        responses = []
        say = lambda x: add_response(responses, x)
        if action.action_type == ActionType.pardon:
            if is_missing_entity(action):
                say(ask_more_entity(action))
            else:
                say(pardon())
        elif action.action_type == ActionType.exec_hotel:
            # Restaurant count
            if is_restaurant_empty(data):
                say(no_matching_restaurant())
            else:
                say(count_restaurant(data))
        elif action.action_type == ActionType.dialogue:
            say(casual_chat(action.args))
        #elif action.action_type == ActionType.filter:
        #    pass 
        else:
            raise NotImplementedError()
        return responses


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
                            response_str += "Restaurant number " + str(idx) + " is called " + rest["name"] + ". "
                        else:
                            response_str += "The restaurant name is " + rest["name"] + ". "
                        response_str += "Near there, there is a train line called " + access["line"] + " which should be taken to get there. "
                    # could not find the restaurant's name, but nearby train line
                    else:
                        if count > 1:
                            response_str += "I could not find the name of restaurant number " + str(idx) + ". "
                        else:
                            response_str += "I could not find the name of the restaurant. "
                        response_str += "But, near there, there is a train line called " + access["line"] + " which should be taken to get there. "
                    # found nearby train line and station
                    if "station" in access and self.is_str( access["station"] ):
                        response_str += "Furthermore, there is also a nearby train station called " + access["station"] + ". "
                        # found nearby train line and station and walking minutes from the nearby station
                        if "walk" in access and self.is_str( access["walk"] ):
                            response_str += "From there you can get to the place on foot within " + str(access["walk"]) + " minutes. "
                    else:
                        # found nearby train line and walking minutes from its nearby station
                        if "walk" in access and self.is_str( access["walk"] ):
                            response_str += "And, from its nearest station you can get there on foot within " + str(access["walk"]) + " minutes. "
                # could not find nearby train line
                else:
                    # found nearby train sta:w
                    tion
                    if "station" in access and self.is_str( access["station"] ):
                        # found the restaurant's name
                        if "name" in rest and self.is_str( rest["name"] ):
                            if count > 1:
                                response_str += "Restaurant number " + str(idx) + " is called " + rest["name"] + ". "
                            else:
                                response_str += "The restaurant name is " + rest["name"] + ". "
                            response_str += "Near there, there is a train station called " + access["line"] + ". "
                        # could not find the restaurant's name
                        else:
                            if count > 1:
                                response_str += "I could not find the name of restaurant number " + str(idx) + ". "
                            else:
                                response_str += "I could not find the name of the restaurant. "
                            response_str += "But, near there, there is a train station called " + access["station"] + ". "
                        # found  walking minutes from the nearby station
                        if "walk" in access and self.is_str( access["walk"] ):
                            response_str += "And from there you can get to the place on foot within " + str(access["walk"]) + " minutes. "
                    # could not find nearby train station
                    else:
                        # found walking minutes from nearby train station
                        if "walk" in access and self.is_str( access["walk"] ):
                            # found the restaurant's name
                            if "name" in rest and self.is_str( rest["name"] ):
                                if count > 1:
                                    response_str += "Restaurant number " + str(idx) + " is called " + rest["name"] + ". "
                                else:
                                    response_str += "The restaurant name is " + rest["name"] + ". "
                                response_str += "If you try to walk from its nearest station, it will take about " + str(access["walk"]) + " minutes. "
                            # could not find the restaurant's name
                            else:
                                if count > 1:
                                    response_str += "I could not find the name of restaurant number " + str(idx) + ". "
                                else:
                                    response_str += "I could not find the name of the restaurant. "
                                response_str += "But, if you try to walk from its nearest station, it will take about " + str(access["walk"]) + " minutes. "
                        # could not find name and access for this restaurant
                        else:
                            if count > 1:
                                response_str += "I am sorry, I could not find the name and access details for the restaurant number " + str(idx) + ". "
                            else:
                                response_str += "I am sorry, I could not find the name and access details for this restaurant. "
            # could not find access for this restaurant
            else:
                # found restaurant's name
                if "name" in rest and self.is_str( rest["name"] ):
                    if count > 1:
                        response_str += "Restaurant number " + str(idx) + " is called " + rest["name"] + ". "
                    else:
                        response_str += "The restaurant name is " + rest["name"] + ". "
                    response_str += "But, I am sorry, I could not find the access detail to get there. "
                # could not find restaurant's name
                else:
                    if count > 1:
                        response_str += "I am sorry, I could not find the name and access details for the restaurant number " + str(idx) + ". "
                    else:
                        response_str += "I am sorry, I could not find the name and access details for this restaurant. "
            idx += 1
