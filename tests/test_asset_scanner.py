import ast
import os

from asset_scanner.scripts import asset_scanner

# debug purposes: switch to root directory if run as script
cwd = os.getcwd()
if cwd.split('/')[-1] == 'tests':
    os.chdir('..')

extract_assets_conf = os.path.join('conf', 'extract-assets.yaml')
extract_items_conf = os.path.join('conf', 'extract-items.yaml')


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


def test_extract_assets(capsys):
    """
    Test if the extract has a non-empty body
    """
    asset_scanner_extractor(extract_assets_conf)
    out, err = capsys.readouterr()
    output = out.split('\n')
    extract = ast.literal_eval(output[0])

    assert extract['body']


def test_extract_items(capsys):
    """
    Test if the extract has non-empty properties
    """
    asset_scanner_extractor(extract_items_conf)
    out, err = capsys.readouterr()
    output = out.split('\n')
    extract = ast.literal_eval(output[0])

    assert extract['body']['properties']


def test_id_generation(capsys):
    """
    Test the item_id and file_id are separate ids
    """
    asset_scanner_extractor(extract_items_conf)
    out, err = capsys.readouterr()
    output = out.split('\n')
    item = ast.literal_eval(output[0])
    file = ast.literal_eval(output[1])

    assert item['id'] != file['id']
