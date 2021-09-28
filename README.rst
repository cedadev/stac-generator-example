**********************
Asset-Scanner Example
**********************

This repo serves as a basic example to provide a working introduction to the
`asset-scanner`_ framework. It uses an intake catalog to provide URLs to public
data in an S3 Object Store. These are then turned into STAC Assets and STAC Items.

Getting Started
================

1. Install the requirements

    .. code-block::

        pip install -r requirements.txt

2. Run the `asset-extractor`_

    .. code-block::

        asset-scanner conf/extract-assets.yaml

3. Run the `item-generator`_

    .. code-block::

        asset-scanner conf/extract-items.yaml

Outputs Explained
==================

Asset Extractor
---------------

The asset-extractor outputs a single dict:

.. code-block:: python

    {
        'id': 'c4b8f1578ed806f080f62470ebce2dcd',
        'body': {
            'media_type': 'OBJECT_STORE',
            'filepath_type_location': 'http://cmip6-zarr-o.s3-ext.jc.rl.ac.uk/CMIP6.CMIP.MOHC.UKESM1-0-LL/historical.r4i1p1f2.Amon.tas.gn.v20190502.zarr',
            'filename': 'historical.r4i1p1f2.Amon.tas.gn.v20190502.zarr',
            'extension': '.zarr',
            'categories': ['data']
        }
    }

Item Generator
---------------

The item-generator outputs two dicts:

The first one is the item metadata, containing the extracted properties.

.. code-block:: python


    {
        'id': '4dfbda18d335385742738fad6314450d',
        'body': {
            'item_id': '4dfbda18d335385742738fad6314450d',
            'type': 'item',
            'properties': {
                'mip_era': 'CMIP6',
                'activity_id': 'CMIP',
                'institution_id': 'MOHC',
                'source_id': 'UKESM1-0-LL',
                'experiment_id': 'historical',
                'member_id': 'r4i1p1f2',
                'table_id': 'Amon',
                'variable_id': 'tas',
                'grid_label': 'gn',
                'version': 'v20190502'
            }
        }
    }

The second one outputs an asset object which will allow downstream applications
to associate assets with a particular item.

.. code-block:: python

    {
        'id': '4dfbda18d335385742738fad6314450d',
        'body': {
            'collection_id': '4dfbda18d335385742738fad6314450d'
        }
    }





.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`asset-scanner`: https://cedadev.github.io/asset-scanner/
.. _`asset-extractor`: https://cedadev.github.io/asset-extractor/
.. _`item-generator`: https://cedadev.github.io/item-generator/
