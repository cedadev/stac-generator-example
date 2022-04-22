# encoding: utf-8
"""
STAC API collection summaries updater
-------------

Update a collection summaries from the Queryables of the collection itself.
"""
__author__ = "Mathieu Provencher"
__date__ = "20 Apr 2022"
__copyright__ = "Copyright 2022 Computer Research Institute of Montréal"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "mathieu.provencher@crim.ca"

import requests
import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class StacApiCollectionSummariesUpdater():
    """
    Update a collection summaries from the Queryables of the collection itself.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        collection_id = "c604ffb6d610adbb9a6b4787db7b8fd7"
        stac_host = "http://127.0.0.1:8000/"

        stac_collection = self.get_stac_collection(stac_host, collection_id)
        stac_collection_queryables = self.get_stac_collection_queryables(stac_host, collection_id)
        stac_collection = self.update_stac_collection(stac_collection, stac_collection_queryables)
        self.post_collection(stac_host, stac_collection)

    def get_stac_collection(self, stac_host, collection_id):
        """
        Get a STAC collection

        Returns the collection JSON.
        """
        r = requests.get(os.path.join(stac_host, "collections", collection_id))

        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()

        return {}

    def get_stac_collection_queryables(self, stac_host, collection_id):
        """
        Get the queryables of a STAC collection.

        Returns the queryables JSON.
        """
        r = requests.get(os.path.join(stac_host, "collections", collection_id, "queryables"))

        if r.status_code == 200:
            return r.json()
        else:
            r.raise_for_status()

        return {}

    def update_stac_collection(self, stac_collection, stac_collection_queryables):
        """
        Update a STAC collection with summaries obtain by queryables.

        Returns the collection with updated summaries.
        """
        summaries = {}

        for k, v in stac_collection_queryables["properties"].items():
            summaries[k] = v["enum"]

        stac_collection["summaries"] = summaries

        return stac_collection

    def post_collection(self, stac_host, json_data):
        """
        Post a STAC collection.

        Returns the collection id.
        """
        collection_id = json_data['id']
        r = requests.post(os.path.join(stac_host, "collections"), json=json_data)

        if r.status_code == 200:
            print(f"{bcolors.OKGREEN}[INFO] Pushed STAC collection [{collection_id}] to [{stac_host}] ({r.status_code}){bcolors.ENDC}")
        elif r.status_code == 409:
            print(f"{bcolors.WARNING}[INFO] STAC collection [{collection_id}] already exists on [{stac_host}] ({r.status_code}), updating..{bcolors.ENDC}")
            r = requests.put(os.path.join(stac_host, "collections"), json=json_data)
            r.raise_for_status()
        else:
            r.raise_for_status()

        return collection_id

if __name__ == "__main__":
    StacApiCollectionSummariesUpdater()
