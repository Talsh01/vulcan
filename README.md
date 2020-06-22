# Nessus DB REST API

Downloads the nessus DB from vulners.com and stores in MongoDB.
The DB gets refreshed periodically and overrides the existing data.

## Run Server

Install the required python libraries using the command:

$ pip install -r requirements.txt

Run server by running the command:

$ python server.py

## API

### Get all Nessus plugins

Get all nessus plugins that are saved in DB. orderBy is optional and can be any of [pluginID, published, score].

> http://localhost:8080/allplugins?orderBy=xxx

### Get by pluginID

Get nessus plugins by plugin ID. pluginid must be provided.

> http://localhost:8080/pluginbyid?pluginid=xxx

### Get all Nessus plugins that affect a specific CVE

Get nessus plugins by CVE ID. cveid must be provided.

> http://localhost:8080/pluginsforcve?cveid=xxx
