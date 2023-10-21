from rest_framework import serializers

from kfsd.apps.endpoints.handlers.signals.inbound import InboundHandler
from kfsd.apps.endpoints.handlers.signals.outbound import OutboundHandler


class ClearTblInputReqSerializer(serializers.Serializer):
    tbl = serializers.ChoiceField(choices=["INBOUND", "OUTBOUND"])

    def exec(self, validated_data):
        op = validated_data.get("tbl", None)
        if op == "INBOUND":
            return InboundHandler.clear()
        elif op == "OUTBOUND":
            return OutboundHandler.clear()
