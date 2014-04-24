<?php

include ("decorateDocument.php");

const BASE_URL = 'http://localhost:8080';
//const BASE_URL = 'https://pdfprocess-test.datalogics-cloud.com';
const APP_INFO = '{"id": "84445ec0", "key": "2d3eac77bb3b9bea69a91e625b9241d2"}';

function run($args)
{
    
    $deco_request = new DecorateDocument(APP_INFO, BASE_URL);

    $deco_request->create_request($args);
}

$reponse = run($argv);

?>