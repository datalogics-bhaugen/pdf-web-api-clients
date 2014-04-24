<?php

# Copyright (c) 2014, Datalogics, Inc. All rights reserved.

# Sample DecorateDocument client module

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

$request_array = array("DecorateDocument" => "decorate/document");

class DecorateDocument {

    function __construct($app_data, $url) {
        $this->app_info = $app_data;
        $this->base_url = $url;
    }

    function create_request($args) {
        $request_type = $this->get_request_type($args[1]);
        //url to send DecorateDocument request to
        $full_url = $this->base_url . "/api/actions/" . $request_type;
        //array containing two arrays (pdf and xml settings)
        $all_files = $this->get_files(array_slice($args,2));
       
        //app_info is the app id and key that subscribers are supplied with        
        $request_fields["application"] = $this->app_info;
        
        if(count($all_files["input"]) > 0) {
            $request_fields["input"] = $all_files["input"][0];
        } else {
            exit("Invalid input. Please specify a PDF file.\n");
        }

        if(count($all_files["decoData"]) > 0) {
            $request_fields["decorationData"] = $all_files["decoData"][0];
        } else {
            exit("Invalid input. Please specify at least one data file.\n");
        }

        //create headers and request to send to url
        $curl = curl_init($full_url);
        $http_header = array('Content-Type: multipart/form-data');
        curl_setopt($curl, CURLOPT_HTTPHEADER, $http_header);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $request_fields);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        //get response from server (if successful, returns PDF)
        $request_response = curl_exec($curl);
        curl_close($curl);
        //pipe this output to a pdf to see the input PDF with headers/footers
        print $request_response . "\n";
        
    }

    //grab the request type from the command line and determine
    //if that value exists in the request_array
    function get_request_type($request_type) {
        global $request_array;

        if(array_key_exists($request_type, $request_array)) {
            return $request_array[$request_type];
        }
        else {
            exit("Request type must be of type DecorateDocument \n");
        }   
    }

    //grab the files from the command line; open them up and put them in a list
    function get_files($files) {
        $deco_data = ["XML"];
        $pdf_files = [];
        $data_files = [];
        foreach($files as $file) {
            $file_type = strtoupper(preg_split("*\.*", $file)[1]);

            if($file_type == "PDF"){
                $pdf_files[] = "@$file";
            } else if(array_search($file_type, $deco_data) == 0) {
                $data_files[] = "@$file";
            }
        }

        $all_files["input"] = $pdf_files;
        $all_files["decoData"] = $data_files;
        return $all_files;
    }
}

?>
