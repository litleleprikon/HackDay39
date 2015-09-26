from django.conf.urls import url
from auth import views
from HackDay39.urls import method_dispatch

__author__ = 'emilsharifullin'

urlpatterns = [
    url(r'^user/',
        method_dispatch(
            POST=views.new_user_handler)),
    url(r'',
        method_dispatch(
            POST=views.authenticate_handler,
            DELETE=views.logout_handler)
        )
]
