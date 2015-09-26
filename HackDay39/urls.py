"""HackDay39 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseNotAllowed


def method_dispatch(**table):
    def invalid_method(request, *args, **kwargs):
        # logger.warning('Method Not Allowed (%s): %s', request.method, request.path,
        #     extra={
        #         'status_code': 405,
        #         'request': request
        #     }
        # )
        return HttpResponseNotAllowed(table.keys())

    def d(request, *args, **kwargs):
        handler = table.get(request.method, invalid_method)
        return handler(request, *args, **kwargs)
    return d

urlpatterns = [
    url(r'^api/admin/', include(admin.site.urls)),
    url(r'^api/auth/', include('auth.urls')),
]
