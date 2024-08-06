from django.urls import path
from user import views

urlpatterns = [
    # ... other urls
    path('filter/dept/', views.load_departments, name='filter_dept'),
]
