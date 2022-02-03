import json
import os

import pytest
from asset_scanner.scripts import asset_scanner

# debug purposes: switch to root directory if run as script
cwd = os.getcwd()
if cwd.split('/')[-1] == 'tests':
    os.chdir('..')

# delete all files in the test/file-io directory for fresh test instance
io_dir = os.path.join('tests', 'file-io')
for file in os.listdir(io_dir):
    os.remove(os.path.join(io_dir, file))
    
# get the config files for the generators    
extract_assets_conf = os.path.join('conf', 'extract-assets.yaml')
extract_items_conf = os.path.join('conf', 'extract-items.yaml')
extract_collections_conf = os.path.join('conf', 'extract-collections.yaml')



def asset_scanner_extractor(config):
    """
    Mimic the asset_scanner.script.asset_scanner module.

    :param config: conf filepath arg
    """
    conf = asset_scanner.load_config(config)
    asset_scanner.setup_logging(conf)

    extractor = asset_scanner.load_extractor(conf)
    input_plugins = asset_scanner.load_plugins(conf, "asset_scanner.input_plugins", "inputs")
    for input in input_plugins:
        input.run(extractor)


def test_extract_assets():
    """
    Test if the extract has a non-empty properties
    """
    asset_scanner_extractor(extract_assets_conf)
    output_dir = os.path.join('tests', 'file-io', 'assets.json')

    with open(output_dir, 'r+') as file:
        data = json.load(file)

    assert data[0]['body']['properties']


def test_extract_items():
    """
    Test if the extract has non-empty properties
    """
    asset_scanner_extractor(extract_items_conf)
    output_dir = os.path.join('tests', 'file-io', 'items.json')

    with open(output_dir, 'r+') as file:
        data = json.load(file)

    assert data[0]['body']['properties']


def test_extract_collections():
    """
    Test if the collections has non-empty summaries
    """
    asset_scanner_extractor(extract_collections_conf)
    output_dir = os.path.join('tests', 'file-io', 'collections.json')

    with open(output_dir, 'r+') as file:
        data = json.load(file)

    assert data[0]['body']['summaries']

# What was the reason for this test?
# def test_id_generation(capsys):
#     """
#     Test the item_id and file_id are separate ids
#     """
#     asset_scanner_extractor(extract_items_conf)
#     out, err = capsys.readouterr()
#     output = out.split('\n')
#     item = ast.literal_eval(output[0])
#     file = ast.literal_eval(output[1])

#     assert item['id'] != file['id']
