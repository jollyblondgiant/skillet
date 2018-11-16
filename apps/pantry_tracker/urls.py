from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^skillet$',views.index),
    url(r'register$', views.register),
    url(r'dashboard$', views.dashboard),
    url(r'login$', views.login),
    url(r'logout$', views.logout)
]