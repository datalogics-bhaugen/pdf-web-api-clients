The Datalogics PDF API is a RESTful interface that provides secure,
cloud-based PDF processing capability using the Adobe PDF Library.
The first release of this service implements the features of our
[PDF2IMG](http://www.datalogics.com/products/pdf2img/index.asp) product.

### API Key

To use this service, first get an API key from
[3scale](http://datalogics-cloud.3scale.net/). Then, you may address
image service requests to this URL:

    https://api.pdfprocess.datalogics-cloud.com/0/actions/image

### Sample Client

To facilitate using this service, we supply a sample Python
[script](pdf2img_8py_source.html) and [client](classpdfclient_1_1_client.html)
module. After downloading these files and copying your API key into the script,
you can use the script's command-line interface to request images.

This sample has the following dependencies:

* Python 3.3 or 2.7 (other versions might work, but are not supported)
* [Requests](http://docs.python-requests.org/en/latest/): HTTP for Humans (1.2.3)

### Service Interface

#### Request

A request is a HTTP POST method. The message body is the request document,
and the request parameters are encoded as form data.

* Any request options are encoded as JSON in the optional _options_ parameter.
* To facilitate logging, please provide the optional _inputName_ parameter.
* For image requests, use the optional _outputForm_ parameter to specify the image format (default=TIFF).

Example:

    TODO: under construction

#### Response

The message body of the HTTP response is a JSON object:

* _processCode_ (int) is 0 if the request was successful, or a nonzero code identifying the error.
* _output_ (string) contains base64-encoded data if the request was successful, or information about the error.

Example:

    TODO: under construction

### Resources

* [3scale](http://3scale.net): API Management
* [PDF2IMG](http://www.datalogics.com/products/pdf2img/index.asp)

