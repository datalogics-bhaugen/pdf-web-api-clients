<?php namespace pdfclient;

# Copyright (c) 2014, Datalogics, Inc. All rights reserved.

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
    function __construct($application_json, $base_url, $url_suffix)
    {
        $this->_application = $application_json;
        $this->_url = $base_url . '/api/actions/' . $url_suffix;
    }

    /**
     * Send request
     * @return a Response object
     * @param input_files array of input filenames
     * @param request_fields array with keys in
     *  {'inputURL', 'inputName', 'password', 'options'}
     */
    function __invoke($input_files, $request_fields)
    {
        $request_fields['application'] = $this->_application;

        if (!array_key_exists('inputName', $request_fields) &&
            array_key_exists('input', $input_files))
        {
            $request_fields['inputName'] = $input_files['input'];
        }

        if (array_key_exists('options', $request_fields))
        {
            $request_options = $request_fields['options'];
            foreach ($request_options as $option_name => $ignored)
            {
                if (!in_array($option_name, $this::$Options))
                {
                    $invalid_option = 'invalid option: ' . $option_name;
                    exit($invalid_option);
                }
            }
            $request_fields['options'] = json_encode($request_options);
        }

        foreach ($input_files as $part_name => $filename)
        {
            $request_fields[$part_name] = "@$filename";
        }

        $curl = curl_init($this->_url);
        $http_header = array('Content-Type: multipart/form-data');
        curl_setopt($curl, CURLOPT_HTTPHEADER, $http_header);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $request_fields);
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

    private $_application;
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
     *  [error code]
     *   (https://api.datalogics-cloud.com/Getting-Started#ErrorMessages)
     *   (int)
     */
    function error_code() { return $this->_error_code; }

    /**
     * @return NULL if successful, otherwise an
     *  [error message]
     *   (https://api.datalogics-cloud.com/Getting-Started#ErrorMessages)
     *   (string)
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
 * @brief Export FDF, XFDF, or XML form data
 */
class ExportFormData extends Request
{
    /**
     * %ExportFormData options:
     * * [exportXFDF]
     *    (https://api.datalogics-cloud.com/docs#exportXFDF)
     *    export XFDF instead of FDF for AcroForm input
     */
    static $Options = array('exportXFDF');

    function __construct($application, $base_url)
    {
        parent::__construct($application, $base_url, "export/form-data");
    }
}


/**
 * @brief Fill form fields with supplied FDF/XFDF data
 */
class FillForm extends Request
{
    /**
     * %FillForm request options:
     * * [disableCalculation]
     *    (https://api.datalogics-cloud.com/docs#disableCalculation)
     *    do not run calculations afterward
     * * [disableGeneration]
     *    (https://api.datalogics-cloud.com/docs#disableGeneration):
     *    do not generate appearances afterward
     * * [flatten](https://api.datalogics-cloud.com/docs#flatten):
     *    flatten form afterward
     */
    static $Options = array(
        'disableCalculation', 'disableGeneration', 'flatten');

    function __construct($application, $base_url)
    {
        parent::__construct($application, $base_url, "fill/form");
        $this->_output_format = 'pdf';
    }
}


/**
 * @brief Flatten form fields
 */
class FlattenForm extends Request
{
    /**
     * %FlattenForm has no request options
     */
    static $Options = array();

    function __construct($application, $base_url)
    {
        parent::__construct($application, $base_url, "flatten/form");
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
     *    png (default), bmp, gif, jpg, or tif
     * * [pages](https://api.datalogics-cloud.com/docs#pages):
     *    default = 1
     * * [pdfRegion](https://api.datalogics-cloud.com/docs#pdfRegion):
     *    crop (default), art, bleed, bounding, media, or trim
     * * [printPreview](https://api.datalogics-cloud.com/docs#printPreview):
     *    ignored if suppressAnnotations is true
     * * [resampler](https://api.datalogics-cloud.com/docs#resampler):
     *    auto (default), bicubic, none
     * * [resolution](https://api.datalogics-cloud.com/docs#resolution):
     *    12 to 2400 (default = 150)
     * * [smoothing](https://api.datalogics-cloud.com/docs#smoothing):
     *    all (default), none, text, line, image, or comma-separated value
     * * [suppressAnnotations]
     *    (https://api.datalogics-cloud.com/docs#suppressAnnotations):
     *    draw only actual page contents
     */
    static $Options = array(
        'colorModel', 'compression',
        'disableColorManagement', 'disableThinLineEnhancement',
        'imageHeight', 'imageWidth',
        'OPP', 'outputFormat',
        'pages', 'pdfRegion',
        'printPreview', 'resampler',
        'resolution', 'smoothing',
        'suppressAnnotations');

    function __construct($application, $base_url)
    {
        parent::__construct($application, $base_url, "render/pages");
    }

    /**
     * Send request
     * @return a Response object
     * @param input input document URL or file
     * @param request_fields array with keys in
     *  {'inputURL', 'inputName', 'password', 'options'}
     */
    function __invoke($input, $request_fields)
    {
        $output_format = '';
        if (array_key_exists('options', $request_fields) &&
            array_key_exists('outputFormat', $request_fields['options']))
        {
            $output_format = $request_fields['options']['outputFormat'];
        }
        $this->_output_format = $output_format ? $output_format : 'png';
        return parent::__invoke($input, $request_fields);
    }
}


namespace pdfclient\ExportFormData;

/**
 * @brief Error codes for %ExportFormData requests
 */
class ErrorCode extends \pdfclient\ErrorCode
{
    const ExportXFDFFromXFA = 41;
}

namespace pdfclient\FillForm;

/**
 * @brief Error codes for %FillForm requests
 */
class ErrorCode extends \pdfclient\ErrorCode { }

namespace pdfclient\FlattenForm;

/**
 * @brief Error codes for %FlattenForm requests
 */
class ErrorCode extends \pdfclient\ErrorCode
{
    const NoAnnotations = 21;
}

namespace pdfclient\RenderPages;

/**
 * @brief Error codes for %RenderPages requests
 */
class ErrorCode extends \pdfclient\ErrorCode
{
    const InvalidColorModel = 31;
    const InvalidCompression = 32;
    const InvalidRegion = 33;
    const InvalidResolution = 34;
}
?>
