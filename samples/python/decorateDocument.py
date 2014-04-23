import inspect
import json
import re
import sys
import requests
import os

base_url = ""
app_info = ""

request_dict = {"DecorateDocument": "decorate/document"}

class DecorateDocument(object):

    #assign values to global variables
    def __init__(self, app_data, url):
        global base_url, app_info
        app_info = app_data
        base_url = url

    #create a request to perform a specific task. Request types are listed in
    # the keys of request_dict
    def create_request(self, args):
        request_type = self.get_request_type(args[1])
        full_url = base_url + "/api/actions/" + request_type
        print full_url
        pdf_files, data_files = self.get_files(args[2:])
        data = {}
        files = {}

        #app_info is the app id and key that subscribers are supplied with
        data["application"] = app_info

        # assign xml settings files to the "files" dictionary under the
        #decorationData key
        if len(data_files) != 0:
            files["decorationData"] = data_files[0]
        else:
            print("Invalid input. Please specify at least one data file.\n")

        # PDFs get assigned to the "input" key in the files dictionary
        if len(data_files) != 0:
            files["input"] = pdf_files[0]
        else:
            print("Invalid input. Please specify a PDF file.\n")

        print files["decorationData"]
        #pipe this output to a pdf to see the input PDF with headers/footers
        print requests.post(full_url, verify=False, data=data,
                            files=files).content

    #grab the request type from the command line and determine
    #if that key exists in the request_dict
    def get_request_type(self, request_type):
        if request_type in request_dict.keys():
            return request_dict[request_type]
        else:
            print("Invalid request type; Pick from these: "
                  + str(request_dict.keys()) + "\n")
            sys.exit()

    #grab the files from the command line; open them up and put them in a list
    def get_files(self, files):
        forms_data = ['FDF', 'XFDF', 'XML']
        data_files = []
        pdf_files = []

        for filename in files:
            file_type = filename.split('.')[1].upper()
            open_file = open(filename, 'rb')

            if(file_type == "PDF"):
                pdf_files.append(open_file)
            elif(file_type in forms_data):
                data_files.append(open_file)

        return pdf_files, data_files
