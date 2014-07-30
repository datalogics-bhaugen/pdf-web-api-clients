import os
import glob
import ConfigParser

class Config(dict):
    DLENV = 'dlenv'  # PROD or TEST
    DLENV_FILENAME = '/etc/dl_environment'
    def __getattr__(self, name): return self[name]
    def initialize(self, filenames, default_dlenv='test'):
        "Parse configuration files and set *dlenv* attribute."
        parser = ConfigParser.ConfigParser()
        parser.read(filenames)
        for section_name in parser.sections():
            section = self._section(section_name)
            for name, value in parser.items(section_name):
                section[name] = value
        self._set_environment(Config.DLENV_FILENAME)
        self._set_dlenv(self.environment, default_dlenv)
    def _section(self, name):
        if name not in self: self[name] = self.__class__()
        return self[name]
    def _set_dlenv(self, section, default_dlenv):
        dlenv = Config.DLENV
        if dlenv in os.environ: section[dlenv] = os.environ[dlenv]
        elif dlenv not in section: section[dlenv] = default_dlenv
        section[dlenv] = section[dlenv].lower()
    def _set_environment(self, dlenv_filename):
        section = self._section('environment')
        if glob.glob(dlenv_filename):
            for line in open(dlenv_filename):
                name, value = line.split('=')
                section[name] = value.rstrip()

def _is_cfg_file(file):
    return not os.path.splitext(file)[1].startswith('.py')

Configuration = Config()
cfg_files = glob.glob('{}/*'.format(os.path.dirname(__file__)))
Configuration.initialize(file for file in cfg_files if _is_cfg_file(file))
