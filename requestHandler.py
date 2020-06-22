from http.server import BaseHTTPRequestHandler
from nessusAggregator import NessusAggregator
import json

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        aggregator = NessusAggregator()
        res = []

        if self.path.find("allplugins") != -1:
            orderBy = ""
            if self.path.find("orderBy") != -1:
                orderBy = self.path[(self.path.find('orderBy') + len('orderBy') + 1):]
            res = aggregator.getAllPlugins(orderBy)

        elif self.path.find("pluginbyid") != -1:
            if self.path.find("pluginid") != -1:
                pluginID = self.path[(self.path.find("pluginid") + len("pluginid") + 1):]
                res = aggregator.getPluginById(pluginID)
            else:
                res = { "error": "Must provide plugin id!" }

        elif self.path.find("pluginsforcve") != -1:
            if self.path.find("cveid") != -1:
                cveID = self.path[(self.path.find("cveid") + len("cveid") + 1):]
                res = aggregator.getPluginsByCVE(cveID)
            else:
                res = { "error": "Must provide eve id!" }

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(res).encode())
