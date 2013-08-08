The Datalogics PDF API is a RESTful interface that provides secure,
cloud-based PDF processing capability based on the Adobe PDF Library.
The first release of this service implements the features of our
[PDF2IMG](http://www.datalogics.com/products/pdf2img/index.asp) product.

To use this service, first get an API key from
[3scale](http://datalogics-cloud.3scale.net/). Then, you may address
image service requests to this URL:

    https://api.pdfprocess.datalogics-cloud.com/0/actions/image

To facilitate using this service, we supply a sample Python
[script](classpdf2img_1_1_p_d_f2_i_m_g.html) and
[client](classpdfclient_1_1_client.html) module.

### Dependencies

* Python 3.3 or 2.7 (other versions might work, but are not supported)
* [Requests](http://docs.python-requests.org/en/latest/): HTTP for Humans (1.2.3)
* [3scale](http://3scale.net): API Management

### Resources

* [PDF2IMG](http://www.datalogics.com/products/pdf2img/index.asp)

