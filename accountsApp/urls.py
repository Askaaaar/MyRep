from django.urls import path
from .views import AccountsCreateView

urlpatterns = [
    path('registration/', AccountsCreateView.as_view(), name='registration'),
]