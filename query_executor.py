from trapepper.api import RestaurantAPIManager
from trapepper.lib import ActionType

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

    def execute_question(self, entities):
        if entities["looking_for"] == "restaurant":
            if entities["location"] == "nearby":
                entities["location"] = "奈良先端科学技術大学院大学"
            return self.execute_restaurant(entities)
        if entities["looking_for"] == "hotel":
            pass

    def execute(self, action):
        if action.action_type == ActionType.exec_hotel:
            return self.execute_question(action.args)

#        if action["query_type"] == "hello":
#            pass
#
#        if action["query_type"] == "bye":
#            pass

        
class TestQueryExecutor:
    def __init__(self):
        self.query_exec = QueryExecutor()
        pass

    def test(self):
        import query_parser
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
    

