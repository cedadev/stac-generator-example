import ast
import os

from asset_scanner.scripts import asset_scanner

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
