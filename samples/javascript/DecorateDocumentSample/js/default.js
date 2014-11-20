// For an introduction to the Blank template, see the following documentation:
// http://go.microsoft.com/fwlink/?LinkId=232509
(function () {
    "use strict";

    var app = WinJS.Application;
    var activation = Windows.ApplicationModel.Activation;

    app.onactivated = function (args) {
        if (args.detail.kind === activation.ActivationKind.launch) {
            if (args.detail.previousExecutionState !== activation.ApplicationExecutionState.terminated) {
                // TODO: This application has been newly launched. Initialize
                // your application here.
            } else {
                // TODO: This application has been reactivated from suspension.
                // Restore application state here.
            }
            args.setPromise(WinJS.UI.processAll());

            // Retrieve the button and register our event handler
            var decoDocButton = document.getElementById("decorateDocument");
            decoDocButton.addEventListener("click", buttonClickHandler, false);
        }
    };

    app.oncheckpoint = function (args) {
        // TODO: This application is about to be suspended. Save any state
        // that needs to persist across suspensions here. You might use the
        // WinJS.Application.sessionState object, which is automatically
        // saved and restored across suspension. If you need to complete an
        // asynchronous operation before your application is suspended, call
        // args.setPromise().
    };

    function buttonClickHandler(eventInfo) {
        var appID = document.getElementById("applicationID").value;
        var appKey = document.getElementById("applicationKey").value;
        addContent(appID, appKey, doPost);
        document.getElementById("displayResult").innerText = "Now decorating the document...";
    }

    /*
    * This method builds a multipart form-data request. It will contain
    * an application part, a PDF part, and a decorationData part (as
    * I am demo-ing using the DecorateDocument request). Once the 
    * request is built, it will get sent off in a POST, which is signaled
    * via callback.
    */
    function addContent(appID, appKey, callback) {
        //creating multipart form-data request part that all parts get added to
        var requestContent = new Windows.Web.Http.HttpMultipartFormDataContent();

        //add app id and key
        requestContent.add(new Windows.Web.Http.HttpStringContent(
        "{\"id\":\"" + appID + "\", \"key\":\"" + appKey + "\"}"), "application");


        //You need permission to access the files in certain folders, hence the use
        //of FolderPicker. There are probably other classes that will achieve this
        //as well. 
        var filePicker = new Windows.Storage.Pickers.FileOpenPicker();
        filePicker.fileTypeFilter.replaceAll([".pdf"]);

            //grab the pdf
            filePicker.pickSingleFileAsync().then(function (pdfFile) {
                //open the pdf for reading
                pdfFile.openReadAsync().then(function (pdfData) {

                    //add an "input" part to our request, where the data is from a PDF. 
                    requestContent.add(new Windows.Web.Http.HttpStreamContent(pdfData), "input", pdfFile.name);

                    //grab the decoration data file
                    filePicker.fileTypeFilter.replaceAll([".xml"]);
                    filePicker.pickSingleFileAsync().then(function (decoFile) {
                        //open the decoration file for reading
                        decoFile.openReadAsync().then(function (decoData) {
                            //add a "decorationData" part to our request, where the data is an xml or json file
                            requestContent.add(new Windows.Web.Http.HttpStreamContent(decoData), "decorationData", decoFile.name);

                            //call doPost() with our completed requestContent multipart
                            callback(requestContent);
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
        var uriString = new Windows.Foundation.Uri("https://pdfprocess.datalogics.com/api/actions/decorate/document");
        var httpClient = new Windows.Web.Http.HttpClient();

        //Adding headers
        httpClient.defaultRequestHeaders.append("user-agent", "python-requests/2.0.1 CPython/2.7.5 Darwin/13.0.0");
        httpClient.defaultRequestHeaders.append("Accept", "*/*");
        httpClient.defaultRequestHeaders.append("Accept-Encoding", "gzip, deflate, compress");

        //Post the request content to the specified url
        var httpPromise = httpClient.postAsync(uriString, requestContent).then(function (response) {
            var outputStatus = response.statusCode + " " + response.reasonPhrase;
            Debug.writeln(outputStatus);

            response.content.readAsBufferAsync().then(function (responseBodyAsBuffer) {
                savePDF(responseBodyAsBuffer)
                return response;
            });
        });
    }

    function savePDF(responseBody) {
        // Create the picker object and set options
        var savePicker = new Windows.Storage.Pickers.FileSavePicker();
        // Dropdown of file types the user can save the file as
        savePicker.fileTypeChoices.insert("PDF", [".pdf"]);
        // Default file name if the user does not type one in or select a file to replace
        savePicker.suggestedFileName = "outputPDF";
        
        // Open the picker for the user to pick a file
        savePicker.pickSaveFileAsync().then(function (file) {
            if (file) {
                Windows.Storage.FileIO.writeBufferAsync(file, responseBody).then(function (response) {
                    document.getElementById("displayResult").innerText = "File written"
                });
            } else {
                document.getElementById("displayResult").innerText = "User did not pick an output file";
            }
        });
    }

    // Run the app!!
    app.start();
})();
