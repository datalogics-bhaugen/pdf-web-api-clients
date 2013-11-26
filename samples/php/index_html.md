<!-- this prevents Doxygen from putting excess space at the top of the page -->
### 0. Client Dependency

* PHP 5.3 or higher

### 1. Download Sample Files

* [Client](download/pdfclient.php) module
* Command line [script](download/pdfprocess.php)
(demonstrates client module usage)

### 2. Get Application Key

* Get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/).
* To use the command line script, copy these values into it.
(Search for TODO comments.)

### 3. Send %Request

* Make a request factory

        $api_client = new \pdfclient\Application('your app id', 'your app key');

* Make a request

        $api_request = $api_client->make_request('RenderPages');

* Set request options

        $options = array('outputFormat' => 'jpg', 'printPreview' => true);

* Send request 

        $input = 'hello_world.pdf';
        $request_fields = array('inputName' => $input, 'options' => $options);
        $api_response = $api_request($input, $request_fields);

### 4. Interpret %Response

* %Response properties are initialized according to the returned HTTP
status code.

        if ($api_response->ok())
        {
            assert('$api_response->http_code() == 200');
            # $api_response->output() is the requested document or image.
            assert('$api_response->error_code() == NULL');
            assert('$api_response->error_message() == NULL');
        }
        else
        {
            assert('$api_response->http_code() != 200');
            assert('$api_response->output() == NULL');
            assert('$api_response->error_code() != NULL');
            assert('$api_response->error_message() != NULL');
        } <!-- force Doxygen to print this brace -->

