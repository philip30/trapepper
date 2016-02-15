import key.gnavi_key
import sys
import urllib.parse, urllib.request
import json
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
            return -1, -1, ""

        data = fromstring(result.decode('utf-8'))
        lat = data[2][0].text
        lng = data[2][1].text
        loc_name = data[5].text

        return lat, lng, loc_name


class GnaviCaller:
    def __init__(self):
        self.gnavi_key = key.gnavi_key.gnavi_keyid
        self.gnavi_url = key.gnavi_key.gnavi_url

    def is_str(self, data = None) :
      if isinstance(data, str) :
        return True
      else :
        return False

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
            return -1, None
        data = json.loads( result.decode('utf-8') )
         
        # error occurs
        if "error" in data :
            if "message" in data :
                print(data["message"])
            else :
                print("Failed to get the data.")
            return -1, None
         
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


class QueryExecutor:
    def __init__(self):
        self.gnavi_caller = GnaviCaller()

    def execute(self, query):
        total, recv_data = self.gnavi_caller.call_api(query)
        print(total)
        self.gnavi_caller.print_data(recv_data)

class TestQueryExecutor:
    def __init__(self):
        self.query_exec = QueryExecutor()
        self.geo_api = GeoCaller()

    def test(self):
        lat, lng, place_name = self.geo_api.call_api("同志社前")
        
        # 範囲
        range     = "1"

        print("searching near " + place_name)
        query = [
          ( "format",       "json" ),
          ( "latitude",     lat    ),
          ( "longitude",    lng    ),
          ( "hit_per_page", 100     ),
          ( "range",        range  )
        ]

        self.query_exec.execute(query)

if __name__ == "__main__":
    # Test
    test_query_exce = TestQueryExecutor()
    test_query_exce.test()
    

