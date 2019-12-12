from django.urls import include, path
from django.conf.urls import url
from django.views.generic import TemplateView
from allauth.account.views import confirm_email
from . import views
from rest_auth.registration import urls
from .views import ConfirmAPIView
urlpatterns = [
    path('me/', views.MyAccountView.as_view()),
    path('auth/', include('rest_auth.urls')),
    path('auth/register/account-confirmation-sent/',
         TemplateView.as_view(template_name='account/email_confirmation_sent.html'),
         name='account_email_verification_sent'
    ),
    path('auth/register/account-confirm-email/<str:key>/',
         confirm_email,
         name='account_confirm_email'),
    path('auth/register/', include('rest_auth.registration.urls')),
    #path('login/', ConfirmAPIView.as_view(), name='confirm_login'),
    url(r"^login/$", views.confirm_login, name='confirm_login')
]
