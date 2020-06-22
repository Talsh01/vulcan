from pymongo import MongoClient
import json

class NessusAggregator():

    def __init__(self):

        # load config.json
        with open("./conf/config.json") as config_file:
            config = json.load(config_file)

        # connect to mongo and init collection
        mongoclient = MongoClient(config["mongo_connection_string"])
        self.nessusCollection = mongoclient[config["mongo_db_name"]].get_collection(config["vulners_collection_type"])

    def getAllPlugins(self, orderBy):

        if orderBy != "score":
            orderBy = "_source." + orderBy

        plugins = self.nessusCollection.aggregate([
            { '$sort':  { orderBy: 1 } }
        ])

        pluginsList = []

        for plugin in plugins:
            pluginsList.append({
                'pluginID': plugin['_source']['pluginID'],
                'published': plugin['_source']['published'],
                'title': plugin['_source']['title'],
                'cvelist': plugin['_source']['cvelist'],
                'score': plugin['score']
            })

        return pluginsList

    def getPluginById(self, pluginID):
        plugins = self.nessusCollection.find( { "_source.pluginID": pluginID } )

        for plugin in plugins:
            return plugin

    def getPluginsByCVE(self, cveID):
        plugins = self.nessusCollection.find(
            { "_source.cvelist": { '$exists': 'true', '$in': [cveID] } }
        )

        pluginsList = []

        for plugin in plugins:
            pluginsList.append({
                'pluginID': plugin['_source']['pluginID'],
                'published': plugin['_source']['published'],
                'title': plugin['_source']['title'],
                'score': plugin['score']
            })

        return pluginsList

