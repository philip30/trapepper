from trapepper.api import RestaurantAPIManager
from trapepper.lib import Action, ActionType
from trapepper.util import log

from enum import Enum

State = Enum("Enum", "init expect search")

def merge_entity(last_state, entities):
    for key, value in entities.items():
        if type(value) == dict:
            if type(last_state[key]) != dict:
                last_state[key] = {}
            merge_entity(last_state[key], value)
        else:
            last_state[key] = value

def different_location(last_state, parsed):
    try:
        if last_state is None: return True
        return last_state["entities"]["location"] != parsed["entities"]["location"]
    except:
        return True

class ActionDeterminer:
    def determine(self, parsed, last_state):
        
        query_type = parsed["query_type"]
        entities = parsed["entities"]
        raw_tokens = parsed["raw_tokens"]
        
        # Entity merging
        if last_state is not None:
            if query_type == "pardon":
                if last_state["STATE"] == State.init or last_state["STATE"] == State.expect:
                    query_type = "question"
            else:
                last_state["query_type"] = parsed["query_type"]

            merge_entity(last_state["entities"], parsed["entities"])
            entities = last_state["entities"]
        else:
            last_state = parsed
            last_state["STATE"] = State.init

        # updating state
        last_state["raw_tokens"] = raw_tokens

        if query_type == "question":
            if entities["question"] == "is_there":
                if last_state["STATE"] != State.search or different_location(last_state, parsed):
                    # Trying to query
                    api_manager = RestaurantAPIManager(entities)
                    api_satisfied, missing_entities = api_manager.are_enough_entities()
                
                    # If queries are OK, then execute
                    if api_satisfied:
                        last_state["STATE"] = State.search
                        action = Action(ActionType.exec_rest, entities)
                    else:
                        last_state["STATE"] = State.expect
                        action = Action(ActionType.pardon, missing_entities)
                else:
                    # TODO
#                    print(last_state)
#                    print(entities)
#                    action = Action(ActionType.pardon, "location")
                     raise NotImplementedError()
            elif entities["question"] == "how":
                # Route
                if last_state["STATE"] == State.search:
                    action = Action(ActionType.route)
                else:
                    action = Action(ActionType.pardon, "location")
            else:
                raise NotImplementedError()

        elif query_type == "hello" or query_type == "bye":
            if query_type == "bye":
                last_state = None
            action = Action(ActionType.dialogue, query_type)
        else:
            if last_state["STATE"] == State.search:
                action = Action(ActionType.explain)
            else:
                action = Action(ActionType.pardon)
        return action, last_state

