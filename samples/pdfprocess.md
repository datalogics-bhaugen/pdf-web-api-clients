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
or look at our [examples](#examples).

### Request

Request parameters are encoded as form data:

* The [application](https://api.datalogics-cloud.com/docs#application) parameter is a JSON object identifying your application, e.g. {"id": yourID, "key": yourKey}
* _Optional:_ Any request options are encoded as JSON in the [options](https://api.datalogics-cloud.com/docs#options) parameter
* _Optional:_ If the [inputName](https://api.datalogics-cloud.com/docs#inputName) parameter is supplied, the server uses it when logging the request

#### GET

To have the server upload the request document, send a [GET request](https://api.datalogics-cloud.com/docs/#GET) with this parameter:

* The [inputURL](https://api.datalogics-cloud.com/docs#inputURL) parameter identifies the document to be processed

#### POST

To upload the request document to the server, send a [POST request](https://api.datalogics-cloud.com/docs/#POST) with the document in the request body (Content-Type: application/pdf).

<a name="examples"/>
#### Examples

These requests were sent by our sample Python client:

* [GET](examples/GET.txt): request for the first page of the _PDF2IMG User Guide_ in JPEG format
* [POST](examples/POST.txt): request for the first page of a _hello world_ document in JPEG format

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

