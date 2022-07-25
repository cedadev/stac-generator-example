**********************
STAC Generator Example
**********************

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/cedadev/stac-generator-example/HEAD
.. image:: https://github.com/cedadev/stac-generator-example/actions/workflows/tests.yaml/badge.svg
 :target: https://github.com/cedadev/stac-generator-example/actions/workflows/tests.yaml

This repo serves as a basic example to provide a working introduction to the
`stac-generator`_ framework. It uses an intake catalog to provide URLs to public
data in an S3 Object Store. These are then turned into a STAC Catalog of Assets,
Items, and Collections.

Getting Started
================

You can either run locally or launch in Binder:
 
Running in Binder
-----------------

Click 

.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/cedadev/stac-generator-example/HEAD

To just run it and see the example output, open ``example_notebook.ipynb``.


Local deployment
-----------------

1. Install the requirements

    .. code-block::

        pip install -r requirements.txt

2. Run the `asset-generator`_

    .. code-block::

        stac_generator conf/asset-generator.yaml

3. Run the `item-generator`_

    .. code-block::

        stac_generator conf/item-generator.yaml

3. Run the `collection-generator`_

    .. code-block::

        stac_generator conf/collection-generator.yaml

Inputs Explained
================

The yaml files in conf setup the input and outputs for the script. In this case, the input is an intake-esm catalog and the output is the terminal.

The file in collection-descriptions, describes the workflow to extract the facets.

.. code-block:: yaml

    paths:
  - https://cmip6-zarr-o.s3-ext.jc.rl.ac.uk/CMIP6.CMIP.MOHC.UKESM1-0-LL

    asset:
    # The default asset id is a hash of the assets uri
    extraction_methods:
        # - method: posix_stats
        - method: regex
        inputs:
            regex: 'https://cmip6-zarr-o.s3-ext.jc.rl.ac.uk\/(?P<mip_era>\w+)\.(?P<activity_id>\w+)\.(?P<institution_id>[\w-]+)\.(?P<source_id>[\w-]+)\/(?P<experiment_id>[\w-]+)\.(?P<member_id>\w+)\.(?P<table_id>\w+)\.(?P<var_id>\w+)\.(?P<grid_label>\w+)\.(?P<version>\w+)'

    item:
    # The default item id is a hash of the collection id
    id:
        method: hash
        inputs:
        terms:
            - mip_era
            - activity_id
            - institution_id
            - source_id
            - table_id
            - var_id
            - version
    extraction_methods:
        - method: json_file
        inputs:
            filepath: tests/file-io/assets.json
            terms:
            - mip_era
            - activity_id
            - institution_id
            - source_id
            - table_id
            - var_id
            - version

    collection:
    # The default collection id is "undefined"
    id:
        method: default
        inputs:
        value: cmip6
    extraction_methods:
        - method: json_file
        inputs:
            filepath: tests/file-io/items.json
            terms:
            - mip_era
            - activity_id
            - institution_id
            - source_id
            - table_id
            - var_id
            - version


Outputs Explained
=================

Asset Generator
---------------

The asset-generator outputs:

.. code-block:: python

    {
        'id': 'c4b8f1578ed806f080f62470ebce2dcd',
        'body': {
            'type': 'asset',
            'properties': {
                'media_type': 'OBJECT_STORE',
                'filepath_type_location': 'http://cmip6-zarr-o.s3-ext.jc.rl.ac.uk/CMIP6.CMIP.MOHC.UKESM1-0-LL/historical.r4i1p1f2.Amon.tas.gn.v20190502.zarr',
                'filename': 'historical.r4i1p1f2.Amon.tas.gn.v20190502.zarr',
                'extension': '.zarr',
            },
            'categories': ['data']
        }
    }

Item Generator
--------------

The item-generator outputs:

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

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`stac-generator`: https://cedadev.github.io/stac-generator/
