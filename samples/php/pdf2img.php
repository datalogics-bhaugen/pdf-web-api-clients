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
class PDF2IMG 
{
    var $base_url;
    var $application_id = 'TODO: Add Application ID';
    var $application_key = 'TODO: Add Application Key';
    var $source_file_name;
    var $destination_file_name;
    var $output_format = 'png';
    var $print_preview = FALSE;
    var $options;
  
    public function __construct() 
    { 
        $this->base_url = "https://pdfprocess.datalogics-cloud.com/api/"
                            ."actions/render/pages";
    }  
  
    public function parse_arguments($args) 
    {
        $scriptName = $args[0];
        $options = array();
        $options['outputFormat'] = $this->output_format;
        $lastElement = end($args);
        foreach ($args as $key => $index)
        {
            if ($scriptName === $index)
            {
                continue;  //script name
            }

            if (strpos($index, '-') === 0) //option
            {
                if ($index === $lastElement)
                {
                    throw new Exception('Usage: ' .$scriptName. ' [options] inputFile');
                }
                
                $index = ltrim($index, '-');

                if (strpos($index, '=') !== false)
                {
                    list($key, $value) = explode('=', $index);
                    $options[$key] = $value;
                }
                else
                {
                    $options[$index] = TRUE;
                }
            }
            else
            {
                if ($index === $lastElement)
                {
                    $this->source_file_name = $index;
                    list($this->destination_file_name, $type) 
                        = explode('.', $index);
                    if (array_key_exists('outputFormat', $options))
                    {
                        $this->destination_file_name
                            .= '.'.$options[outputFormat]; 
                    }
                    else
                    {
                        $this->destination_file_name
                            .= '.'.$this->output_format;
                    }
                }
                else
                {
                    throw new Exception('Usage: ' .$scriptName
                                        . ' [options] inputFile');
                }
            }
        }
        $this->options = json_encode($options);
    }

}

// Driver code
$pdf2img = new PDF2IMG();
$requester = new Request();
$responder = new Response();

try
{
    $pdf2img->parse_arguments($argv);
}
catch (Exception $e)
{
    echo $e->getMessage(), "\n";
    exit();
}

$prepared = $requester->prepare_request($pdf2img->source_file_name,
                                        $pdf2img->options,
                                        $pdf2img->application_id,
                                        $pdf2img->application_key);
$response = $requester->make_request($pdf2img->base_url, $prepared);
$responder->handle_response($response, $pdf2img->destination_file_name);
?>
