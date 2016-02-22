
from trapepper.lib import ActionType
from trapepper.util import log

# DIALOGS
def count_restaurant(data):
    count = len(data["recv"]["rest"])
    if count > 1:
        response_str = str(count) + "件のレストランがあります"
    else:
        response_str = "ないですね"
    return response_str

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

def restaurant_alternate_route(wtg, rest, access):
    if len(wtg) == 0:
        return way_to_restaurant(rest, False)
    else:
        ret = []
        for i, acc in enumerate(wtg):
            if i != 0:
                ret.append("他の行き方としては")
            if acc == "line":
                ret.append(access["line"] + "という電車がありますのでご乗車ください")
            elif acc == "station":
                ret.append(access["station"] + "という駅が最寄りにあります")
            elif acc == "walk":
                ret.append("歩く場合は最寄りの駅から" + str(access["walk"]) + "分で着きます")
        return ret

# ROUTINES
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
    return len(data["recv"]["rest"]) == 0

def select_route(data):
    data = data["recv"]["rest"][0:1]
    if len(data) != 1:
        return which_one()
    else:
        rest = data[0]
        ret  = []
        if "access" in rest:
            access = rest["access"]
            ret.append(way_to_restaurant(rest, True))
            way_to_go = []
            if "line" in access: way_to_go.append("line")
            if "station" in access: way_to_go.append("station")
            if "walk" in access: way_to_go.append("walk")
            add_response(ret, restaurant_alternate_route(way_to_go, rest, access))
        else:
            ret.append(way_to_restaurant(rest, False))
        return ret
            
# ret
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
        elif action.action_type == ActionType.route:
            say(select_route(data))
        else:
            raise NotImplementedError()
        return responses

