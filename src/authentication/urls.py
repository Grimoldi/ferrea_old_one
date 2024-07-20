
from django.urls import path
from authentication.views import AuthenticateUser

urlpatterns = [
    path('authenticate', AuthenticateUser.as_view(), name='authenticate'),

]
