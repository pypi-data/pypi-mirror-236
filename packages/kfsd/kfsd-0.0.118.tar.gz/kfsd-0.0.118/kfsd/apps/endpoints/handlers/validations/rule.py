from functools import reduce
import operator

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.validations.rule import (
    RuleModelSerializer,
    RuleViewModelSerializer,
)

from kfsd.apps.models.tables.validations.rule import Rule

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.attr import AttrUtils
from kfsd.apps.core.utils.arr import ArrUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def gen_rule_handler(instance):
    handler = RuleHandler(instance.identifier, False)
    qsData = RuleModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Rule)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Rule)
def process_post_del(sender, instance, **kwargs):
    pass


def intersection(arr1, arr2):
    if ArrUtils.intersection(arr1, arr2):
        return True
    return False


class RuleHandler(BaseHandler):
    EXPR = "expr"
    ALLOF = "allOf"
    ANYOF = "anyOf"
    VAR = "var"
    VALUES = "values"
    CTX = "ctx"
    KEYPATH = "keypath"

    def __init__(self, ruleIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=RuleModelSerializer,
            viewSerializer=RuleViewModelSerializer,
            modelClass=Rule,
            identifier=ruleIdentifier,
            isDBFetch=isDBFetch,
        )
        self.__errors = []
        self.__traces = {}

    def getExpr(self):
        return DictUtils.get(self.getModelQSData(), self.EXPR)

    def getAllOf(self):
        return DictUtils.get(self.getModelQSData(), self.ALLOF)

    def getAnyOf(self):
        return DictUtils.get(self.getModelQSData(), self.ANYOF)

    def getType(self):
        return DictUtils.get(self.getModelQSData(), "type")

    def getPrefetch(self):
        return DictUtils.get(self.getModelQSData(), "prefetch", [])

    def setRaw(self, data):
        self.__raw = data

    def getRaw(self):
        return self.__raw

    def getErrors(self):
        return self.__errors

    def getTraces(self):
        return self.__traces

    def processRuleByType(self, rule):
        if self.EXPR in rule and DictUtils.get(rule, self.EXPR):
            return self.ruleExpr(DictUtils.get(rule, self.EXPR))
        elif self.ALLOF in rule and DictUtils.get(rule, self.ALLOF):
            return self.ruleAllOf(DictUtils.get(rule, self.ALLOF))
        elif self.ANYOF in rule and DictUtils.get(rule, self.ANYOF):
            return self.ruleAnyOf(DictUtils.get(rule, self.ANYOF))
        return False

    def ruleAnyOf(self, anyOf):
        return reduce(operator.or_, (self.processRuleByType(rule) for rule in anyOf))

    def ruleAllOf(self, allOf):
        return reduce(operator.and_, (self.processRuleByType(rule) for rule in allOf))

    def ruleExpr(self, expr, default=False):
        result = default
        request = AttrUtils.format_dict(self.__raw)  # noqa: F841
        input = self.__raw  # noqa: F841
        try:
            result = eval(expr)
        except Exception as e:
            extnError = ""
            if isinstance(e, KeyError):
                extnError = "not found"
            self.__errors.append(
                "exception while executing expr: '{}', error: {} {}".format(
                    expr, e.args[0], extnError
                )
            )
        self.__traces[expr] = result
        return result

    def evaluate(self):
        effect = None
        rule = self.getModelQSData()
        if DictUtils.get(rule, self.VALUES) and self.processRuleByType(rule):
            return rule.pop(self.VALUES)
        return effect

    def genCtx(self, step):
        var = DictUtils.get(step, self.VAR)
        val = self.processRuleByType(step)
        return var, val

    def genCtxAll(self):
        for value in self.getPrefetch():
            var, val = self.genCtx(value)
            self.__raw[self.CTX] = DictUtils.merge(
                dict1=DictUtils.get(self.__raw, self.CTX, {}), dict2={var: val}
            )

    def exec(self, data, debug=False):
        self.setRaw(data)
        self.genCtxAll()
        values = self.evaluate()
        resp = {}
        resp["values"] = values
        if debug:
            resp["input"] = self.__raw
            resp["errors"] = self.__errors
            resp["trace"] = self.__traces
        return resp
