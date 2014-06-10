# Required if this project is to be used as Django module

import logging
import json

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden,\
    HttpResponseBadRequest, HttpResponseNotFound, Http404

from jira.config import get_jira
from jira.exceptions import JIRAError

log = logging.getLogger(__name__)

JIRA = get_jira()


def main(request):
    return render_to_response('multiboard.html', RequestContext(request, {}))


def search(request):
    try:
        epic_group_number = request.GET["epicGroupNumber"]
        jql = request.GET["search"]
        callback_name = request.GET["callback"]
    except KeyError:
       return HttpResponseBadRequest("some parameters missing")

    try:
        search_results = JIRA.search_issues(jql, maxResults=500) 
    except JIRAError, e:
        logging.error("Error retrieving results " + str(e))
        search_results = []
    issues_data = [
        (issue.fields.project.key,
        issue.key,
        issue.fields.summary,
        issue.fields.status.name) for issue in search_results
    ]
    return HttpResponse(callback_name + "({result: " + json.dumps(issues_data) + "})")
