
from trapepper.lib import ActionType
from trapepper.util import log

MAX_SHOW = 3

# State modification depending of which response being said 
# i.e. STATE is a object returned by query_parser
STATE = None

# DIALOGS
def count_restaurant(data, filt):
    ret = []
    count = len(data)
    if count > 0:
        ret.append(str(count) + "件のレストランがあります")
        if count > MAX_SHOW:
            # TODO
            ret.append(which_one())
        else:
            add_response(ret, describe_restaurant(data, filt))
    else:
        ret.append("ないですね")
    return ret

def describe_restaurant(data, filt):
    ret = []
    for i, rest in enumerate(data):
        ret.extend(describe_single_restaurant(rest, filt, i+1, len(data) == 1))
    return ret

def describe_single_restaurant(rest, filt=None, number=0, describe_route=False):
    ret = []
    if number != 0:
        restaurant_type = extract_category(rest)
        restaurant_type = "" if not restaurant_type else ("a " + restaurant_type)
        restaurant_name = str(rest["name"])
        rest_str = restaurant_name + "についてご案内します。"
        if filt is not None:
            if "price" in filt:
                rest_str += "大体" + rest["budget"] + "円ほどでお食事が楽しめます。"
            if "distance" in filt:
                rest_str += "徒歩" + rest["access"]["walk"] + "分ほどで着きますよ。"
        rest_str += "."
        ret.append(rest_str)
        add_response(ret, restaurant_alternate_route(rest, rest['access']))
    return ret

def ask_more_entity(action):
    missing_entity = action.args.strip()
    if missing_entity == "location":
        return "どのあたりにあるレストランがご希望ですか"
    else:
        raise NotImplementedError()

def pardon():
    return "すみません。もう少し希望を述べていただけますか？"

def no_matching_restaurant():
    return "ないですね"

def which_one():
    return "どのレストランに行きたいですか？"

def way_to_restaurant(rest, route_found):
    if route_found:
        return rest["name"] + "へ行く道のりです。"
    else:
        return rest["name"] + "へ行く道のりのご案内はできません。ごめんなさい。"

def restaurant_alternate_route(rest, access):
    accessible = lambda x: x in access and len(access[x]) != 0
    wtg = []
    if accessible("line"): wtg.append("line")
    if accessible("station"): wtg.append("station")
    if accessible("walk"): wtg.append("walk")
    if len(wtg) == 0:
        return way_to_restaurant(rest, False)
    else:
        ret = []
        ret.append(way_to_restaurant(rest, True))
        for i, acc in enumerate(wtg):
            # if i != 0:
            #     ret.append("他の行き方としては")
            if acc == "line":
                ret.append(access["line"] + "という電車がありますのでご乗車ください")
            elif acc == "station" and not access.get("line"):
                ret.append(access["station"] + "という駅が最寄りにあります")
            elif acc == "walk":
                ret.append("歩く場合は最寄りの駅から" + str(access["walk"]) + "分で着きます")
        return ret

# ROUTINES
def extract_category(rest):
    code_category_name_s = []
    if "code" in rest and "category_name_s" in rest["code"] :
        for category_name_s in rest["code"]["category_name_s"] :
            code_category_name_s.append( category_name_s )
    if len(code_category_name_s) != 0:
        return code_category_name_s[0] # return the first category # TODO is this correct?
    else:
        return None

def to_number_str(number):
    # TODO    
    numbers = "first second third"
    numbers = {i+1: num_str for i, num_str in enumerate(numbers.split())}
    return numbers[number]

def add_response(response, data):
    if type(data) == str:
        response.append(data)
    elif type(data) == list or type(data) == tuple:
        response.extend(data)
    else:
        response.append(data)

def casual_chat(dialog):
    if dialog == "hello":
        return "こんにちは。"
    elif dialog == "bye":
        return "バイバイ。"
    else:
        return "そうなんですか？"

def is_missing_entity(action):
    return action.args is not None and len(action.args) > 0

def is_restaurant_empty(data):
    return len(data) == 0

def select_route(data):
    if len(data) != 1:
        return which_one()
    else:
        rest = data[0]
        ret  = []
        if "access" in rest:
            access = rest["access"]
            
            add_response(ret, restaurant_alternate_route(rest, access))
        else:
            ret.append(way_to_restaurant(rest, False))
        return ret
            
# ret
class ResponseGenerator:
    def generate_response(self, action, data, filt):
        global STATE
        STATE = data
        responses = []
        say = lambda x: add_response(responses, x)
        if action.action_type == ActionType.pardon:
            if is_missing_entity(action):
                say(ask_more_entity(action))
            else:
                say(pardon())
        elif action.action_type == ActionType.exec_rest or action.action_type == ActionType.explain:
            # Restaurant count
            if is_restaurant_empty(data):
                say(no_matching_restaurant())
            else:
                say(count_restaurant(data, filt))
        elif action.action_type == ActionType.dialogue:
            say(casual_chat(action.args))
        elif action.action_type == ActionType.route:
            say(select_route(data))
        else:
            raise NotImplementedError()
        return responses

