from django.urls import path, include
from rest_framework import routers

from kfsd.apps.endpoints.views.relations.hrel import HRelModelViewSet
from kfsd.apps.endpoints.views.relations.relation import RelationModelViewSet
from kfsd.apps.endpoints.views.relations.hierarchy import HierarchyModelViewSet
from kfsd.apps.endpoints.views.relations.hierarchy_init import HierarchyInitModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("relations/hrel", HRelModelViewSet, basename="hrel")
router.register("relations/relation", RelationModelViewSet, basename="relation")
router.register("relations/hierarchy", HierarchyModelViewSet, basename="hierarchy")
router.register(
    "relations/hierarchy_init", HierarchyInitModelViewSet, basename="hierarchy_init"
)

urlpatterns = [
    path("", include(router.urls)),
]
