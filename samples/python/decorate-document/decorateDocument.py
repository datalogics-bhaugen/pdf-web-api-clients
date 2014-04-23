# Copyright (c) 2014, Datalogics, Inc. All rights reserved.

"Sample DecorateDocument client module"

# This agreement is between Datalogics, Inc. 101 N. Wacker Drive, Suite 1800,
# Chicago, IL 60606 ("Datalogics") and you, an end user who downloads
# source code examples for integrating to the Datalogics (R) PDF WebAPI (TM)
# ("the Example Code"). By accepting this agreement you agree to be bound
# by the following terms of use for the Example Code.
#
# LICENSE
# -------
# Datalogics hereby grants you a royalty-free, non-exclusive license to
# download and use the Example Code for any lawful purpose. There is no charge
# for use of Example Code.
#
# OWNERSHIP
# ---------
# The Example Code and any related documentation and trademarks are and shall
# remain the sole and exclusive property of Datalogics and are protected by
# the laws of copyright in the U.S. and other countries.
#
# Datalogics and Datalogics PDF WebAPI are trademarks of Datalogics, Inc.
#
# TERM
# ----
# This license is effective until terminated. You may terminate it at any
# other time by destroying the Example Code.
#
# WARRANTY DISCLAIMER
# -------------------
# THE EXAMPLE CODE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER
# EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
# DATALOGICS DISCLAIM ALL OTHER WARRANTIES, CONDITIONS, UNDERTAKINGS OR
# TERMS OF ANY KIND, EXPRESS OR IMPLIED, WRITTEN OR ORAL, BY OPERATION OF
# LAW, ARISING BY STATUTE, COURSE OF DEALING, USAGE OF TRADE OR OTHERWISE,
# INCLUDING, WARRANTIES OR CONDITIONS OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE, SATISFACTORY QUALITY, LACK OF VIRUSES, TITLE,
# NON-INFRINGEMENT, ACCURACY OR COMPLETENESS OF RESPONSES, RESULTS, AND/OR
# LACK OF WORKMANLIKE EFFORT. THE PROVISIONS OF THIS SECTION SET FORTH
# SUBLICENSEE'S SOLE REMEDY AND DATALOGICS'S SOLE LIABILITY WITH RESPECT
# TO THE WARRANTY SET FORTH HEREIN. NO REPRESENTATION OR OTHER AFFIRMATION
# OF FACT, INCLUDING STATEMENTS REGARDING PERFORMANCE OF THE EXAMPLE CODE,
# WHICH IS NOT CONTAINED IN THIS AGREEMENT, SHALL BE BINDING ON DATALOGICS.
# NEITHER DATALOGICS WARRANT AGAINST ANY BUG, ERROR, OMISSION, DEFECT,
# DEFICIENCY, OR NONCONFORMITY IN ANY EXAMPLE CODE.

import sys
import requests

request_dict = {"DecorateDocument": "decorate/document"}

class DecorateDocument(object):

    #assign values to global variables
    def __init__(self, app_data, url):
        self.app_info = app_data
        self.base_url = url

    #create a request to perform a specific task. Request types are listed in
    # the keys of request_dict
    def create_request(self, args):
        request_type = self.get_request_type(args[1])
        full_url = self.base_url + "/api/" + request_type
        pdf_files, data_files = self.get_files(args[2:])
        data = {}
        files = {}

        #app_info is the app id and key that subscribers are supplied with
        data["application"] = self.app_info

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

        #pipe this output to a pdf to see the input PDF with headers/footers
        print(requests.post(full_url, verify=False, data=data,
                            files=files).content)

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
        deco_data = ['XML']
        data_files = []
        pdf_files = []

        for filename in files:
            file_type = filename.split('.')[1].upper()
            open_file = open(filename, 'rb')

            if(file_type == "PDF"):
                pdf_files.append(open_file)
            elif(file_type in deco_data):
                data_files.append(open_file)

        return pdf_files, data_files
