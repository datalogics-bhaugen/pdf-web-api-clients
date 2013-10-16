Datalogics PDF WebAPI provides secure, cloud-based PDF processing using
Adobe and Datalogics PDF technologies. This is a RESTful service for the
internet developer community that currently provides:

* Flattening PDF form fields and other annotations using the Adobe PDF Java Toolkit
* Rendering of PDF files using the Adobe PDF Library and Datalogics PDF2IMG technologies

### Application Key

To use this service, first get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/).
Then, you may address image service requests to these URLs:

    https://pdfprocess.datalogics-cloud.com/api/actions/flatten/form
    https://pdfprocess.datalogics-cloud.com/api/actions/render/pages

Each application ID has a usage limit, currently 10 requests per minute.

### Service Interface

This is a summary of the interface. For a detailed description, please visit our
<a href="https://api.datalogics-cloud.com/docs">developer portal</a>
or look at our [example](#example).

#### Request

A request is a POST method with form data:

* [application](https://api.datalogics-cloud.com/docs#application) is a JSON value identifying your application, e.g. {"id": yourID, "key": yourKey}
* _Optional values:_
    - [inputURL](https://api.datalogics-cloud.com/docs#inputURL) identifies the input document that the server should upload
    - If there is no inputURL, put the input document in the request body (Content-Type: application/pdf)
    - [inputName](https://api.datalogics-cloud.com/docs#inputName) helps identify the request in the service's request log
    - [password](https://api.datalogics-cloud.com/docs#password) must be supplied if the document is password-protected
    - [options](https://api.datalogics-cloud.com/docs#options) is a JSON value containing any other request options 

<a name="example"/>
#### Request Example

This [example](examples/renderPages.txt) is a request for an image of the first page of a _hello world_ document. It was sent by our sample Python client.

#### Response

The message body of the HTTP response is a JSON value:

* [processCode](https://api.datalogics-cloud.com/docs#processCode) is 0 if the request was successful, or a nonzero code identifying the error
* [output](https://api.datalogics-cloud.com/docs#output) contains base64-encoded data if the request was successful, or information about the error

### Sample Clients

To facilitate using this service, we supply two sample clients:

* For Perl, download this [script](examples/pdfprocess.pl). After copying your API key into it, you can use its command-line interface to send requests. This client has the following dependencies:
    * HTTP::Request::Common
    * JSON
    * LWP::UserAgent
    * MIME::Base64

* For Python, download this [client](pdfclient_8py_source.html) module and [script](pdfprocess_8py_source.html). After copying your API key into the script, you can use its command-line interface to send requests. This client has the following dependencies:
    * Python 3.3 or 2.7 (other versions might work, but are not supported)
    * [Requests](http://docs.python-requests.org/en/latest/): HTTP for Humans
    * [simplejson](http://simplejson.readthedocs.org/en/latest/): JSON encoder and decoder

### Resources

* [PDF2IMG](http://www.datalogics.com/products/pdf2img/)
* [PDFJT](http://www.datalogics.com/products/pdfjt/)

