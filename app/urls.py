from django.urls import path, include
from app import views

urlpatterns = [
    path("", views.index),
    path("signin", views.sign_in, name="signin"),
    path("sign-out", views.sign_out, name="sign-out"),
    path("signup", views.sign_up, name="signup"),
]