# Required if this project is to be used as Django module
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'multi_board_view.views.main', name='main'),
    url(r'^search/', 'multi_board_view.views.search', name='search'),
)
