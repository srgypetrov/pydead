import os
import configparser


base_dir = os.getcwd()
config_file = os.path.join(base_dir, '.pydead')

parser = configparser.ConfigParser()
parser.read(config_file)


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


conf = AttributeDict(
    EXCLUDE=['.*'] + parser.get('paths', 'exclude', fallback='').split('\n'),
    EXTENSIONS=['.py'],
    BASE_DIR=base_dir
)
