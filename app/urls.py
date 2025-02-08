from django.urls import path, include
from app import views

urlpatterns = [
    path("", views.index),
    path("signin", views.sign_in, name="signin"),
    path("signout", views.sign_out, name="signout"),
    path("signup", views.sign_up, name="signup"),
    path("profile", views.profile, name="profile"),
    path("home", views.home, name="home"),
]