from rest_framework import serializers

from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.models.tables.relations.relation import Relation
from kfsd.apps.endpoints.serializers.model import BaseModelSerializer


class RelationViewModelSerializer(BaseModelSerializer):
    id = None
    created = None
    updated = None
    slug = None
    target = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=HRel.objects.all(),
    )
    source = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=HRel.objects.all(),
    )

    class Meta:
        model = Relation
        exclude = (
            "id",
            "created",
            "updated",
        )
