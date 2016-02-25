import re

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
                print("filter is:")
                print(fit)
                if fit == "price":
                    ret = list(filter(lambda x: len(x["budget"]) != 0, ret))
                    ret = list(sorted(ret, key=lambda x: int(x["budget"]), reverse=(value == "high")))[0:1]
                elif fit == "distance":
                    ret = list(sorted(ret, key=lambda x: int(re.findall("[0-9]+", x["access"]["walk"])[0])))[0:1]
                elif fit == "recom":
                    ret = [ret[0]] # recommendation is the first hit :)
                elif fit == "which":
                    converter = {
                            '一': 0,
                            '二': 1,
                            '三': 2,
                            '四': 3,
                            '五': 4,
                            '六': 5,
                            '七': 6,
                            '八': 7,
                            '九': 8,
                            '十': 9,
                            '0': 0,
                            '1': 1,
                            '2':2,
                            '3':3,
                            '4':4,
                            '5':5,
                            '6':6,
                            '7':7,
                            '8':8,
                            '9':9
                            }
                    print(value[0])
                    print(converter.get(value[0]))
                    ret = [ret[converter.get(value[0])]] #, int(value[0]) - 1)]]
                else:
                    raise NotImplementedError
        print(len(ret))
        return ret, ret == self.data
