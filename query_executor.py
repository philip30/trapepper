import key.gnavi_key
import sys
import urllib.parse, urllib.request
import json
import query_parser
from xml.etree.ElementTree import *

class GeoCaller:
    def __init__(self):
        self.api_url = "http://www.geocoding.jp/api/?v=1.1"

    # return latitude, longitude, location name
    # if error occurs, return -1, -1
    def call_api(self, location):
        url = self.api_url + "&q=" + urllib.parse.quote(location)

        # call api
        try :
            result = urllib.request.urlopen( url ).read()
        except ValueError as e :
            print(e)
            print("Failed to access the API.")
            return -1, -1, "error"

        data = fromstring(result.decode('utf-8'))

        # in case of wrong data structure
        try:
            lat = data[2][0].text
            lng = data[2][1].text
            loc_name = data[5].text
        except:
           return -1, -1, "error"

        return lat, lng, loc_name


class GnaviCaller:
    def __init__(self):
        self.gnavi_key = key.gnavi_key.gnavi_keyid
        self.gnavi_url = key.gnavi_key.gnavi_url
        self.require = ["location"]

    def is_str(self, data = None) :
      if isinstance(data, str) :
        return True
      else :
        return False

    def are_enough_entities(self, entities):
        for req in self.require:
            if req not in entities.keys():
                return False, req
        return True, ""

    # return number of hit restaurants and data
    # if error occurs, return -1
    def call_api(self, query):
        # add api key to query
        query.append(("keyid", self.gnavi_key))

        # generate URL
        url = self.gnavi_url + "?" + urllib.parse.urlencode( query )

        # call api
        try :
            result = urllib.request.urlopen( url ).read()
        except ValueError :
            print("Failed to access the API.")
            return -1, []
        data = json.loads( result.decode('utf-8') )
         
        # error occurs
        if "error" in data :
            if "message" in data["error"] :
                print(data["error"]["message"])
            else :
                print("Failed to get the data.")
            return -1, []
         
        # get number of hits
        total_hit_count = None
        if "total_hit_count" in data :
            total_hit_count = int(data["total_hit_count"])
        
        if total_hit_count is None or total_hit_count <= 0 :
            print("No hit.")
            return 0, data
         
        if not "rest" in data :
            print("cannot find any restaurants.")
            return 0, data
         
        # show number of hits
        print("found %d restaurants." % (total_hit_count) )
        print("----")

        return total_hit_count, data

    def print_data(self, data):
        for rest in data["rest"]:
            line                 = []
            id                   = ""
            name                 = ""
            access_line          = ""
            access_station       = ""
            access_walk          = ""
            code_category_name_s = []

            # restaurant id
            if "id" in rest and self.is_str( rest["id"] ) :
                id = rest["id"]
            line.append( id )

            # restaurant name
            if "name" in rest and self.is_str( rest["name"] ) :
                name = rest["name"]
            line.append( name )

            if "access" in rest :
                access = rest["access"]
                # nearest train line
                if "line" in access and self.is_str( access["line"] ) :
                    access_line = access["line"]
                # nearest station
                if "station" in access and self.is_str( access["station"] ) :
                    access_station = access["station"]
                # need time from the nearest station to the restaurant
                if "walk"    in access and self.is_str( access["walk"] ) :
                    access_walk = access["walk"] + "分"
            line.extend( [ access_line, access_station, access_walk ] )

            # restaurant small category
            if "code" in rest and "category_name_s" in rest["code"] :
                for category_name_s in rest["code"]["category_name_s"] :
                    if self.is_str( category_name_s ) :
                        code_category_name_s.append( category_name_s )
            line.extend( code_category_name_s )

            print("\t".join( line ))


class RestaurantAPIManager:
    def __init__(self, entities):
        self.entities = entities
        self.api_caller = GnaviCaller()

    def are_enough_entities(self):
        print(self.entities)
        return self.api_caller.are_enough_entities(self.entities)

    def print_data(self, data):
        self.api_caller.print_data(data)

    def call_api(self):
        geo_api = GeoCaller()
        lat, lng, place_name = geo_api.call_api(self.entities["location"])
        
        print("searching near " + place_name)
        query = [
          ( "format",       "json" ),
          ( "latitude",     lat    ),
          ( "longitude",    lng    ),
          ( "input_coordinates_mode", 1),
          ( "hit_per_page", 10     ),
          ( "range",        5  ),
          ( "category_s",   self.entities["genre_id"])
        ]

        count, api_result = self.api_caller.call_api(query)
        if count == -1:
            raise Exception("API Error")

        return api_result


class QueryExecutor:
    def __init__(self):
        pass

    def run(self, action):
        return self.execute(action)

    def execute_restaurant(self, entities):
        api_manager = RestaurantAPIManager(entities)
        ret_data = {}

        ret_data["looking_for"] = "restaurant"
        ret_data["enough_entities"], ret_data["next_entity"] = api_manager.are_enough_entities()
        if ret_data["enough_entities"] == False:
            return ret_data
        
        ret_data["recv"] = api_manager.call_api()
        if len(ret_data["recv"]["rest"]) > 0:
            api_manager.print_data(ret_data["recv"])
        return ret_data

    def execute_question(self, action):
        if action["entities"]["looking_for"] == "restaurant":
            return self.execute_restaurant(action["entities"])
        if action["entities"]["looking_for"] == "hotel":
            pass

    def execute(self, action):
        if action["query_type"] == "question":
            return self.execute_question(action)

        if action["query_type"] == "hello":
            pass

        if action["query_type"] == "bye":
            pass

        
class TestQueryExecutor:
    def __init__(self):
        self.query_exec = QueryExecutor()
        pass

    def test(self):
        inp = "奈良先端近くの居酒屋を探して"

        qparser = query_parser.QueryParser("./resources/small_search.tsv")
        action = qparser.parse(inp)
        print(action)
        result = self.query_exec.run(action)
        print(result)


if __name__ == "__main__":
    # Test
    test_query_exec = TestQueryExecutor()
    test_query_exec.test()
    

