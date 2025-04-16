from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path(
        "create_equipment/",
        views.EquipmentCreateView.as_view(),
        name="create_equipment",
    ),
    # products/
    path("", views.product_catalog, name="product_catalog"),
    # products/1/details/
    path("<int:pk>/details/", views.ProductDetailView.as_view(), name="product_detail"),
    path("<int:pk>/reviews/", views.ReviewCreate.as_view(), name="product_review"),
    path(
        "<int:pk>/reviews/edit/",
        views.ReviewUpdate.as_view(),
        name="product_review_update",
    ),
    path("<int:borrow_request_id>/rent/", views.rent_equipment, name="product_rent"),
    path("<int:borrow_request_id>/deny/", views.deny_equipment, name="product_deny"),

    path("user/<int:pk>/my-products/", views.my_products, name="my_products"),
    path(
        "<int:equipment_id>/requests/",
        views.RequestsView.as_view(),
        name="product_requests",
    ),
    path("<int:pk>/edit/", views.EquipmentUpdateView.as_view(), name="edit_equipment"),
    path("<int:pk>/delete/", views.ProductDetailView.delete_product, name="delete_product"),
    path(
        "<int:pk>/borrow/",
        views.ProductDetailView.request_product,
        name="request_product",
    ),
    path("manage_requests/",
         views.ManageRequests.as_view(),
         name="manage_requests"),
    # products/{productID}
    path("my_rentals/", views.my_rentals, name="my_rentals"),
    path("return/<int:rental_id>/", views.return_rental, name="return_rental"),
]
