"pdfprocess version"

import subprocess
import re
import sys
import ConfigParser

from stdout import Stdout

class Version():
    def get_pdf2img_ver(self):
        with Stdout() as stdout:
            subprocess.call('pdf2img', stdout=stdout)
            return re.search('pdf2imglib version (.+?)\)\n',
                str(stdout)).group(1)
    def write_version_file(self, current_tag, pdf2img_ver):
        with open('apiversion.ini', 'w') as ini_file:
            config = ConfigParser.ConfigParser()
            config.add_section('webapi')
            config.set('webapi', 'VERSION', str(current_tag))
            config.add_section('pdf2img')
            config.set('pdf2img', 'VERSION', str(pdf2img_ver))
            config.write(ini_file)
            ini_file.close()
    def get_apiversion(self, section):
        config = ConfigParser.ConfigParser()
        config.read('../../../apiversion.ini')
        config.sections()
        data = {}
        options = config.options(section)
        for option in options:
            data[option] = config.get(section, option)
        return data
    def get_version_data(self, filename):
        config = ConfigParser.ConfigParser()
        config.read(filename)
        data = {}
        sections = config.sections()
        for section in sections:
            options = config.options(section)
            for option in options:
                name = section + '-' + option
                data[name] = config.get(section, option)
        return data        

if __name__ == "__main__":
    version = Version()
    version_info = re.split('-', sys.argv[1])
    current_tag = version_info[0]
    pdf2img_ver = version.get_pdf2img_ver()
    version.write_version_file(current_tag, pdf2img_ver)

