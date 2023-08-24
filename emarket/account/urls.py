from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_info/', views.current_user, name='userinfo'),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password/<str:token>', views.reset_password, name="forgot_password")

]