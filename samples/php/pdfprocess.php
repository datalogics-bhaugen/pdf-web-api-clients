<?php namespace pdfprocess;

# Copyright (c) 2014, Datalogics, Inc. All rights reserved.

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

const CMD = 'php pdfprocess.php ';
const PDF2IMG_GUIDE = 'http://www.datalogics.com/pdf/doc/pdf2img.pdf';
const USAGE_OPTIONS = '[inputName=name] [password=pwd] [options=json]';

$json = substr(php_uname('s'), 0, 3) == 'Win' ?
    '"{\\"printPreview\\": true, \\"outputFormat\\": \\"jpg\\"}"' :
    '\'{"printPreview": true, "outputFormat": "jpg"}\'';

$usage =
    "usage: " . CMD . "request_type <input document> [input file(s)] " .
        USAGE_OPTIONS . "\n" .
    "example: " . CMD . "DecorateDocument any.pdf headers.xml\n" .
    "example: " . CMD . "FillForm form.pdf form.fdf\n" .
    "example: " . CMD . "FlattenForm hello_world.pdf\n" .
    "example: " . CMD . "RenderPages " . PDF2IMG_GUIDE . " options=" . $json;


/**
 * @brief Sample pdfclient driver:
 * execute pdfprocess.php with no arguments for usage information
 */
class Client extends \pdfclient\Application
{
    /**
     * Create a %pdfclient\\%Request from command-line arguments and execute it
     * @return a Response object
     * @param args e.g.
     *  ['php', '%pdfprocess.php', 'FlattenForm', 'hello_world.pdf']
     * @param base_url default = %https://pdfprocess.datalogics-cloud.com
     */
    function __invoke($args, $base_url = NULL)
    {
        $base_url = $base_url ? $base_url : \pdfclient\BASE_URL;
        $parser = $this->_parse($args, $base_url);
        $input_files = $parser->input_files();

        $default_fields = array('inputName' => '');
        $request_fields = $parser->request_fields();
        $request_fields = array_merge($default_fields, $request_fields);

        $api_request = $this->_request;
        $api_response = $api_request($input_files, $request_fields);
        return new Response($api_response, $this->output_format());
    }

    function output_format()
    {
        return $this->_request->output_format();
    }

    private function _parse($args, $base_url)
    {
        if (count($args) > 2)
        {
            try
            {
                $this->_request = $this->make_request($args[1], $base_url);
                return new Parser($this->_request, array_slice($args, 2));
            }
            catch (Exception $exception)
            {
                echo $exception->getMessage();
            }
        }
        global $usage;
        exit($usage);
    }

    private $_request;
}


/**
 * @brief %pdfclient\\%Response wrapper saves output to a file
 */
class Response
{
    function __construct($api_response, $output_format)
    {
        $this->_api_response = $api_response;
        $this->_output_format = $output_format;
    }

    function __toString() { return (string) $this->api_response(); }

    /**
     * @return pdfclient\\%Response
     */
    function api_response() { return $this->_api_response; }

    /**
     * @return True only if http_code is 200
     */
    function ok() { return $this->api_response()->ok(); }

    function output_filename()
    {
        if ($this->ok() && !$this->_output_format)
            $this->_output_format = $this->output_format();
        if ($this->_output_format)
            return 'pdfprocess.' . $this->_output_format;
        return 'pdfprocess.out';
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

    private function output_format()
    {
        $output = $this->api_response()->output();
        if (strpos($output, '%FDF') === 0) return 'fdf';

        $xml_tag = '<?xml version="1.0" encoding="UTF-8"?>';
        if (strpos($output, $xml_tag . '<xfdf xmlns') === 0) return 'xfdf';
        if (strpos($output, $xml_tag . '<xfa:datasets') === 0) return 'xml';
        return '';
    }

    private $_api_response;
    private $_output_format;
}


/**
 * @brief Translate command line arguments to form needed by
 * <a href="http://www.php.net/manual/en/book.curl.php">curl</a>
 */
class Parser
{
    function __construct($request, $args)
    {
        $is_option = function($arg) { return strpos($arg, '='); };
        $options = array_filter($args, $is_option);

        $is_input = function($arg) { return strpos($arg, '=') === false; };
        $input = array_filter($args, $is_input);

        $urls = array_filter($input, array('pdfprocess\\Parser', '_is_url'));
        if (count($urls) > 1)
        {
            $invalid_input = 'invalid input: ' . count($urls) . ' URLs';
            throw new UnexpectedValueException($invalid_input);
        }

        if ($urls)
        {
            $input_url = array_shift($urls);
            unset($input[array_search($input_url, $input)]);
            $this->_request_fields['inputURL'] = $input_url;
        }
        else
        {
            $this->_input_files['input'] = $input[0];
        }

        $suffixes = array();
        foreach (array_slice($input, 1) as $filename)
        {
            $part_name = $request->part_name($filename);
            if (is_array($part_name))
            {
                $part_name = $part_name[0];
                if (!isset($suffixes[$part_name]))
                {
                    $suffixes[$part_name] = -1;
                }
                $suffix = ++$suffixes[$part_name];
                $part_name = sprintf('%s[%s]', $part_name, $suffix);
            }
            $this->_input_files[$part_name] = $filename;
        }

        $form_parts = array('inputName', 'password', 'options');
        foreach ($options as $arg)
        {
            list($option, $value) = explode('=', $arg);
            if (!in_array($option, $form_parts))
            {
                $invalid_option = 'invalid option: ' . $option;
                throw new UnexpectedValueException($invalid_option);
            }
            $this->_request_fields[$option] =
                $option == 'options' ? json_decode($value, true) : $value;
        }
    }

    /**
     * @return array of input files that will be passed to curl
     */
    function input_files() { return $this->_input_files; }

    /**
     * @return array of request fields that will be passed to curl
     */
    function request_fields() { return $this->_request_fields; }

    private static function _is_url($filename)
    {
        return preg_match('(http:|https:)', strtolower($filename));
    }

    private $_input_files = array();
    private $_request_fields = array();
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
    echo "created: " . $response->output_filename() . "\n";
}
else
{
    echo $response . "\n";
    exit($response->api_response()->error_code());
}
?>
