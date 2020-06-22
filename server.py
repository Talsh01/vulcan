from http.server import HTTPServer
from requestHandler import HTTPRequestHandler
from vulners import Vulners
import threading
import json

PORT = 8080

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def loadNessusCollection():
    vulners_api = Vulners(api_key=config["api_key"])
    all_cve = vulners_api.saveCollection(config["vulners_collection_type"])
    print("Collection was loaded")

# load config.json
with open("./conf/config.json") as config_file:
    config = json.load(config_file)

# load the nessus collection from vulners.com periodically
loadNessusCollection()
set_interval(loadNessusCollection, config["get_collection_interval_seconds"])

# serve
httpd = HTTPServer(("localhost", PORT), HTTPRequestHandler)
print("listening on port " + str(PORT))
httpd.serve_forever()