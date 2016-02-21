from trapepper.api import RestaurantAPIManager
from trapepper.lib import Action, ActionType
from trapepper.util import log

def merge_entitiy(last_state, entities):
    for key, value in entities.items():
        last_state[key] = value

class ActionDeterminer:
    def determine(self, parsed, last_state):
        query_type = parsed["query_type"]
        entities = parsed["entities"]
        raw_tokens = parsed["raw_tokens"]
        expecting_details = last_state is not None

        if expecting_details and query_type == "pardon":
            query_type = last_state["query_type"]
            merge_entitiy(last_state["entities"], entities)
           

        if query_type == "question":
            if entities["question"] == "is_there":
                # Trying to query
                api_manager = RestaurantAPIManager(entities)
                api_satisfied, missing_entities = api_manager.are_enough_entities()
            
                # If queries are OK, then execute
                if api_satisfied:
                    action = Action(ActionType.exec_hotel, entities)
                else:
                    action = Action(ActionType.pardon, missing_entities)
            elif entities["question"] == "how":
                # Route
                if "original_result" in last_state:
                    action = Action(ActionType.route)
                else:
                    action = Action(ActionType.pardon, "location")
            else:
                raise NotImplementedError()


            # saving a new state
            if last_state is None:
                last_state = parsed
        elif query_type == "hello" or query_type == "bye":
            if query_type == "bye":
                last_state = None
            action = Action(ActionType.dialogue, query_type)
        elif query_type == "details":
            action = Action(ActionType.details, entities)
        else:
            action = Action(ActionType.pardon, "")
        return action, last_state


