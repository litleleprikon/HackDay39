from django.conf.urls import url
from todo import views
from HackDay39.urls import method_dispatch

__author__ = 'emilsharifullin'

urlpatterns = [
    url(r'^activities/?',
        method_dispatch(
            GET=views.get_activities_handler)),
    url(r'^activities/link/?',
        method_dispatch(
            POST=views.add_link_handler)),
    url(r'^activities/game/?',
        method_dispatch(
            POST=views.add_game_handler
        ))
    #     method_dispatch(
    #         POST=views.authenticate_handler,
    #         DELETE=views.logout_handler)
    #     )
]
