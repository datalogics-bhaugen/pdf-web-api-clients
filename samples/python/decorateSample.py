from decorateDocument import DecorateDocument

import sys

APPLICATION_INFO = '{"id": "", "key": ""}'  # TODO: Paste!
BASE_URL = 'https://pdfprocess-test.datalogics-cloud.com'

def main(args):
    deco_request = DecorateDocument(APPLICATION_INFO, BASE_URL)

    deco_request.create_request(args)

if __name__ == '__main__':
    main(sys.argv)
