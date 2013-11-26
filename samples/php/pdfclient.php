<?php namespace pdfclient;

# Copyright (c) 2013, Datalogics, Inc. All rights reserved.

# Sample pdfprocess client module

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

const BASE_URL = 'https://pdfprocess.datalogics-cloud.com';


/**
 * @brief %Request factory
 */
class Application
{
    /**
     * @param id from our [developer portal](http://api.datalogics-cloud.com/)
     * @param key from our [developer portal](http://api.datalogics-cloud.com/)
     */
    function __construct($id, $key)
    {
        $this->_json = json_encode(array('id' => $id, 'key' => $key));
    }

    /**
     * Create a request for the specified request type
     * @return a Request object
     * @param request_type e.g. '%FlattenForm'
     * @param base_url default = %https://pdfprocess.datalogics-cloud.com
     */
    function make_request($request_type, $base_url = NULL)
    {
        if (!$base_url) $base_url = BASE_URL;

        $request_type = '\\pdfclient\\' . $request_type;
        return new $request_type($this->_json, $base_url);
    }

    private $_json;
}


/**
 * @brief Service request
 */
class Request
{
    function __construct($application_json, $base_url)
    {
        $class_name = end(explode('\\', get_class($this)));
        $action = preg_replace('/([A-Z])/', '/$1', $class_name);
        $this->_url = $base_url . '/api/actions' . strtolower($action);
        $this->_request_fields = array('application' => $application_json);
    }

    /**
     * Send request
     * @return a Response object
     * @param input input document URL or file
     * @param request_fields array with keys in
     *  {'inputName', 'password', 'options'}
     */
    function __invoke($input, $request_fields)
    {
        $fields = array_merge($this->_request_fields, $request_fields);
        if (preg_match('(http:|https:)', strtolower($input)))
        {
            $fields['inputURL'] = $input;
        }
        else
        {
            $fields['input'] = "@$input";
            if (!array_search('inputName', $fields))
            {
                $fields['inputName'] = basename($input);
            }
        }

        $request_options = $fields['options'];
        if ($request_options)
        {
            foreach ($request_options as $option_name => $ignored)
            {
                if (!array_search($option_name, $this::$options))
                {
                    $invalid_option = 'invalid option: ' . $option_name;
                    exit($invalid_option);
                }
            }
            $fields['options'] = json_encode($request_options);
        }
        elseif ($request_options == array())
        {
            unset($fields['options']);
        }

        $curl = curl_init($this->_url);
        $http_header = array('Content-Type: multipart/form-data');
        curl_setopt($curl, CURLOPT_HTTPHEADER, $http_header);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $fields);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        $request_response = curl_exec($curl);
        $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        curl_close($curl);
        return new Response($http_code, $request_response);
    }

    /**
     * Output filename extension (string)
     */
    function output_format() { return $this->_output_format; }

    protected $_output_format;

    private $_request_fields;
    private $_url;
}


/**
 * @brief Service response
 */
class Response
{
    function __construct($http_code, $request_response)
    {
        $this->_http_code = $http_code;
        $this->_response = $request_response;
        if (!$this->ok()) $this->_not_ok();
    }

    function __toString()
    {
        return $this->ok() ? $this->output() :
            $this->error_code() . ': ' . $this->error_message();
    }

    /**
     * @return True only if http_code is 200
     */
    function ok() { return $this->http_code() == 200; }

    /**
     * @return HTTP status code (int)
     */
    function http_code() { return (int) $this->_http_code; }

    /**
     * @return Document or image data (string) if request was successful,
     *  otherwise NULL
     */
    function output() { if ($this->ok()) return $this->_response; }

    /**
     * @return NULL if successful, otherwise API
     *  [error code](https://api.datalogics-cloud.com/#errorCode) (int)
     */
    function error_code() { return $this->_error_code; }

    /**
     * @return NULL if successful, otherwise an
     *  [error message](https://api.datalogics-cloud.com/#errorMessage)
     *  (string)
     */
    function error_message() { return $this->_error_message; }

    private function _not_ok()
    {
        try
        {
            $json = json_decode($this->_response, true);
            $this->_error_code = $json['errorCode'];
            $this->_error_message = $json['errorMessage'];
        }
        catch (Exception $ignored)
        {
            # 404?
        }
    }

    private $_error_code;
    private $_error_message;
    private $_response;
}


/**
 * @brief API error codes
 */
class ErrorCode
{
    const AuthorizationError = 1;
    const InvalidSyntax = 2;
    const InvalidInput = 3;
    const InvalidPassword = 4;
    const MissingPassword = 5;
    const UnsupportedSecurityProtocol = 6;
    const InvalidOutputFormat = 7;
    const InvalidPage = 8;
    const RequestTooLarge = 9;
    const UsageLimitExceeded = 10;
    const UnknownError = 20;
}


/**
 * @brief Flatten form fields and other annotations
 */
class FlattenForm extends Request
{
    /**
     * %FlattenForm has no request options
     */
    static $options = array();

    function __construct($application, $base_url)
    {
        parent::__construct($application, $base_url);
        $this->_output_format = 'pdf';
    }
}


/**
 * @brief Create raster image representation
 */
class RenderPages extends Request
{
    /**
     * %RenderPages request options:
     * * [colorModel](https://api.datalogics-cloud.com/docs#colorModel):
     *    rgb (default), gray, rgba, or cmyk
     * * [compression](https://api.datalogics-cloud.com/docs#compression):
     *    lzw (default) or jpg
     * * [disableColorManagement]
     *    (https://api.datalogics-cloud.com/docs#disableColorManagement):
     *    for downstream color management (rarely used)
     * * [disableThinLineEnhancement]
     *    (https://api.datalogics-cloud.com/docs#disableThinLineEnhancement)
     *    for high-resolution output (rarely used)
     * * [imageHeight](https://api.datalogics-cloud.com/docs#imageHeight):
     *    pixels
     * * [imageWidth](https://api.datalogics-cloud.com/docs#imageWidth):
     *    pixels
     * * [OPP](https://api.datalogics-cloud.com/docs#OPP): overprint preview
     * * [outputFormat](https://api.datalogics-cloud.com/docs#outputFormat):
     *    png (default), gif, jpg, or tif
     * * [pages](https://api.datalogics-cloud.com/docs#pages):
     *    default = 1
     * * [pdfRegion](https://api.datalogics-cloud.com/docs#pdfRegion):
     *    crop (default), art, bleed, bounding, media, or trim
     * * [printPreview](https://api.datalogics-cloud.com/docs#printPreview):
     *    ignored if suppressAnnotations is true
     * * [resolution](https://api.datalogics-cloud.com/docs#resolution):
     *    12 to 2400 (default = 150)
     * * [smoothing](https://api.datalogics-cloud.com/docs#smoothing):
     *    all (default), none, or text
     * * [suppressAnnotations]
     *    (https://api.datalogics-cloud.com/docs#suppressAnnotations):
     *    draw only actual page contents
     */
    static $options = array(
        'colorModel', 'compression',
        'disableColorManagement', 'disableThinLineEnhancement',
        'imageHeight', 'imageWidth',
        'OPP', 'outputFormat',
        'pages', 'pdfRegion',
        'printPreview', 'resolution',
        'smoothing', 'suppressAnnotations');

    /**
     * Send request
     * @return a Response object
     * @param input input document URL or file
     * @param request_fields array with keys in
     *  {'inputName', 'password', 'options'}
     */
    function __invoke($input, $request_fields)
    {
        $output_format = $request_fields['outputFormat'];
        $this->_output_format = $output_format ? $output_format : 'png';
        return parent::__invoke($input, $request_fields);
    }
}


namespace pdfclient\FlattenForm;

/**
 * @brief Error codes for FlattenForm requests
 */
class ErrorCode extends \pdfclient\ErrorCode
{
    const NoAnnotations = 21;
}

namespace pdfclient\RenderPages;

/**
 * @brief Error codes for RenderPages requests
 */
class ErrorCode extends \pdfclient\ErrorCode
{
    const InvalidColorModel = 31;
    const InvalidCompression = 32;
    const InvalidRegion = 33;
    const InvalidResolution = 34;
}
?>
