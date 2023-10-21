from kfsd.apps.core.utils.dict import DictUtils


class Transform:
    KEYPATH = "keypath"
    EXPR = "expr"

    def __init__(self, rules, data):
        self.__rules = rules
        self.__data = data

    def exec(self):
        for rule in self.__rules:
            keys = rule[self.KEYPATH].split(".")
            val = rule[self.EXPR]
            newValDict = DictUtils.create_hierarchy(keys, val)
            self.__data = DictUtils.merge(self.__data, newValDict)
        return self.__data
