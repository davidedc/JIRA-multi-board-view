# Required if this project is to be used as Django module
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'JIRA_multi_board_view.views.main', name='main'),
    url(r'^search/', 'JIRA_multi_board_view.views.search', name='search'),
    url(r'^config.coffee', 'JIRA_multi_board_view.views.config', name='config'),
)
