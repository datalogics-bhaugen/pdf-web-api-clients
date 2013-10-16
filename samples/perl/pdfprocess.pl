#!/usr/bin/env perl

# Copyright (c) 2013, Datalogics, Inc. All rights reserved.
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

use strict;

use HTTP::Request::Common qw(POST);
use JSON;
use LWP::UserAgent;
use MIME::Base64;

my $application_id = 'TODO: Application ID';
my $application_key = 'TODO: Application key';

my $application = {'id' => $application_id, 'key' => $application_key};
my $options = {'outputForm' => 'jpg', 'printPreview' => JSON::true};
my $input_file = $ARGV[$#ARGV];

my $content = [
    'application' => encode_json($application),
    'input' => [$input_file],
    'inputName' => $input_file,
    'options' => encode_json($options)];

my $url = 'https://pdfprocess.datalogics-cloud.com/api/actions/render/pages';
my $request = POST($url, Content_Type => 'form-data', Content => $content);

my $user_agent = LWP::UserAgent->new(ssl_opts => {verify_hostname => 0});
my $response = $user_agent->request($request)->decoded_content;

#
# Response is JSON-encoded
#
my $decoded_response = decode_json($response);
my $process_code = $decoded_response->{'processCode'};
my $output = $decoded_response->{'output'};

#
# If process code != 0, output is error message
#
if ($process_code != 0) {
    print 'ERROR: '.$process_code."\n";
    print 'Error Message: '.$output."\n";
    exit $process_code;
}

#
# If process code == 0, output is base64-encoded image
#
(my $output_file = $input_file) =~ s/.pdf/.jpg/;
open(FILE, '>', $output_file) or die "cannot open file: $!";
binmode FILE;
print FILE decode_base64($output);
close(FILE);

