from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('predict', views.predict,name='predict'),
    path('login', views.login,name='login'),
    path('register', views.register,name='register'),
    path('logout', views.logout,name='register'),
    path('nav', views.nav,name='nav'),
]
