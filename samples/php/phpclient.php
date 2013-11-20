<?php
/**
 * Copyright (c) 2013, Datalogics, Inc. All rights reserved.
 *
 *"Sample pdfprocess client module"
 *
 * This agreement is between Datalogics, Inc. 101 N. Wacker Drive, Suite 1800,
 * Chicago, IL 60606 ("Datalogics") and you, an end user who downloads
 * source code examples for integrating to the Datalogics (R) PDF WebAPI (TM)
 * ("the Example Code"). By accepting this agreement you agree to be bound
 * by the following terms of use for the Example Code.
 *
 * LICENSE
 * -------
 * Datalogics hereby grants you a royalty-free, non-exclusive license to
 * download and use the Example Code for any lawful purpose. There is no charge
 * for use of Example Code.
 *
 * OWNERSHIP
 * ---------
 * The Example Code and any related documentation and trademarks are and shall
 * remain the sole and exclusive property of Datalogics and are protected by
 * the laws of copyright in the U.S. and other countries.
 *
 * Datalogics and Datalogics PDF WebAPI are trademarks of Datalogics, Inc.
 *
 * TERM
 * ----
 * This license is effective until terminated. You may terminate it at any
 * other time by destroying the Example Code.
 *
 * WARRANTY DISCLAIMER
 * -------------------
 * THE EXAMPLE CODE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER
 * EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
 *
 * DATALOGICS DISCLAIM ALL OTHER WARRANTIES, CONDITIONS, UNDERTAKINGS OR
 * TERMS OF ANY KIND, EXPRESS OR IMPLIED, WRITTEN OR ORAL, BY OPERATION OF
 * LAW, ARISING BY STATUTE, COURSE OF DEALING, USAGE OF TRADE OR OTHERWISE,
 * INCLUDING, WARRANTIES OR CONDITIONS OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE, SATISFACTORY QUALITY, LACK OF VIRUSES, TITLE,
 * NON-INFRINGEMENT, ACCURACY OR COMPLETENESS OF RESPONSES, RESULTS, AND/OR
 * LACK OF WORKMANLIKE EFFORT. THE PROVISIONS OF THIS SECTION SET FORTH
 * SUBLICENSEE'S SOLE REMEDY AND DATALOGICS'S SOLE LIABILITY WITH RESPECT
 * TO THE WARRANTY SET FORTH HEREIN. NO REPRESENTATION OR OTHER AFFIRMATION
 * OF FACT, INCLUDING STATEMENTS REGARDING PERFORMANCE OF THE EXAMPLE CODE,
 * WHICH IS NOT CONTAINED IN THIS AGREEMENT, SHALL BE BINDING ON DATALOGICS.
 * NEITHER DATALOGICS WARRANT AGAINST ANY BUG, ERROR, OMISSION, DEFECT,
 * DEFICIENCY, OR NONCONFORMITY IN ANY EXAMPLE CODE.
 * 
 * PHPClient Sample
 * ----------------
 * phpclient.php is a sample php file that demonstrates how to request
 * and respond to data sent and received by the Datalogics PDF WebAPI 
 * servers.  This script takes data received via the pdfprocess.php
 * client driver script, request an action from the PDF WebAPI servers
 * and produces any output received in the response.
 * 
 * Samples for additional languages and there documentation can be 
 * found at the links provided.
 *
 * @package php_client
 * @link ../classes/Request.html Request
 * @link ../classes/Response.html Response
 * @link phpclient.php.txt Source
 * @link https://api.datalogics-cloud.com PDF WebAPI Documentation
 */

error_reporting(E_ALL);

/**
 * Class for preparing and sending a request to the WebAPI server
 */
class Request
{
    /**
     * Make the request to the server
     *
     * You can find
     * <a href="https://api.datalogics-cloud.com/#RequestExamples">
     * Request Examples</a> at 
     * <a href="https://api.datalogics-cloud.com">api.datalogics-cloud.com</a>
     *
     * @param string $full_url Complete URL for server request
     * @param string[] $prepared_request JSON encoded array with request data
     * @return string|string[] $response Response from the server
     */
    public function make_request($full_url, $prepared_request)
    {
        $ch = curl_init($full_url);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $prepared_request);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_VERBOSE, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER,
                       array('Content-Type: multipart/form-data'));
        $response = curl_exec($ch);
        curl_close($ch);
        return $response;
    }

    /**
     * Prepare the data to be sent in the server request
     * 
     * You can find the proper    
     * <a href="https://api.datalogics-cloud.com/#RequestForm">Request Form</a>
     * at
     * <a href="https://api.datalogics-cloud.com">api.datalogics-cloud.com</a>
     *
     * @param string $app_id Application ID
     * @param string $app_key Application Key
     * @param string $file The name of the input file
     * @param string $password Password for PDF Document
     * @param string $input_name The name for the file if differnt from $file
     * @param string[] $options JSON encoded array of user optionsi
     */
    public function prepare_request($app_id, $app_key, $file, $password = NULL,
                                    $input_name = NULL, $options = NULL)  
    {

        printf($app_id);
        //verify if a different file name is wanted
        $file_name = ($input_name != NULL ? $input_name : $file);
        
        //add fields to output array
        $fields = array();
        $fields['application'] = $this->prepare_application_json($app_id, 
                                                                  $app_key);
        $fields['inputName'] = $file_name;
        $fields['input'] = "@$file";
        
        //verify these were requested before adding
        if($options != NULL) 
        { 
            $field['options'] = $options; 
        }
        if($password != NULL) 
        { 
            $fields['password'] = $password; 
        }
         
        return $fields;
    }

    /**
     * Puts the application ID and key into JSON Format
     * 
     * For information on preparing the 
     * <a href="https://api.datalogics-cloud.com/#application">
     * Application</a> please see
     * <a href="https://api.datalogics-cloud.com">api.datalogics-cloud.com</a>
     *
     * @param string $app_id Application ID
     * @param string $app_key Application Key
     * @return string[] $application JSON encoded array with ID and Key data
     */
    private function prepare_application_json($app_id, $app_key)
    {
        $application = array('id' => $app_id, 'key' => $app_key);
        return json_encode($application);
    }
}

/**
 * Class to deal with the response sent by the WebApi server
 */
class Response
{
    /**
     * Process the response from the WebAPI server
     *
     * Please see 
     * @see <a href="https://api.datalogics-cloud.com/#ServiceResponse">
     * Service Response</a> at 
     * <a href="https://api.datalogics-cloud.com">api.datalogics-cloud.com</a>
     * for more information on responses from the server.
     *
     * @param string|string[] $response Response from the Server
     * @param string $destination_file File to write output to
     * @param string $service Request type requested from the server
     * @param string $input_file File that was sent to the server
     * <a href="https://api.datalogics-cloud.com/#ServiceResponse">
     * Service Response</a> at 
     * <a href="https://api.datalogics-cloud.com">api.datalogics-cloud.com</a>
     */
    public function handle_response($response, $destination_file, 
                                    $service, $input_file)
    {
        $json_decoded = json_decode($response);
        if(json_last_error() == JSON_ERROR_NONE)
        {
            $error_code = $json_decoded->errorCode;
            $error_message = $json_decoded->errorMessage;
            printf('ERROR: '.$error_code."\n");
            printf($error_message."\n");
            exit($error_code);
        }
        elseif($service === '/flatten/form')
        {
            $file = fopen($input_file, "wb");
        }
        else
        {
            $file = fopen($destination_file, "wb");
        }
        fwrite($file, $response);
        fclose($file);
    }
    
}

?>
