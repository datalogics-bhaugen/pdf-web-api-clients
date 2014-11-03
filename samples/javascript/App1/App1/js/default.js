var uriString = new Windows.Foundation.Uri("https://pdfprocess.datalogics.com/api/actions/decorate/document");
var httpClient = new Windows.Web.Http.HttpClient();

//give some extra time for the response to be printed out
setTimeout(function () { Debug.writeln("Finished") }, 20000);

//call addContent, using the doPost method as our callback
addContent(doPost);

/*
* This method builds a multipart form-data request. It will contain
* an application part, a PDF part, and a decorationData part (as
* I am demo-ing using the DecorateDocument request). Once the 
* request is built, it will get sent off in a POST, which is signaled
* via callback.
*/
function addContent(callback) {
    //Adding headers
    httpClient.defaultRequestHeaders.append("user-agent", "python-requests/2.0.1 CPython/2.7.5 Darwin/13.0.0");
    httpClient.defaultRequestHeaders.append("Accept", "*/*");
    httpClient.defaultRequestHeaders.append("Accept-Encoding", "gzip, deflate, compress");

    //creating multipart form-data request part that all parts get added to
    var requestContent = new Windows.Web.Http.HttpMultipartFormDataContent();

    //add app id and key
    requestContent.add(new Windows.Web.Http.HttpStringContent(
        "{\"id\":\"APP ID HERE\", \"key\":\"APP KEY HERE\"}"), "application");

    //You need permission to access the files in certain folders, hence the use
    //of FolderPicker. There are probably other classes that will achieve this
    //as well. 
    var folderPicker = new Windows.Storage.Pickers.FolderPicker();
    folderPicker.fileTypeFilter.replaceAll(["*"]);
    //picking the folder that contains the input files
    folderPicker.pickSingleFolderAsync("ABSOLUTE PATH TO INPUT FILES HERE").then(function (allowedFolder) {

        //grab the pdf
        var temp = allowedFolder.getFileAsync("inputPDF.pdf").then(function (pdfFile) {
            //open the pdf for reading
            pdfFile.openReadAsync().then(function (pdfData) {

                //add an "input" part to our request, where the data is from a PDF. 
                requestContent.add(new Windows.Web.Http.HttpStreamContent(pdfData), "input", "inputPDF.pdf");

                //grab the decoration data file
                var temp2 = allowedFolder.getFileAsync("decorationData.xml").then(function (decoFile) {
                    //open the decoration file for reading
                    decoFile.openReadAsync().then(function (decoData) {
                        //add a "decorationData" part to our request, where the data is an xml or json file
                        requestContent.add(new Windows.Web.Http.HttpStreamContent(decoData), "decorationData", "decorationData.xml");

                        //call doPost() with our completed requestContent multipart
                        callback(requestContent);
                    });
                });
            });
        });
    });
}

/*
* This method sends a post request to the url listed at the top of this JS file
* containing the requestContent multipart, which holds all the input file data. 
* It then prints out the response status and the response data. 
*/
function doPost(requestContent) {

    //Post the request content to the specified url
    var httpPromise = httpClient.postAsync(uriString, requestContent).then(function (response) {
        outputStatus = response.statusCode + " " + response.reasonPhrase;
        Debug.writeln(outputStatus);

        response.content.readAsStringAsync().then(function (responseBodyAsText) {
            //Format the HTTP response to display better
            responseBodyAsText = responseBodyAsText.replace(/<br>/g, "\r\n");

            //may be truncated in console due to length; recommend writing to file
            Debug.writeln(responseBodyAsText);
            return response;
        });
    });
}

