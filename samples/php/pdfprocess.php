<?php
# Copyright (c) 2013, Datalogics, Inc. All rights reserved.
#
# Sample pdfclient driver
#
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

include 'phpclient.php';

error_reporting(E_ALL);

/**
 * Class for the purpose of converting user input into 
 * data needed for proper server request
 */
class PDFProcess
{
    /**
     * @var string $base_url The base of the request URL 
     */
    var $base_url = "https://pdfprocess.datalogics-cloud.com";
    
    /** 
     * @var string $full_url The Full URL for the service request 
     */
    var $full_url;
    
    /** 
     * @var string $application_id Application ID at api.datalogics-cloud.com 
     */
    var $application_id = '123456789';
   
    /**
     * @var string $application_key Application Key at api.datalogics-cloud.com 
     */
    var $application_key = '123456789abcdefghi';
    
    /**
     * @var string $source_file Full path to file being uploaded for processing
     */
    var $source_file;

    /**
     * @var string $source_file_name File name without Path information
     */
    var $source_file_name;
    
    /**
     * @var string $URL_input URL to pdf file to be processed 
     */
    var $URL_input = NULL;

    /**
     * @var string $destination_file_name Output file name
     */
    var $destination_file_name;

    /**
     * @var string $output_format Default format for output file 
     */
    var $output_format = 'png';

    /**
     * @var boolean $print_preview Default print preview option setting 
     */
    var $print_preview = FALSE;

    /**
     * @var JSONArray $options holds options for server request call
     */
    var $options;

    /**
     * Service request to be used on the uploaded document
     * @var string $request_type Service to be used on provided document
     */
    var $request_type;

    /**
     * @var string $password User provided password for given PDf file
     */
    var $password;
  
    /**
     * Format request type given on the command line
     * for use in request URL.
     * @param string $request_type the request type argument
     * @return string $return_string the URL formatted request type
     */ 
    public function set_request_type($request_type)
    {
        $string_array = str_split($request_type);
        $formatted_string = '';
        foreach($string_array as $char)
        {
            if(ctype_upper($char))
            {
                $formatted_string .= '/'. strtolower($char);
            }
            else
            {
                $formatted_string .= $char;
            }
        }
        return $formatted_string;
    }

    /** 
     * Parses through arguments to create JSON formatted array for request
     * @param string[]  $args The user provided arguments
     * @return string[]  $json_array The JSON formatted array
     * @throws Exception If arguments provided are not formatted correctly 
     */
    private function set_options($args)
    {   
        $input = array();
        $options = array();
        $scriptName = $args[0];

        foreach ($args as $key => $index)
        {   
            if ($scriptName === $index ||
                $args[1] === $index ||
                $this->source_file === $index)
            {   
                continue;
            }   
            else if (strpos($index, '=') !== false)
            {   
                list($opt, $value) = explode('=', $index, 2); 
                if ($opt === 'password')
                {   
                    $input[$opt] = $value;
                }   
                else if ($opt === 'input_name')
                {   
                    $this->source_file_name = $value;
                }   
                else if ($opt === 'options')
                {   
                    $decoded = array(json_decode($value));
                    foreach ($decoded[0] as $ref => $val)
                    {   
                        $options[$ref] = $val;
                    }   
                }   
            }   
            else
            {   
                throw new Exception('Usage: '
                                     .$scriptName.
                                     ' request_type input [input_name=name]'
                                     .' [password=pwd] [options=json]');
            }   
        }   
        $json_array = array_merge($input, $options);
        return $json_array;
    }   

    /**
     * Set the full URL for making service request
     */
    private function set_request_url()
    {
        $this->full_url = $this->base_url . '/api/actions'. $this->request_type;
    }

    /**
     * Set the format for the name of the output file (if any)
     * @param string[] $json_array An array of options in JSON format
     */
    private function set_output_format($json_array)
    {
        if (array_key_exists('outputFormat', $json_array))
        {
            $this->output_format = $json_array['outputFormat'];
        }

        list($this->destination_file_name, $type)
                        = explode('.', $this->source_file_name);
        $this->destination_file_name .= '.'. $this->output_format;
    }

    /**
     * Parse command line arguments to create proper server request call
     * @param string[] $args The user supplied arguments
     * @param int $argc The number of arguments the user provided
     * @throws Exception If enough arguments are not provided
     */ 
    public function parse_arguments($args, $argc) 
    {
	$this->request_type = $this->set_request_type($args[1]);
        $this->source_file = $args[2];
	$this->source_file_name = basename($args[2]);

	if ($argc < 3)
	{
	    throw new Exception('Usage: ' 
                                .$scriptName. 
                                ' request_type input [input_name=name]'
                                .' [password=pwd] [options=json]');
	}
        
        $json_array = $this->set_options($args);
        $this->options = json_encode($json_array);
        
        $this->set_output_format($json_array);
        $this->set_request_url();
    } 
}

// Driver code
$pdfprocess = new PDFProcess();
$requester = new Request();
$responder = new Response();

try
{
    $pdfprocess->parse_arguments($argv, $argc);
}
catch (Exception $e)
{
    echo $e->getMessage(), "\n";
    exit();
}

$prepared = $requester->prepare_request($pdfprocess->source_file_name,
                                        $pdfprocess->options,
                                        $pdfprocess->application_id,
                                        $pdfprocess->application_key,
                                        $argc);
$response = $requester->make_request($pdfprocess->full_url, $prepared);
$responder->handle_response($response, 
                            $pdfprocess->destination_file_name, 
                            $pdfprocess->request_type,
                            $pdfprocess->source_file);

?>
