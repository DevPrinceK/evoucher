from django.urls import path
from . import views

# authentication
urlpatterns = [
    # API Overview
    path("", views.OverviewAPI.as_view(), name="api-overview"),
    # signup a new user
    path('sign-up/', views.SignUpAPI.as_view(), name="sign_up"),
    # login users
    path('login/', views.LoginAPI.as_view(), name="login"),
]

urlpatterns += [
    # Gets all events created by user
    path("all-events/", views.EventListAPI.as_view(), name="all_events"),
    # create, update, delete event
    path("cud-event/", views.CUDEventAPI.as_view(), name="cud_events"),
]
