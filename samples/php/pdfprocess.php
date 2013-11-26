<?php namespace pdfprocess;

# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

# Sample pdfclient driver

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

include 'pdfclient.php';

const APPLICATION_ID = 'your app id';  # TODO: paste!
const APPLICATION_KEY = 'your app key';  # TODO: paste!

const PDF2IMG_GUIDE = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf';
const USAGE_OPTIONS = '[inputName=name] [password=pwd] [options=json]';

$usage =
    "usage: pdfprocess.php request_type input " . USAGE_OPTIONS . "\n" .
    "example: pdfprocess.php FlattenForm hello_world.pdf\n" .
    "example: pdfprocess.php RenderPages " . PDF2IMG_GUIDE .
        'options={"printPreview": True, "outputFormat": "jpg"}';


/**
 * @brief Sample pdfclient driver:
 * execute %pdfprocess.php with no arguments for usage information
 */
class Client extends \pdfclient\Application
{
    /**
     * Create a Request from command-line arguments and execute it
     * @return a Response object
     * @param args e.g.['%pdfprocess.php', 'FlattenForm', 'hello_world.pdf']
     * @param base_url default = %https://pdfprocess.datalogics-cloud.com
     */
    function __invoke($args, $base_url = NULL)
    {
        if (count($args) < 3) { exit($usage); }

        $input = $args[2];
        $request_fields = $this->_initialize($args);
        $base_url = $base_url ? $base_url : \pdfclient\BASE_URL;
        $this->_request = $this->make_request($args[1], $base_url);

        $input_name = $request_fields['inputName'];
        $this->_input_name = $input_name ? $input_name : basename($input);

        $api_request = $this->_request;
        $api_response = $api_request($input, $request_fields);
        return new Response($api_response, $this->output_filename());
    }

    /**
     * Derived from the input name or explicitly specified
     */
    function input_name() { return $this->_input_name; }

    /**
     * @return #input_name with extension replaced by requested output format
     */
    function output_filename()
    {
        $extension = $this->_request->output_format();
        return basename($this->input_name(), '.pdf') . '.' . $extension;
    }

    private function _initialize($args)
    {
        try
        {
            return $this->_parse_args(array_slice($args, 3));
        }
        catch (Exception $exception)
        {
            echo $exception->getMessage();
            exit($usage);
        }
    }

    private function _parse_args($args)
    {
        $result = array();
        $options = array('inputName', 'password', 'options');
        foreach ($args as $arg)
        {
            list($option, $value) = explode('=', $arg);
            if (!array_search($option, OPTIONS))
            {
                $invalid_option = 'invalid option: ' . $option;
                throw new UnexpectedValueException($invalid_option);
            }
            $result[$option] =
                $option == 'options' ? json_decode($value, true) : $value;
        }
        return $result;
    }

    private $_input_name;
    private $_request;
}


/**
 * @brief %pdfclient\\%Response wrapper
 * saves output to the file specified by the request
 */
class Response
{
    function __construct($api_response, $output_filename)
    {
        $this->_api_response = $api_response;
        $this->_output_filename = $output_filename;
    }

    function __toString() { return (string) $this->api_response(); }

    /**
     * @return pdfclient\\%Response
     */
    public function api_response() { return $this->_api_response; }

    /**
     * @return True only if http_code is 200
     */
    function ok() { return $this->api_response()->ok(); }

    /**
     * Derived from Client.input_name and requested output format
     */
    public function output_filename()
    {
        if ($this->ok()) { return $this->_output_filename; }
    }

    /**
     * Save output in file named #output_filename
     */
    function save_output()
    {
        $output_file = fopen($this->output_filename(), 'wb');
        fwrite($output_file, $this->api_response()->output());
        fclose($output_file);
    }

    private $_api_response;
    private $_output_filename;
}


function run($args, $app_id = NULL, $app_key = NULL)
{
    if (!$app_id) $app_id = APPLICATION_ID;
    if (!$app_key) $app_key = APPLICATION_KEY;

    $client = new Client($app_id, $app_key);
    return $client($args);
}

$response = run($argv);
if ($response->ok())
{
    $response->save_output();
    echo 'created: ' . $response->output_filename();
}
else
{
    echo $response;
    exit($response->api_response()->error_code());
}
?>
