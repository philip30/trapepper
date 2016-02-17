
from trapepper.api import RestaurantAPIManager
from trapepper.lib import Action, ActionType

class ActionDeterminer:
    def determine(self, parsed, last_state):
        print(parsed)
        query_type = parsed["query_type"]
        entities = parsed["entities"]
        raw_tokens = parsed["raw_tokens"]
        
        if query_type == "question":
            api_manager = RestaurantAPIManager(entities)
            api_satisfied, missing_entities = api_manager.are_enough_entities()
            if api_satisfied:
                action = Action(ActionType.exec_hotel, entities)
            else:
                action = Action(ActionType.pardon, missing_entities)
        elif query_type == "hello" or query_type == "bye":
            action = Action(ActionType.dialogue, query_type)
        elif query_type == "":
            action = Action(ActionType.details, entities)


        return action, None


