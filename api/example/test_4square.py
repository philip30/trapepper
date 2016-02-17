import httplib, json, sys, time
from collections import OrderedDict

## testing script for place finder w/ Foursquare API

# main constants for query
client_id = "UUZXSZ1G3APJMPPQPLUNO15DLGLDBEDLICCOCIIQTC1B55RQ"
client_secret = "4NTHEKV0CSSEKZS5C1IQABM0LM5VLCO1XQAEUO3EO0TCRGJL"
date = time.strftime("%Y%m%d")

# check arguments
try:
    if len(sys.argv) == 1:
        near = 'nara'
        place = 'ramen'
    elif len(sys.argv) == 2:
        near = sys.argv[1]
    elif len(sys.argv) == 3:
        near = sys.argv[1]
        place = sys.argv[2]
    elif len(sys.argv) == 4:
        near = sys.argv[1]
        place = sys.argv[2]+"%20"+sys.argv[3]
except Exception as e:
    print "Error: too many arguments"

# set other variables
radius = "800"
limit = "7"

# print detail query
print ""
print "Near: "+near+"\nPlace: "+place+"\n"

# connect, request, get response
# using explore function, doc. --> https://developer.foursquare.com/docs/venues/explore
conn = httplib.HTTPSConnection("api.foursquare.com")
conn.request("GET", "/v2/venues/explore?client_id="+client_id+"&client_secret="+client_secret+"&v="+date
                    +"&near="+near+"&query="+place+"&radius="+radius+"&limit="+limit)
response = conn.getresponse()

# read response, parse json response
json_data = response.read()
data = json.loads(json_data, object_pairs_hook=OrderedDict)

# print places' info, json example --> https://developer.foursquare.com/docs/explore#req=venues/explore%3F%26near%3Dnara%26limit%3D7%26radius%3D800%26query%3Dramen
for i in range(0,len(data['response']['groups'][0]['items'])):
    print `i+1`+". Name: "+data['response']['groups'][0]['items'][i]['venue']['name']
    print "   Address: "+data['response']['groups'][0]['items'][i]['venue']['location']['formattedAddress'][0]
    print "   Type: "+data['response']['groups'][0]['items'][i]['venue']['categories'][0]['name']
    #if data['response']['groups'][0]['items'][i]['venue']['rating']:
    #   print "   Rating: "+data['response']['groups'][0]['items'][i]['venue']['rating']
    #print "   Open status: "+data['response']['groups'][0]['items'][i]['venue']['hours']['isOpen']+" ("+data['response']['groups'][0]['items'][i]['venue']['hours']['status']+")"
    #print "   Summary: "+data['response']['groups'][0]['items'][i]['reasons']['items'][0]['summary']
    print ""
