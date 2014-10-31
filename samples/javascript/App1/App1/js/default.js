var uriString = new Windows.Foundation.Uri("http://10.2.4.204:8080/api/decorate/document");
//192.168.132.1
var httpClient = new Windows.Web.Http.HttpClient();

setTimeout(function () { Debug.writeln("Yo") }, 30000);
addContent(doPost);

function addContent(callback) {
    Debug.writeln("Adding content");
    httpClient.defaultRequestHeaders.append("user-agent", "python-requests/2.0.1 CPython/2.7.5 Darwin/13.0.0");
    httpClient.defaultRequestHeaders.append("Accept", "*/*");
    httpClient.defaultRequestHeaders.append("Accept-Encoding", "gzip, deflate, compress");
    var requestContent = new Windows.Web.Http.HttpMultipartFormDataContent();

    requestContent.add(new Windows.Web.Http.HttpStringContent(
        "{\"id\":\"84445ec0\", \"key\":\"2d3eac77bb3b9bea69a91e625b9241d2\"}"), "application");

    var folderPicker = new Windows.Storage.Pickers.FolderPicker();
    folderPicker.fileTypeFilter.replaceAll(["*"]);
    folderPicker.pickSingleFolderAsync("C:\Users\cstock\Documents\Visual Studio 14\Projects\\").then(function (allowedFolder) {

        var temp = allowedFolder.getFileAsync("ScenariosOfWorkingWithDLE.pdf").then(function (pdfFile) {
            pdfFile.openReadAsync().then(function (pdfData) {
                        requestContent.add(new Windows.Web.Http.HttpStreamContent(pdfData), "input");

                        Debug.writeln("Yello?");
                            
                        var temp2 = allowedFolder.getFileAsync("AllPages.xml").then(function (decoFile) {
                            decoFile.openReadAsync().then(function (decoData) {
                                    requestContent.add(new Windows.Web.Http.HttpStreamContent(decoData), "decorationData");

                                    Debug.writeln("Yello dos");
                                    requestContent.readAsStringAsync().then(function (requestData) {
                                        Debug.writeln(requestData);

                                        callback(requestContent);
                                    });
                            });
                    });
                });
            });
    });

}

function doPost(requestContent) {

    Debug.writeln("Posting");

    var httpPromise = httpClient.postAsync(uriString, requestContent).then(function (response) {
        outputStatus = response.statusCode + " " + response.reasonPhrase;
        Debug.writeln("response");
        Debug.writeln(outputStatus);

        response.content.readAsStringAsync().then(function (responseBodyAsText) {
            //Format the HTTP response to display better
            responseBodyAsText = responseBodyAsText.replace(/<br>/g, "\r\n");

            Debug.writeln(responseBodyAsText);
            return response;
        });
    })
}

