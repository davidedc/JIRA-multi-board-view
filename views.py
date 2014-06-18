# Required if this project is to be used as Django module

import logging
import json

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden,\
    HttpResponseBadRequest, HttpResponseNotFound, Http404
from django.conf import settings

from jira.config import get_jira
from jira.exceptions import JIRAError

from jira_analysis.JIRA_multi_board_view.models import BoardDefinition, EpicDefinition

log = logging.getLogger(__name__)

JIRA = get_jira()


def main(request):
    return render_to_response('multiboard.html', RequestContext(request, {}))


def search(request):
    try:
        jql = request.GET["search"]
        callback_name = request.GET["callback"]
    except KeyError:
       return HttpResponseBadRequest("some parameters missing")
    try:
        search_results = JIRA.search_issues(jql, fields="project,summary,status,issuelinks", maxResults=500) 
    except JIRAError, e:
        logging.error("Error retrieving results " + str(e))
        search_results = []
    issues_data = [(
        issue.fields.project.key,
        issue.key,
        issue.fields.summary,
        issue.fields.status.name,
        [
            {
                'type':{
                    'inward':issuelink.type.inward,
                    'outward':issuelink.type.outward,
                },
                'inwardIssue':{
                    'key':issuelink.inwardIssue.key,
                } if hasattr(issuelink,'inwardIssue') else None,
                'outwardIssue':{
                    'key':issuelink.outwardIssue.key,
                } if hasattr(issuelink, 'outwardIssue') else None, 
            } for issuelink in issue.fields.issuelinks
        ]
    ) for issue in search_results]
    return HttpResponse(callback_name + "({result: " + json.dumps(issues_data) + "})")


def config(request):
    config = ""
    for epic in EpicDefinition.objects.all():
        config += "epicGroupsWithQuery.push ['{0}', '{1}']\n".format(epic.name, epic.jql)
    for board in BoardDefinition.objects.all():
        config += "boardNames.push '{0}'\n".format(board.name)
        config += "boardQueries.push '{0}'\n".format(board.jql)
        config += "groupedStatuses.push ["
        for column in board.statuses.split('|'):
            config += "["
            for status in column.split(','):
                config += "'{0}',".format(status.strip())
            config += "],"
        config += "]\n"
    return HttpResponse(config, "text/coffeescript")

