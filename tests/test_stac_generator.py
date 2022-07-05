import json
import os

from stac_generator.scripts import stac_generator

# debug purposes: switch to root directory if run as script
cwd = os.getcwd()
if cwd.split('/')[-1] == 'tests':
    os.chdir('..')

# delete all files in the test/file-io directory for fresh test instance
io_dir = os.path.join('tests', 'file-io')
for file in os.listdir(io_dir):
    os.remove(os.path.join(io_dir, file))
    
# get the config files for the generators    
asset_generator_conf = os.path.join('conf', 'extract-assets.yaml')
item_generator_conf = os.path.join('conf', 'extract-items.yaml')
collection_generator_conf = os.path.join('conf', 'extract-collections.yaml')



def stac_generator_mime(config):
    """
    Mimic the stac_generator.script.stac_generator module.

    :param config: conf filepath arg
    """
    conf = stac_generator.load_config(config)
    stac_generator.setup_logging(conf)

    generator = stac_generator.load_generator(conf)
    input_plugins = stac_generator.load_plugins(conf, "stac_generator.input_plugins", "inputs")
    for input in input_plugins:
        input.run(generator)


def test_generate_assets():
    """
    Test if the generator has a non-empty properties
    """
    stac_generator_mime(asset_generator_conf)
    output_dir = os.path.join('tests', 'file-io', 'assets.json')

    with open(output_dir, 'r+') as file:
        data = json.load(file)

    assert data[0]['body']['properties']


def test_generate_items():
    """
    Test if the generator has non-empty properties
    """
    stac_generator_mime(item_generator_conf)
    output_dir = os.path.join('tests', 'file-io', 'items.json')

    with open(output_dir, 'r+') as file:
        data = json.load(file)

    assert data[0]['body']['properties']


def test_generate_collections():
    """
    Test if the collections has non-empty summaries
    """
    stac_generator_mime(collection_generator_conf)
    output_dir = os.path.join('tests', 'file-io', 'collections.json')

    with open(output_dir, 'r+') as file:
        data = json.load(file)

    assert data[0]['body']['summaries']

# What was the reason for this test?
# def test_id_generation(capsys):
#     """
#     Test the item_id and file_id are separate ids
#     """
#     stac_generator_extractor(extract_items_conf)
#     out, err = capsys.readouterr()
#     output = out.split('\n')
#     item = ast.literal_eval(output[0])
#     file = ast.literal_eval(output[1])

#     assert item['id'] != file['id']
