from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/', views.VerifyCodeRegisterView.as_view(), name='verify_code'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # profile user
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change/profile/', views.ChangeProfile.as_view(), name='change_profile'),
    path('change/date-of-birth/', views.ChangeDateBirth.as_view(), name='change_birth'),
    path('change/password/', views.ChangePasswordView.as_view(), name='change_password'),
    # this part for forget password
    path('forget/password/', views.ForgetPasswordView.as_view(), name='forget_password'),
    path('verify/password/', views.VerifyCodePasswordView.as_view(), name='verify_password'),
    path('create/password/', views.CreateNewPasswordView.as_view(), name='create_password'),

]
