
class ResultFilterer:
    
    def __init__(self):
        self.data = []

    def reset(self, data):
        self.data = data["recv"]["rest"]

    def filter(self, state):
        if len(self.data) == 0 or state is None:
            return self.data, False
        
        ret = [x for x in self.data]
        if "filter" in state["entities"] and type(state["entities"]["filter"]) == dict:
            for fit, value in state["entities"]["filter"].items():
                if fit == "price":
                    ret = list(filter(lambda x: len(x["budget"]) != 0, ret))
                    ret = list(sorted(ret, key=lambda x: int(x["budget"]), reverse=(value == "high")))[0:1]
                elif fit == "distance":
                    ret = list(sorted(ret, key=lambda x: int(x["access"]["walk"])))[0:1]
                elif fit == "recom":
                    ret = [x[0]] # recommendation is the first hit :)
                else:
                    raise NotImplementedError
        
        return ret, ret == self.data
