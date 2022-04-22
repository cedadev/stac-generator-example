# encoding: utf-8
"""
STAC API collection processor
-------------

Create a STAC collection or update its summaries based on its queryables.
"""
__author__ = "Mathieu Provencher"
__date__ = "20 Apr 2022"
__copyright__ = "Copyright 2022 Computer Research Institute of Montréal"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "mathieu.provencher@crim.ca"

import requests
import os
import pystac
import datetime
from asset_scanner.core.utils import generate_id


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


class CollectionProcessor():
    """
    Create a STAC collection or update its summaries based on its queryables.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        stac_host = "http://127.0.0.1:8000/"
        collection_description = "The WCRP Coupled Model Intercomparison Project, Phase 6 (CMIP6), was a global climate model intercomparison project, coordinated by PCMDI (Program For Climate Model Diagnosis and Intercomparison) on behalf of the World Climate Research Program (WCRP) and provided input for the Intergovernmental Panel on Climate Change (IPCC) 6th Assessment Report (AR6).The CMIP6 archive is managed via the Earth System Grid Federation, a globally distributed archive, with various gateways with advanced faceted search capabilities provided by a number of participating organisations. Full details are available from the PCMDI CMIP6 pages (see linked documentation on this record)."
        collection_name = "CMIP6"
        collection_id = generate_id(collection_name)
        stac_collection = self.get_stac_collection(stac_host, collection_id)

        if stac_collection:
            # update collection
            stac_collection_queryables = self.get_stac_collection_queryables(stac_host, collection_id)
            stac_collection = self.update_stac_collection(stac_collection, stac_collection_queryables)
            self.post_collection(stac_host, stac_collection)
        else:
            # create collection
            default_collection = self.create_stac_collection(collection_id, collection_name, collection_description)
            self.post_collection(stac_host, default_collection)

    def get_stac_collection(self, stac_host, collection_id):
        """
        Get a STAC collection

        Returns the collection JSON.
        """
        r = requests.get(os.path.join(stac_host, "collections", collection_id))

        if r.status_code == 200:
            return r.json()

        return {}

    def get_stac_collection_queryables(self, stac_host, collection_id):
        """
        Get the queryables of a STAC collection.

        Returns the queryables JSON.
        """
        r = requests.get(os.path.join(stac_host, "collections", collection_id, "queryables"))

        if r.status_code == 200:
            return r.json()

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

    def create_stac_collection(self, collection_id, collection_name, collection_description):
        """
        Create a basic STAC collection.

        Returns the collection.
        """

        sp_extent = pystac.SpatialExtent([[-140.99778, 41.6751050889, -52.6480987209, 83.23324]])
        capture_date = datetime.datetime.strptime('2015-10-22', '%Y-%m-%d')
        end_capture_date = datetime.datetime.strptime('2100-10-22', '%Y-%m-%d')
        tmp_extent = pystac.TemporalExtent([(capture_date, end_capture_date)])
        extent = pystac.Extent(sp_extent, tmp_extent)

        collection = pystac.Collection(id=collection_id,
                                       title=collection_name,
                                       description=collection_description,
                                       extent=extent,
                                       keywords=[
                                           "climate change",
                                           "CMIP5",
                                           "WCRP",
                                           "CMIP"
                                       ],
                                       providers=None,
                                       summaries=pystac.Summaries({"needs_summaries_update": ["true"]}))

        return collection.to_dict()

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
    CollectionProcessor()
