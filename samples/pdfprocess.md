Datalogics PDF WebAPI sample clients:

* Perl [script](pdfprocess_8pl_source.html)
* Python [client](pdfclient_8py_source.html) module and
[script](pdfprocess_8py_source.html)

### Application Key

* To use this service, first get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/).
* Copy these values into the script before running it.

### Request Classes

* Request Factory
    - [Application](classpdfclient_1_1_application.html)
* Request Types
    - [FlattenForm](classpdfclient_1_1_flatten_form.html)
    - [RenderPages](classpdfclient_1_1_render_pages.html)

### Service Response

* Success
    - [Response.output](classpdfclient_1_1_response.html#pub-methods)
    is the requested document or image.
* Failure
    - [Response.error_code](classpdfclient_1_1_response.html#pub-methods)
    and error_message describe the error.

### Dependencies

* Python 3.3 or 2.7: Other versions might work, but are not supported.
* [Requests](http://docs.python-requests.org/en/latest/) (HTTP for Humans):
Use a new version, e.g. 2.0.1.

