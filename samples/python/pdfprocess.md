The Datalogics PDF Web API provides secure, cloud-based PDF processing using
Adobe and Datalogics PDF technologies. This is a RESTful service for the
internet developer community that currently provides:

* Rendering of PDF files using the Adobe PDF Library and Datalogics
[PDF2IMG](http://www.datalogics.com/products/pdf2img/index.asp) technologies

### API Key

To use this service, first get an API key from
[3scale](http://datalogics-cloud.3scale.net/). Then, you may address
image service requests to this URL:

    https://pdfprocess.datalogics-cloud.com/0/actions/image

### Sample Client

To facilitate using this service, we supply a sample Python
[script](pdf2img_8py_source.html) and [client](classpdfclient_1_1_client.html)
module. After downloading these files and copying your API key into the script,
you can use the script's command-line interface to request images.

This sample has the following dependencies:

* Python 3.3 or 2.7 (other versions might work, but are not supported)
* [Requests](http://docs.python-requests.org/en/latest/): HTTP for Humans (1.2.3)

### Service Interface

This is a summary of the interface. For a detailed description, please review our sample client or visit our 3scale
<a href="https://datalogics-cloud.3scale.net/docs">developer portal</a>.

#### Request

A request is a HTTP POST method. The message body is the request document,
and the request parameters are encoded as form data.

* Use the _apiKey_ parameter to specify the API key.
* Any request options are encoded as JSON in the optional _options_ parameter.
* When the optional _inputName_ parameter is supplied, the server uses it when logging the request.
* For image requests, use the optional _outputForm_ parameter to specify the image format (default=TIFF).

Here is an [example of a request](examples/request.txt).

#### Response

The message body of the HTTP response is a JSON object:

* _processCode_ (int) is 0 if the request was successful, or a nonzero code identifying the error.
* _output_ (string) contains base64-encoded data if the request was successful, or information about the error.

Here is an [example of a response](examples/response.txt).

### Resources

* [3scale](http://3scale.net): API Management
* [PDF2IMG](http://www.datalogics.com/products/pdf2img/index.asp)

