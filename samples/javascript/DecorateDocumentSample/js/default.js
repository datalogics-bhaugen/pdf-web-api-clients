// Copyright (c) 2014, Datalogics, Inc. All rights reserved.
//
// This agreement is between Datalogics, Inc. 101 N. Wacker Drive, Suite 1800,
// Chicago, IL 60606 ("Datalogics") and you, an end user who downloads
// source code examples for integrating to the Datalogics (R) PDF WebAPI (TM)
// ("the Example Code"). By accepting this agreement you agree to be bound
// by the following terms of use for the Example Code.
//
// LICENSE
// -------
// Datalogics hereby grants you a royalty-free, non-exclusive license to
// download and use the Example Code for any lawful purpose. There is no charge
// for use of Example Code.
//
// OWNERSHIP
// ---------
// The Example Code and any related documentation and trademarks are and shall
// remain the sole and exclusive property of Datalogics and are protected by
// the laws of copyright in the U.S. and other countries.
//
// Datalogics and Datalogics PDF WebAPI are trademarks of Datalogics, Inc.
//
// TERM
// ----
// This license is effective until terminated. You may terminate it at any
// other time by destroying the Example Code.
//
// WARRANTY DISCLAIMER
// -------------------
// THE EXAMPLE CODE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER
// EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES
// OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
//
// DATALOGICS DISCLAIM ALL OTHER WARRANTIES, CONDITIONS, UNDERTAKINGS OR
// TERMS OF ANY KIND, EXPRESS OR IMPLIED, WRITTEN OR ORAL, BY OPERATION OF
// LAW, ARISING BY STATUTE, COURSE OF DEALING, USAGE OF TRADE OR OTHERWISE,
// INCLUDING, WARRANTIES OR CONDITIONS OF MERCHANTABILITY, FITNESS FOR A
// PARTICULAR PURPOSE, SATISFACTORY QUALITY, LACK OF VIRUSES, TITLE,
// NON-INFRINGEMENT, ACCURACY OR COMPLETENESS OF RESPONSES, RESULTS, AND/OR
// LACK OF WORKMANLIKE EFFORT. THE PROVISIONS OF THIS SECTION SET FORTH
// SUBLICENSEE'S SOLE REMEDY AND DATALOGICS'S SOLE LIABILITY WITH RESPECT
// TO THE WARRANTY SET FORTH HEREIN. NO REPRESENTATION OR OTHER AFFIRMATION
// OF FACT, INCLUDING STATEMENTS REGARDING PERFORMANCE OF THE EXAMPLE CODE,
// WHICH IS NOT CONTAINED IN THIS AGREEMENT, SHALL BE BINDING ON DATALOGICS.
// NEITHER DATALOGICS WARRANT AGAINST ANY BUG, ERROR, OMISSION, DEFECT,
// DEFICIENCY, OR NONCONFORMITY IN ANY EXAMPLE CODE.
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
        // Get the app ID and Key and add content to the PDF
        var appID = document.getElementById("applicationID").value;
        var appKey = document.getElementById("applicationKey").value;
        addContent(appID, appKey, doPost);
        document.getElementById("displayResult").innerText = "Now decorating the document...";
    }

    /*
    * This method builds a multipart form-data request. It will contain
    * an application part, a PDF part, and a decorationData part. Once the 
    * request is built, it will get sent off in a POST, which is signaled
    * via callback.
    */
    function addContent(appID, appKey, callback) {
        // Creating multipart form-data request part that all parts get added to
        var requestContent = new Windows.Web.Http.HttpMultipartFormDataContent();

        // Insert app id and key
        requestContent.add(new Windows.Web.Http.HttpStringContent(
        "{\"id\":\"" + appID + "\", \"key\":\"" + appKey + "\"}"), "application");

        // Select a PDF to decorate
        var filePicker = new Windows.Storage.Pickers.FileOpenPicker();
        filePicker.fileTypeFilter.replaceAll([".pdf"]);

            // Grab the pdf
            filePicker.pickSingleFileAsync().then(function (pdfFile) {
                if (pdfFile) {
                    // Open the pdf for reading
                    pdfFile.openReadAsync().then(function (pdfData) {

                        // Add an "input" part to our request, where the data is from a PDF. 
                        requestContent.add(new Windows.Web.Http.HttpStreamContent(pdfData), "input", pdfFile.name);

                        // Grab the decoration data file
                        filePicker.fileTypeFilter.replaceAll([".json"]);
                        filePicker.pickSingleFileAsync().then(function (decoFile) {
                            if (decoFile) {
                                // Open the decoration file for reading
                                decoFile.openReadAsync().then(function (decoData) {
                                    // Add a "decorationData" part to our request, where the data is an xml or json file
                                    requestContent.add(new Windows.Web.Http.HttpStreamContent(decoData), "decorationData", decoFile.name);

                                    // Call doPost() with our completed requestContent multipart
                                    callback(requestContent);
                                });
                            } else {
                                document.getElementById("displayResult").innerText = "User did not pick a decoration JSON file";
                            }
                        });
                    });
                } else {
                    document.getElementById("displayResult").innerText = "User did not pick an input PDF";
                }
            });
    }

    /*
     * This method sends a post request to the url listed here containing
     * the requestContent multipart, which holds all the input file data. 
     * It then prints out the response status and the response data. 
     */
    function doPost(requestContent) {
        var uriString = new Windows.Foundation.Uri("https://pdfprocess.datalogics.com/api/actions/decorate/document");
        var httpClient = new Windows.Web.Http.HttpClient();

        // Adding headers
        httpClient.defaultRequestHeaders.append("user-agent", "python-requests/2.0.1 CPython/2.7.5 Darwin/13.0.0");
        httpClient.defaultRequestHeaders.append("Accept", "*/*");
        httpClient.defaultRequestHeaders.append("Accept-Encoding", "gzip, deflate, compress");

        // Post the request content to the specified url
        var httpPromise = httpClient.postAsync(uriString, requestContent).then(function (response) {
            if (response.statusCode == 200) {
                // Save the returned PDF
                response.content.readAsBufferAsync().then(function (responseBodyAsBuffer) {
                    savePDF(responseBodyAsBuffer)
                    return response;
                });
            } else {
                // Log the error message
                var outputStatus = response.statusCode + " " + response.reasonPhrase;
                Debug.writeln(outputStatus);

                // Save the JSON output
                response.content.readAsBufferAsync().then(function (responseBodyAsBuffer) {
                    saveError(responseBodyAsBuffer)
                    return response;
                });
            }
        });
    }

    /*
     * This method obtains the content of the HTTP response and saves it
     * to a file selected by the user.
     */
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
                    document.getElementById("displayResult").innerText = "PDF file written!";
                });
            } else {
                document.getElementById("displayResult").innerText = "User did not pick an output file";
            }
        });
    }

    /*
     * This method saves the error content if the request failed.
     */
    function saveError(errorBody) {
        // Create the picker object and set options
        var savePicker = new Windows.Storage.Pickers.FileSavePicker();
        // Dropdown of file types the user can save the error output as
        savePicker.fileTypeChoices.insert("JSON", [".json"]);
        // Default file name if the user does not type one in or select a file to replace
        savePicker.suggestedFileName = "errorText";

        // Open the picker for the user to pick a file
        savePicker.pickSaveFileAsync().then(function (file) {
            if (file) {
                Windows.Storage.FileIO.writeBufferAsync(file, errorBody).then(function (response) {
                    document.getElementById("displayResult").innerText = "Error file written!";
                });
            } else {
                document.getElementById("displayResult").innerText = "User did not pick an output file";
            }
        });
    }

    // Run the app!!
    app.start();
})();
