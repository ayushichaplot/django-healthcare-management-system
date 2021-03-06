"""Healthcare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from healthcare_app.views import views_state, views_city
#from ..healthcare_app.views import views_city, views_state

urlpatterns = [
    path('admin/', admin.site.urls),
    url(
        r'^api/v1/states/$',
        views_state.state_list,
        name='state_list'
    ),
    url(
        r'^api/v1/states/(?P<id>[0-9]+)$',
        views_state.state_detail,
        name='state_detail'
    ),

    url(
        r'^api/v1/cities/$',
        views_city.city_list,
        name='city_list'
    ),
    url(
        r'^api/v1/cities/(?P<id>[0-9]+)$',
        views_city.city_detail,
        name='city_detail'
    ),
]
