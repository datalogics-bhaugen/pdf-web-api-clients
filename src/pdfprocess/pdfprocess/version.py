"pdfprocess version"

import subprocess
import re
import sys
from stdout import Stdout

class Version():
    def get_pdf2img_ver(self):
        with Stdout() as stdout:
            subprocess.call('pdf2img', stdout=stdout)
            return re.search('pdf2imglib version (.+?)\)\n',
                str(stdout)).group(1)
    def write_version_file(self, current_tag, pdf2img_ver):
        file_handle = open('version.ini', 'w')
        file_handle.write('[webapi]\n')
        file_handle.write('VERSION=%s' % str(current_tag))
        file_handle.write('[pdf2img]\n')
        file_handle.write('VERSION=%s' % str(pdf2img_ver))
        file_handle.close()

if __name__ == "__main__":
    version = Version()
    version_info = re.split('-', sys.argv[1])
    current_tag = version_info[0]
    pdf2img_ver = Version.get_pdf2img_ver(version)
    Version.write_version_file(version, current_tag, pdf2img_ver)

