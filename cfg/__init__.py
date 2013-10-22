import os
import glob
import ConfigParser

class Config(dict):
    def __getattr__(self, name): return self[name]
    def read(self, filenames, parser=ConfigParser.ConfigParser()):
        parser.read(filenames)
        for section in parser.sections():
            if section not in self: self[section] = self.__class__()
            for name, value in parser.items(section):
                self[section][name] = value

def is_cfg_file(file):
    return not os.path.splitext(file)[1].startswith('.py')

Configuration = Config()
cfg_files = glob.glob('{}/*'.format(os.path.dirname(__file__)))
Configuration.read(file for file in cfg_files if is_cfg_file(file))
