The Datalogics PDF Web API provides secure, cloud-based PDF processing using
Adobe and Datalogics PDF technologies. This is a RESTful service for the
internet developer community that currently provides:

* Rendering of PDF files using the Adobe PDF Library and Datalogics PDF2IMG
technologies

## Application Key

To use this service, first get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/).
Then, you may address image service requests to this URL:

    https://pdfprocess.datalogics-cloud.com/api/0/actions/image

Each application ID has a usage limit, currently 10 requests per minute.

## Service Interface

This is a summary of the interface. For a detailed description, please visit our
<a href="https://api.datalogics-cloud.com/docs">developer portal</a>
or look at our [example](#example).

### Request

A request is a POST method with parameters encoded as form data:

* The [application](https://api.datalogics-cloud.com/docs#application) parameter is a JSON object identifying your application, e.g. {"id": yourID, "key": yourKey}
* _Optional:_ Use the [inputURL](https://api.datalogics-cloud.com/docs#inputURL) parameter to have the server upload the input document
* _Optional:_ If there is no inputURL, put the input document in the request body (Content-Type: application/pdf)
* _Optional:_ If the [inputName](https://api.datalogics-cloud.com/docs#inputName) parameter is supplied, the server uses it when logging the request
* _Optional:_ Any request options are encoded as JSON in the [options](https://api.datalogics-cloud.com/docs#options) parameter

<a name="example"/>
#### Example

This [example request](examples/POST.txt) is for the first page of a _hello world_ document in JPEG format. It was sent by our sample Python client.

### Response

The message body of the HTTP response is a JSON object:

* [processCode](https://api.datalogics-cloud.com/docs#processCode) is 0 if the request was successful, or a nonzero code identifying the error
* [output](https://api.datalogics-cloud.com/docs#output) contains base64-encoded data if the request was successful, or information about the error

## Sample Clients

To facilitate using this service, we supply two sample clients:

* For Perl, download this [script](examples/pdf2img.pl). After copying your API key into it, you can use its command-line interface to request images. This client has the following dependencies:
    * HTTP::Request::Common
    * JSON
    * LWP::UserAgent
    * MIME::Base64

* For Python, download this [script](pdf2img_8py_source.html) and [client](pdfclient_8py_source.html) module. After copying your API key into the script, you can use its command-line interface to request images. This client has the following dependencies:
    * Python 3.3 or 2.7 (other versions might work, but are not supported)
    * [Requests](http://docs.python-requests.org/en/latest/): HTTP for Humans
    * [simplejson](http://simplejson.readthedocs.org/en/latest/): JSON encoder and decoder

## Resources

* [PDF2IMG](http://www.datalogics.com/products/pdf2img/index.asp)

