import ast
import os
import sys
from io import StringIO

from asset_scanner.scripts import asset_scanner

extract_assets_conf = os.path.join('conf', 'extract-assets.yaml')
extract_items_conf = os.path.join('conf', 'extract-items.yaml')


class Capturing(list):
    """
    Class for capturing stdout
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


def asset_scanner_extractor(config) -> list:
    """
    Mimic the asset_scanner.script.asset_scanner module.

    :param config: conf filepath arg
    """
    conf = asset_scanner.load_config(config)
    asset_scanner.setup_logging(conf)

    extractor = asset_scanner.load_extractor(conf)
    input_plugins = asset_scanner.load_plugins(conf, "asset_scanner.input_plugins", "inputs")
    with Capturing() as output:
        for input in input_plugins:
            input.run(extractor)
    return output


def test_extract_assets():
    """
    Test if the extract has a non-empty body
    """
    output = asset_scanner_extractor(extract_assets_conf)
    extract = ast.literal_eval(output[0])

    assert extract['body']


def test_extract_items():
    """
    Test if the extract has non-empty properties
    """
    output = asset_scanner_extractor(extract_items_conf)
    extract = ast.literal_eval(output[0])

    assert extract['body']['properties']
