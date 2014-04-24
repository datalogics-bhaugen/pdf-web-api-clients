<?php

$request_array = array("DecorateDocument" => "decorate/document");

class DecorateDocument {

    function __construct($app_data, $url) {
        $this->app_info = $app_data;
        $this->base_url = $url;
    }
    
    function create_request($args) {
        $request_type = $this->get_request_type($args[1]);
        $full_url = $this->base_url . "/api/" . $request_type;
        $all_files = $this->get_files(array_slice($args,2));
                
        $request_fields["application"] = $this->app_info;
        
        if(count($all_files["input"]) > 0) {
            $request_fields["input"] = $all_files["input"][0];
        } else {
            //throw error that a pdf file has not been given as input
        }
        
        if(count($all_files["decoData"]) > 0) {
            $request_fields["decorationData"] = $all_files["decoData"][0];
        } else {
            //throw error that an xml settings file has not been given as input
        }

        $curl = curl_init($full_url);
        $http_header = array('Content-Type: multipart/form-data');
        curl_setopt($curl, CURLOPT_HTTPHEADER, $http_header);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $request_fields);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        $request_response = curl_exec($curl);
        $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);
        print $request_response . "\n";
        
    }
    
    function get_request_type($request_type) {
        global $request_array;

        if(array_key_exists($request_type, $request_array)) {
            return $request_array[$request_type];
        }
        else {
            //TODO: throw error (url suffix DNE)
        }   
    }
    
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