from django.urls import path
from apps.accounts.views import UserRegisterView, LoginView, LogOutView, UpdateUserView, PasswordResetView, UpdatePasswordView

app_name='accounts'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('update/', UpdateUserView.as_view(), name='update'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('update_password/', UpdatePasswordView.as_view(), name='update_password'),
    ]
