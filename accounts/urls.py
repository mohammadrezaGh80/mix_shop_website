from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # Login & Logout
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),

    # Registration
    path("register/", views.RegisterStepOneView.as_view(), name="register_step_one"),
    path("register/next/", views.RegisterStepTwoView.as_view(), name="register_step_two"),

    # Activation account
    path("activation/<str:uid>/<str:token>/", views.ActivationAccountView.as_view(), name="activation_account"),
    path("activation/resend/", views.ActivationAccountResendView.as_view(), name="activation_account_resend"),

    # Password Reset an account
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/<str:uid>/<str:token>/", views.CustomPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    # Password Change an account
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
]
