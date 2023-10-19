from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kfsd.apps.endpoints.handlers.common.base import BaseHandler
from kfsd.apps.endpoints.serializers.validations.policy import (
    PolicyModelSerializer,
    PolicyViewModelSerializer,
)
from kfsd.apps.models.tables.validations.policy import Policy
from kfsd.apps.endpoints.handlers.validations.rule import gen_rule_handler
from kfsd.apps.core.utils.dict import DictUtils


def gen_policy_handler(instance):
    handler = PolicyHandler(instance.identifier, False)
    qsData = PolicyModelSerializer(instance=instance)
    handler.setModelQSData(qsData.data)
    handler.setModelQS(instance)
    return handler


@receiver(post_save, sender=Policy)
def process_post_save(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Policy)
def process_post_del(sender, instance, **kwargs):
    pass


class PolicyHandler(BaseHandler):
    RESOURCES = "resources"
    VALUES = "values"

    def __init__(self, policyIdentifier, isDBFetch):
        BaseHandler.__init__(
            self,
            serializer=PolicyModelSerializer,
            viewSerializer=PolicyViewModelSerializer,
            modelClass=Policy,
            identifier=policyIdentifier,
            isDBFetch=isDBFetch,
        )

    def getResourceHandlers(self):
        from kfsd.apps.endpoints.handlers.general.data import gen_data_handler

        return [
            gen_data_handler(resource) for resource in self.getModelQS().resources.all()
        ]

    def addResourcesCtx(self, data):
        resourceHandlers = self.getResourceHandlers()
        for resource in resourceHandlers:
            val = resource.genBody(data)
            var = resource.getSlug()
            data = DictUtils.merge(dict1=data, dict2={self.RESOURCES: {var: val}})

    def getRuleHandlers(self) -> list:
        return [gen_rule_handler(rule) for rule in self.getModelQS().rules.all()]

    def execRules(self, data, debug):
        allValues = []
        allDebug = {}
        for rule in self.getRuleHandlers():
            ruleResp = rule.exec(data, debug)
            values = ruleResp["values"]
            if values and isinstance(values, list):
                allValues += values
            elif values and isinstance(values, str):
                allValues.append(values)

            if debug:
                ruleDebugInfo = DictUtils.filter_by_keys_neg(ruleResp, ["values"])
                allDebug[rule.getIdentifier()] = ruleDebugInfo

        resp = {}
        resp["values"] = allValues
        if debug:
            resp["debug"] = allDebug

        return resp

    def exec(self, data, debug=False):
        input = {"ctx": data}
        self.addResourcesCtx(input)
        return self.execRules(input, debug)
