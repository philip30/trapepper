
from enum import Enum

ActionType = Enum("ActionType", "exec_rest explain dialogue pardon route filter")

class Action:
    def __init__(self, action_type, args=""):
        self.action_type = action_type
        self.args = args

    def __str__(self):
        return str(self.action_type) + ": " + str(self.args)

