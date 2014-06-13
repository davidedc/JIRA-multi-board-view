
# Usage:
#  python vizit portNumber jiraServerURL login password
#  then go to http://localhost:portNumber/index.html

# for the server part
import SocketServer
import SimpleHTTPServer
import urllib
from urlparse import urlparse

# for grokking the arguments coming from the command line
import sys

# for sending the results as JSON to the page
import json

# some objects returnes from the API are
# too complicated for simple json serialisation
# this library sorts that out.
import jsonpickle

# to access JIRA
from jira.client import JIRA

PORT = int(sys.argv[1])


# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
# Override this with the options parameter.
options = {
	'server': sys.argv[2]
}

jira = JIRA(options, basic_auth=(sys.argv[3], sys.argv[4]))



class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		theFile = self.path
		theFile = theFile[1:] # first character is a slash, we take that away
		print "requested ", self.path

		u =urlparse(self.path)
		print "parsed URL: " + str(u)

		try:
			args = dict([x.split("=") for x in u.query.split("&")])
			search = args.get("search","=")
			search = urllib.unquote(search).replace("+", " ")
		except ValueError:
			search = 'no Search'


		print "received search ", search


		if "favicon" in theFile:
			print ""
		elif "search" in theFile:
			# extract the callback name
			callbackName = theFile.split("?callback=",1)[1].split("&",1)[0]

			#This URL will trigger our sample function and send what it returns back to the browser
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()

			searchResults = jira.search_issues(search, maxResults=1000)
			issuesData = [[ issue.fields.project.key, issue.key, issue.fields.summary, issue.fields.status.name, issue.fields.issuelinks] for issue in searchResults]

			#print "issue.fields.issuelinks: " + jsonpickle.encode(issue.fields.issuelinks)

			JSONOfIssues = jsonpickle.encode(issuesData)

			print "json: " +  JSONOfIssues

			self.wfile.write(callbackName + "({result: " + JSONOfIssues + "})")

		elif ".html" in theFile or ".coffee" or ".gif" in theFile:
			# next three lines only needed for Firefox
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.copyfile(urllib.urlopen(theFile), self.wfile)
		else:
			# send empty response
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("")

httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()