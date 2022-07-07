"""mytrip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from atexit import register
from django.contrib import admin
from django.urls import path
from webapp.views import sign_in, welcome, registerPage, user_interests, home, create_trip, logoutUser, view_event, current_trip
#from webapp.views import home, create_account, loginPage, registerPage
#from webapp.views import registerPage, create_trip, user_interests
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"), #need to give the path a name so we can redirect without having to render the template each time
    # path('create-account', create_account),
    # path('login', loginPage, name="login"),
    path('register', registerPage, name="register"),
    path('sign-in', sign_in, name="sign-in"),
    path('logout', logoutUser, name="logout"),
    path('event/<int:id>', view_event, name="view_event"),
    path('create-trip', create_trip, name="create-trip"),
    path('user-interests', user_interests, name="user-interests"),
    path('current-trip', current_trip, name="current-trip"),
    path('welcome', welcome, name="welcome")

    
]
