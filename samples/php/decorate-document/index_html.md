<!-- this prevents Doxygen from putting excess space at the top of the page -->
### 0. Client Dependency

* PHP 5.3 or higher

### 1. Download Sample Files

* DecorateDocument [Client](download/decorateDocument.php) module
* DecorateDocument Command line [script](download/decorateSample.php)
(demonstrates client module usage)

### 2. Get Application Key

* Get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/).
* To use the command line script, copy these values into it.
(Search for TODO comments.)

### 3. Send Request

* Make a request via command line

        php decorateSample.php DecorateDocument input.pdf headers_footers.xml

* A request factory is made in decorateSample.php

        $deco_request = new DecorateDocument('your app ID and key', 'URL to send requests to');

* Request from command line is passed to create_request()

        $deco_request->create_request($args);

* Response is returned as PDF data, which can be piped to an output PDF file.

        php decorateSample.php DecorateDocument input.pdf headers_footers.xml > myPDF.pdf


### 4. Interpret Response

* If an error occurs, an error code and message will be passed back instead of PDF data. 
