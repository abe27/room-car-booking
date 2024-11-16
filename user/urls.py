from django.urls import path
from user import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... other urls
    path('filter/dept/', views.load_departments, name='filter_dept'),
    path('admin/password_reset/<int:pk>/', auth_views.PasswordChangeView.as_view(), name='admin_user_password_change'),
    path('update-user-status/', views.update_user_status, name='update_user_status'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
