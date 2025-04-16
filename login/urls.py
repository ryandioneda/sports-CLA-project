from django.urls import path

from . import views

app_name = "login"

urlpatterns = [
    path("", views.index, name="index"),
    path('profile/', views.profile,  name="profile"),
    path("logout", views.logout_view),
]
