Datalogics PDF WebAPI provides secure, cloud-based PDF processing using
Adobe and Datalogics PDF technologies. This is a RESTful service for the
internet developer community that currently provides:

* Flattening PDF form fields and other annotations using the Adobe PDF Java Toolkit
* Rendering of PDF files using the Adobe PDF Library and Datalogics PDF2IMG technologies

### Application Key

To use this service, first get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/).
Then, you may address requests to our service:

    https://pdfprocess.datalogics-cloud.com/api

Each application ID has a usage limit, currently 10 requests per minute.

### Service Interface

This is a summary of the interface. For a detailed description, please visit our
<a href="https://api.datalogics-cloud.com/docs">developer portal</a>
or look at our [example](#example).

#### Request Types

A request type is two words separated by a slash, e.g. `flatten/form`.
There is one service URL per request type, e.g.

    https://pdfprocess.datalogics-cloud.com/api/actions/flatten/form

#### Request Form

A request is a POST method with form data:

* [application](https://api.datalogics-cloud.com/docs#application) is a JSON value identifying your application, e.g. {"id": yourID, "key": yourKey}
* _Optional values:_
    - [inputURL](https://api.datalogics-cloud.com/docs#inputURL) identifies the input document that the server should process
    - If there is no inputURL, put the input document in the request body (Content-Type: application/pdf)
    - [inputName](https://api.datalogics-cloud.com/docs#inputName) helps identify the request in the service's request log
    - [password](https://api.datalogics-cloud.com/docs#password) must be supplied if the document is password-protected
    - [options](https://api.datalogics-cloud.com/docs#options) is a JSON value containing options for the request type specified by the service URL

<a name="example"/>
#### Request Example

This [example](examples/renderPages.txt) is a request for an image of the first page of a _hello world_ document. It was sent by our sample Python client.

#### Service Response

If the request was successful, the message body of the HTTP response is the requested document or image. Otherwise, the message body is a JSON value:

* [errorCode](https://api.datalogics-cloud.com/docs#errorCode) is an integer code identifying the error
* [errorMessage](https://api.datalogics-cloud.com/docs#errorMessage) is a string describing the error

### Sample Clients

To facilitate using this service, we supply two sample clients:

* For Perl, download this [script](pdfprocess_8pl_source.html). After copying your API key into it, you can use its command-line interface to send requests. This client has the following dependencies:
    * HTTP::Request::Common
    * JSON
    * LWP::UserAgent

* For Python, download this [client](pdfclient_8py_source.html) module and [script](pdfprocess_8py_source.html). After copying your API key into the script, you can use its command-line interface to send requests. This client has the following dependencies:
    * Python 3.3 or 2.7 (other versions might work, but are not supported)
    * [Requests](http://docs.python-requests.org/en/latest/): HTTP for Humans
    * [simplejson](http://simplejson.readthedocs.org/en/latest/): JSON encoder and decoder

### Resources

* [PDF2IMG](http://www.datalogics.com/products/pdf2img/)
* [PDFJT](http://www.datalogics.com/products/pdfjt/)

