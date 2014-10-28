var uriString = new Windows.Foundation.Uri("https://pdfprocess.datalogics.com/api/actions/decorate/document");

var httpClient = new Windows.Web.Http.HttpClient();
var httpPromise;
var temp;

httpClient.defaultRequestHeaders.append("user-agent", "python-requests/2.0.1 CPython/2.7.5 Darwin/13.0.0");
httpClient.defaultRequestHeaders.append("Accept", "*/*");
httpClient.defaultRequestHeaders.append("Accept-Encoding", "gzip, deflate, compress");
var requestContent = new Windows.Web.Http.HttpMultipartFormDataContent();

requestContent.add(new Windows.Web.Http.HttpStringContent(
    "{\"id\":\"INSERT ID HERE!!!\", \"key\":\"INSERT KEY HERE!!!\"}"), "application");

/*temp = new Windows.Storage.StorageFile.getFileFromPathAsync(
    "C:\Users\cstock\Documents\ScenariosOfWorkingWithDLE.pdf").done.then(function (file) {
        requestContent.add(new Windows.Web.Http.HttpStreamContent(file.openReadAsync), "input");
    });*/

var folderPicker = new Windows.Storage.Pickers.FolderPicker();
folderPicker.fileTypeFilter.replaceAll(["*"]);
folderPicker.pickSingleFolderAsync("C:\Users\cstock\Documents\Visual Studio 14\Projects\\").then(function (allowedFolder) {
    
    temp = allowedFolder.getFileAsync("ScenariosOfWorkingWithDLE.pdf").then(function (pdfFile) {
        pdfFile.openReadAsync().then(function (pdfData) {
            requestContent.add(new Windows.Web.Http.HttpStreamContent(pdfData), "input");


            Debug.writeln("Yello?");
        });
    });

    temp2 = allowedFolder.getFileAsync("AllPages.xml").then(function (decoFile) {
        decoFile.openReadAsync().then(function (decoData) {
            requestContent.add(new Windows.Web.Http.HttpStreamContent(decoData), "decorationData");

            doPost();
        });
    });

});

function doPost() {
    Debug.writeln("Posting");
    httpPromise = httpClient.postAsync(uriString, requestContent).then(function (response) {
        outputStatus = response.statusCode + " " + response.reasonPhrase;
        Debug.writeln(outputStatus);

        response.content.readAsStringAsync().then(function (responseBodyAsText) {
            // Format the HTTP response to display better
            responseBodyAsText = responseBodyAsText.replace(/<br>/g, "\r\n");

            Debug.writeln(responseBodyAsText);
            return response;

        });
    });
}
