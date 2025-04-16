from django.urls import path

from . import views

app_name = "productCollections"

urlpatterns = [
    path(
        "make_collections/",
        views.MakeCollectionsCreateView.as_view(),
        name="make_collections",
    ),
    path("view_collections/", views.collection_catalog, name="view_collections"),
    path("my_collections/", views.my_collections, name="my_collections"),
    path(
        "edit_collection/<int:collection_id>/",
        views.edit_collection,
        name="edit_collection",
    ),
    path(
        "view_collection/<int:collection_id>/",
        views.view_collection,
        name="view_collection",
    ),
    path(
        "manage_collection_requests/",
        views.ManageCollectionRequests.as_view(),
        name="manage_collection_requests",
    ),
    path(
        "<int:collection_request_id>/approve/",
        views.approve_collection,
        name="collection_approve",
    ),
    path(
        "<int:collection_request_id>/deny/",
        views.deny_collection,
        name="collection_deny",
    ),
]
