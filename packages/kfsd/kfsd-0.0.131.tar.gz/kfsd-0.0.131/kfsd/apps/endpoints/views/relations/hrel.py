from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.relations.hrel import HRel
from kfsd.apps.endpoints.serializers.relations.hrel import (
    HRelViewModelSerializer,
)
from kfsd.apps.endpoints.views.relations.docs.hrel import HRelDoc


@extend_schema_view(**HRelDoc.modelviewset())
class HRelModelViewSet(CustomModelViewSet):
    queryset = HRel.objects.all()
    serializer_class = HRelViewModelSerializer
