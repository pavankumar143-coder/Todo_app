# from django.conf.urls import include
from .views import SignUpView
from django.urls import path

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),

]

