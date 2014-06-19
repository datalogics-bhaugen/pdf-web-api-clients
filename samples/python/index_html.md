<!-- this prevents Doxygen from putting excess space at the top of the page -->
### 0. Client Dependencies

* Python 3.3 or 2.7: Other versions might work, but are not supported
* [Requests](http://docs.python-requests.org/en/latest/) (HTTP for Humans):
Use a new version, e.g. 2.3

### 1. Get Application ID and Key

* Get an application ID and key from our
[developer portal](http://api.datalogics-cloud.com/)

### 2. Download Sample Files

* [pdfclient](download/pdfclient.py) client module
* [pdfprocess](download/pdfprocess.py) command line script
(demonstrates pdfclient usage)
* To use this script, copy your application ID and key into it.
(Search for TODO comments.)

### 3. Use pdfclient to Send Request

* Make a request factory

        api_client = pdfclient.Application('your app id', 'your app key')

* Make a request

        api_request = api_client.make_request('RenderPages')

* Set request options

        options = {'outputFormat': 'jpg', 'printPreview': True}

* Send request 

        input = 'hello_world.pdf'
        files = {'input': open(input, 'rb')}
        api_response = api_request(files, inputName=input, options=options)

### 4. Interpret Response

* Response properties are initialized according to the returned HTTP
status code.

        if api_response.ok:
            assert api_response.http_code == requests.codes.ok
            # api_response.output is the requested document or image.
            assert api_response.error_code is None
            assert api_response.error_message is None
        else:
            assert api_response.http_code != requests.codes.ok
            assert api_response.output is None
            assert api_response.error_code
            assert api_response.error_message

