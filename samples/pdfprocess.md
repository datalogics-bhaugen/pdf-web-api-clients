The Datalogics PDF Web API provides secure, cloud-based PDF processing using
Adobe and Datalogics PDF technologies. This is a RESTful service for the
internet developer community that currently provides:

* Rendering of PDF files using the Adobe PDF Library and Datalogics PDF2IMG
technologies

### Application Key

To use this service, first get an application ID and key from
[3scale](http://datalogics-cloud.3scale.net/). Then, you may address
image service requests to this URL:

    https://pdfprocess.datalogics-cloud.com/api/0/actions/image

### Service Interface

This is a summary of the interface. For a detailed description, please review our sample client or visit our 3scale
<a href="https://datalogics-cloud.3scale.net/docs">developer portal</a>.

#### Request

A request is a HTTP POST method. The [request body](https://datalogics-cloud.3scale.net/docs#requestBody) is a PDF document (Content-Type: application/pdf).

The request parameters are encoded as form data.

* The [application](https://datalogics-cloud.3scale.net/docs#application) parameter is a JSON object identifying your application, e.g. {"id": yourID, "key": yourKey}.
* _Optional:_ Any request options are encoded as JSON in the [options](https://datalogics-cloud.3scale.net/docs#options) parameter.
* _Optional:_ If the [inputName](https://datalogics-cloud.3scale.net/docs#inputName) parameter is supplied, the server uses it when logging the request.

Here is an [example of a request](examples/request.txt).

#### Response

The message body of the HTTP response is a JSON object:

* [output](https://datalogics-cloud.3scale.net/docs#output) contains base64-encoded data if the request was successful, or information about the error.
* [processCode](https://datalogics-cloud.3scale.net/docs#processCode) is 0 if the request was successful, or a nonzero code identifying the error.

### Sample Clients

To facilitate using this service, we supply two sample clients:

* For Perl, download this [script](examples/pdf2img.pl). After copying your API key into it, you can use its command-line interface to request images. This client has the following dependencies:
    * HTTP::Request::Common
    * JSON
    * LWP::UserAgent
    * MIME::Base64

* For Python, download this [script](pdf2img_8py_source.html) and [client](pdfclient_8py_source.html) module. After copying your API key into the script, you can use its command-line interface to request images. This client has the following dependencies:
    * Python 3.3 or 2.7 (other versions might work, but are not supported)
    * [Requests](http://docs.python-requests.org/en/latest/): HTTP for Humans (1.2.3)
    * [simplejson](http://simplejson.readthedocs.org/en/latest/): JSON encoder and decoder

### Resources

* [3scale](http://3scale.net): API Management
* [PDF2IMG](http://www.datalogics.com/products/pdf2img/index.asp)

