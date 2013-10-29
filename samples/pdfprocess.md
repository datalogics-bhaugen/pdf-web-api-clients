Datalogics PDF WebAPI provides secure, cloud-based PDF processing using
Adobe and Datalogics PDF technologies. This is a RESTful service for the
internet developer community that currently provides:

* Flattening PDF form fields and other annotations using the Adobe PDF Java Toolkit
* Rendering of PDF files using the Adobe PDF Library and Datalogics PDF2IMG technologies

### Application Key

To use this service, first get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/).

### Request Types

* [FlattenForm](classpdfclient_1_1_flatten_form.html)
* [RenderPages](classpdfclient_1_1_render_pages.html)

### Service Response

If the request was successful, the message body of the
[response](classpdfclient_1_1_response.html) is the requested document or image.
Otherwise, the message body is a JSON value.

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

