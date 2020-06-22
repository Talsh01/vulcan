import json
import requests
from io import BytesIO
from zipfile import ZipFile
from pymongo import MongoClient

class Vulners(object):

    # load config.json
    with open("./conf/config.json") as config_file:
        config = json.load(config_file)

    mongoclient = MongoClient(config["mongo_connection_string"])

    def __init__(self, api_key):

        # Requests opener. If persistent option is active - try to load
        self.__opener = requests.session()

        # api key validation
        if not api_key:
            raise ValueError("Must provide API key!")

        self.__api_key = api_key

    def saveCollection(self, collection):

        datefrom = self.config["datefrom"]
        dateto = self.config["dateto"]

        # define params
        json_parameters = { "type": collection, "datefrom": datefrom, "dateto": dateto }
        if self.__api_key:
            json_parameters["apiKey"] = self.__api_key

        # make request to vulners
        vulnersCollectionUrl = self.config["vulners_hostname"] + self.config["vulners_collections_endpoint"]
        response = self.__opener.get(vulnersCollectionUrl, params=json_parameters)
        zipped_json = response.content

        # unzip to json and save results
        with ZipFile(BytesIO(zipped_json)) as zip_file:
            file_name = zip_file.namelist()[0]
            collection = json.loads(zip_file.open(file_name).read())
            self.saveToMongo(collection)
            return collection

    def saveToMongo(self, collection):

        # insert to MongoDB

        col = self.mongoclient[self.config["mongo_db_name"]].get_collection(self.config["vulners_collection_type"])

        for entry in collection:
            entry["_id"] = entry.pop("id")
            col.replace_one({ "_id": entry["_id"] }, entry, upsert=True)
