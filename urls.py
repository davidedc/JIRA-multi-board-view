# Required if this project is to be used as Django module
from django.conf.urls import patterns, include, url
import os

urlpatterns = patterns('',
    url(r'^$', 'JIRA_multi_board_view.views.main', name='main'),
    url(r'^search/', 'JIRA_multi_board_view.views.search', name='search'),
    url(r'^config.coffee', 'JIRA_multi_board_view.views.config', name='config'),
	url(r'^(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.dirname(os.path.realpath(__file__))}),
)
