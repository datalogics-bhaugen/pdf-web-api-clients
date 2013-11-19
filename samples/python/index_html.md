<!-- do not remove !-->
### 0. Client Dependencies

* Python 3.3 or 2.7: Other versions might work, but are not supported.
* [Requests](http://docs.python-requests.org/en/latest/) (HTTP for Humans):
Use a new version, e.g. 2.0.1.

### 1. Download Sample Files

* [Client](download/pdfclient.py) module
* Command line [script](download/pdfprocess.py)
(demonstrates client module usage)

### 2. Get Application Key

* Get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/).
* To use the command line script, copy these values into it.
(Search for TODO comments.)

### 3. Send Request

* Make a request factory

        api_client = pdfclient.Application('your app id', 'your app key')

* Make a request

        api_request = api_client.make_request('RenderPages')

* Set request options

        options = {'outputFormat': 'jpg', 'printPreview': True}

* Send request 

        input = 'hello_world.pdf'
        api_response = api_request(input, inputName=input, options=options)

### 4. Interpret Response

* Response properties are initialized according to returned HTTP status code

        if api_response.ok:
            assert_equal(api_response.http_code, requests.codes.ok)
            # api.response.output is the requested document or image.
            assert_is_none(api_response.error_code)
            assert_is_none(api_response.error_message)
        else:
            assert_not_equal(api_response.http_code, requests.codes.ok)
            assert_is_none(api_response.output)
            assert_is_not_none(api_response.error_code)
            assert_is_not_none(api_response.error_message)

