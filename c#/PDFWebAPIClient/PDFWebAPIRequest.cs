//Copyright (c) 2014, Datalogics, Inc. All rights reserved.
//
//This agreement is between Datalogics, Inc. 101 N. Wacker Drive, Suite 1800,
//Chicago, IL 60606 ("Datalogics") and you, an end user who downloads
//source code examples for integrating to the Datalogics (R) PDF WebAPI (TM)
//("the Example Code"). By accepting this agreement you agree to be bound
//by the following terms of use for the Example Code.
//
//LICENSE
//-------
//Datalogics hereby grants you a royalty-free, non-exclusive license to
//download and use the Example Code for any lawful purpose. There is no charge
//for use of Example Code.
//
//OWNERSHIP
//---------
//The Example Code and any related documentation and trademarks are and shall
//remain the sole and exclusive property of Datalogics and are protected by
//the laws of copyright in the U.S. and other countries.
//
//Datalogics and Datalogics PDF WebAPI are trademarks of Datalogics, Inc.
//
//TERM
//----
//This license is effective until terminated. You may terminate it at any
//other time by destroying the Example Code.
//
//WARRANTY DISCLAIMER
//-------------------
//THE EXAMPLE CODE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER
//EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO THE IMPLIED WARRANTIES
//OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
//
//DATALOGICS DISCLAIM ALL OTHER WARRANTIES, CONDITIONS, UNDERTAKINGS OR
//TERMS OF ANY KIND, EXPRESS OR IMPLIED, WRITTEN OR ORAL, BY OPERATION OF
//LAW, ARISING BY STATUTE, COURSE OF DEALING, USAGE OF TRADE OR OTHERWISE,
//INCLUDING, WARRANTIES OR CONDITIONS OF MERCHANTABILITY, FITNESS FOR A
//PARTICULAR PURPOSE, SATISFACTORY QUALITY, LACK OF VIRUSES, TITLE,
//NON-INFRINGEMENT, ACCURACY OR COMPLETENESS OF RESPONSES, RESULTS, AND/OR
//LACK OF WORKMANLIKE EFFORT. THE PROVISIONS OF THIS SECTION SET FORTH
//SUBLICENSEE'S SOLE REMEDY AND DATALOGICS'S SOLE LIABILITY WITH RESPECT
//TO THE WARRANTY SET FORTH HEREIN. NO REPRESENTATION OR OTHER AFFIRMATION
//OF FACT, INCLUDING STATEMENTS REGARDING PERFORMANCE OF THE EXAMPLE CODE,
//WHICH IS NOT CONTAINED IN THIS AGREEMENT, SHALL BE BINDING ON DATALOGICS.
//NEITHER DATALOGICS WARRANT AGAINST ANY BUG, ERROR, OMISSION, DEFECT,
//DEFICIENCY, OR NONCONFORMITY IN ANY EXAMPLE CODE.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;

using Datalogics.PdfWebApi.Client;
using Datalogics.PdfWebApi.Response;

namespace Datalogics.PdfWebApi.Request
{
    /// <summary>
    /// This is the abstract base class that all PDF WebAPI requests should be derived from.  It
    /// also contains utility methods that those derived classes may need.
    /// </summary>
    public abstract class PdfWebApiRequest
    {
        /// <summary>
        /// This class specifies the data contract required to serialize an application id and key pair
        /// to and from a JSON string.
        /// </summary>
        [DataContract]
        private class Application
        {
            [DataMember(Name = "id", EmitDefaultValue = false)]
            public string Id { get; set; }
            [DataMember(Name = "key", EmitDefaultValue = false)]
            public string Key { get; set; }
        }

        public string Id { get; private set; } // Application Id
        public string Key { get; private set; } // Application Key
        public Uri Url { get; private set; } // Application Url
        // Container for the multipart content
        private Dictionary<String, List<HttpContent>> partLists = new Dictionary<string, List<HttpContent>>();

        /// <summary>
        /// Sets the reqiured authorization values that all valid requests are required to have
        /// </summary>
        /// <param name="id">The application id</param>
        /// <param name="key">The application key</param>
        /// <param name="url">The Url for the request</param>
        protected PdfWebApiRequest(string id, string key, Uri url)
        {
            Id = id;
            Key = key;
            Url = url;
        }

        /// <summary>
        /// Sets a unique part in the multicontent request
        /// </summary>
        /// <param name="content">The content of the part</param>
        /// <param name="name">The unique name of the part</param>
        protected void SetUniquePart(HttpContent content, string name)
        {
            // Remove any existing part(s) with this name
            partLists.Remove(name);
            // Insert the unique part into the part map
            partLists[name] = new List<HttpContent>();
            partLists[name].Add(content);
        }

        /// <summary>
        /// Adds a part to the multicontent request.  Additional parts with
        /// identical names may be added.
        /// </summary>
        /// <param name="content">The content of the part</param>
        /// <param name="name">The unique name of the part</param>
        protected void AddPart(HttpContent content, string name)
        {
            if (!partLists.ContainsKey(name))
                partLists[name] = new List<HttpContent>();
            partLists[name].Add(content);
        }
        
        /// <summary>
        /// Adds a unique file to the multi-part content using default octet-stream for content type.
        /// </summary>
        /// <param name="file">The file including path to add</param>
        /// <param name="name">The name to assign the part</param>
        protected void AddFilePart(string file, string name)
        {
            AddFilePart(file, name, "application/octet-stream", true);
        }

        /// <summary>
        /// Adds a unique file to the multi-part content.
        /// </summary>
        /// <param name="file">The file including path to add</param>
        /// <param name="name">The name to assign the part</param>
        /// <param name="contentType">The content type for this file</param>
        protected void AddFilePart(string file, string name, string contentType)
        {
            AddFilePart(file, name, contentType, true);
        }

        /// <summary>
        /// Adds a file to the multi-part content.
        /// </summary>
        /// <param name="file">The file including path to add</param>
        /// <param name="name">The name to assign the part</param>
        /// <param name="contentType">The content type for this file</param>
        /// <param name="isUnique">Specifies if the part should be unique</param>
        protected void AddFilePart(string file, string name, string contentType, bool isUnique)
        {
            FileInfo fileInfo = new FileInfo(file);
            if (fileInfo.Exists)
            {
                ContentDispositionHeaderValue contentDisposition = new ContentDispositionHeaderValue("form-data");
                contentDisposition.Name = name;
                contentDisposition.FileName = fileInfo.Name;
                
                StreamContent streamContent = new StreamContent(fileInfo.OpenRead());
                streamContent.Headers.ContentType = new MediaTypeHeaderValue(contentType);
                streamContent.Headers.ContentDisposition = contentDisposition;
                
                if (isUnique)
                    SetUniquePart(streamContent, name);
                else
                    AddPart(streamContent, name);
            }
        }

        /// <summary>
        /// This utility method sets the input pdf file for the request.  Derived classes should
        /// only use this method if their request requires an input pdf file.
        /// </summary>
        /// <param name="pdfFile">The Pdf file to set</param>
        public void SetInputFile(string pdfFile)
        {
            SetInputFile(pdfFile, null, null);
        }

        /// <summary>
        /// This utiltiy method sets the input pdf file for the request and the inputName part.
        /// Derived classes should only use this method if their request requires an input pdf file.
        /// </summary>
        /// <param name="pdfFile">The Pdf file to set</param>
        /// <param name="inputName">Optional name to give this input</param>
        public void SetInputFile(string pdfFile, string inputName)
        {
            SetInputFile(pdfFile, inputName, null);
        }

        /// <summary>
        /// This utiltiy method sets the password protected input pdf file for the request and the inputName part.
        /// Derived classes should only use this method if their request requires an input pdf file.
        /// </summary>
        /// <param name="pdfFile">The Pdf file to set</param>
        /// <param name="inputName">Optional name to give this input</param>
        /// <param name="password">The password required to access the Pdf file</param>
        public void SetInputFile(string pdfFile, string inputName, string password)
        {
            // Check if the pdfFile is accessed via the web
            if (pdfFile.StartsWith("http://", true, null) || pdfFile.StartsWith("https://", true, null))
            {
                // Ensure parts doesn't contain "input" since "input" and
                //  "inputURL" are mutually exclusive keys
                partLists.Remove("input");
                // Associate the pdfFile with the "inputURL" part
                SetUniquePart(new StringContent(pdfFile), "inputURL");
            }
            else
            {
                // Ensure parts doesn't contain "inputURL" since "input" and
                // "inputURL" are mutually exclusive parts
                partLists.Remove("inputURL");
                // Associate the pdfFile with the "input" part
                AddFilePart(pdfFile, "input");
            }
            // If the password parameter is not null or empty store the "password"
            // part and body text
            if (!String.IsNullOrEmpty(password))
            {
                SetUniquePart(new StringContent(password), "password");
            }
            // This may be a subsequent call so remove the "password" part if found
            else
            {
                partLists.Remove("password");
            }
            // If the name parameter is not null or empty store the "inputName"
            // part and text body
            if (!String.IsNullOrEmpty(inputName))
            {
                SetUniquePart(new StringContent(inputName), "inputName");
            }
            // This may be a subsequent call so remove the "inputName" part if found
            else
            {
                partLists.Remove("inputName");
            }
        }

        /// <summary>
        /// This method blocks while the request response is obtained from the PDF WebAPI server.
        /// </summary>
        /// <returns>A PdfWebApiResponse object</returns>
        public PdfWebApiResponse GetResponse()
        {
            return GetResponseAsync().Result;
        }

        /// <summary>
        /// Asynchronous request to obtain a response from the PDF WebAPI Server
        /// </summary>
        /// <returns>A PdfWebApiResponse object</returns>
        public async Task<PdfWebApiResponse> GetResponseAsync()
        {
            using (HttpClient httpClient = new HttpClient()) 
            {
                httpClient.DefaultRequestHeaders.Add("user-agent", "C# PdfWebApiClient V." + PdfWebApiClient.Version);
                return new PdfWebApiResponse(await httpClient.PostAsync(Url, BuildRequestContent()));
            }
        } 

        /// <summary>
        /// This method builds the multiform content from all of the httpcontents in the partLists
        /// </summary>
        /// <remarks>Any base class requiring additional parts should override this method and 
        /// call this base method within their override prior to adding the additional parts</remarks>
        /// <returns>An HttpContent reference to a MultiFormDataContent object</returns>
        protected virtual HttpContent BuildRequestContent()
        {
            // Create a new multi-part content container with a random 128-bit boundary
            MultipartFormDataContent requestContent = new MultipartFormDataContent(System.Guid.NewGuid().ToString());
            
            // Create the "application" JSON object { "id" : "<id>", "key" : "<key>" } part
            Application application = new Application() { Id = this.Id, Key = this.Key };
            StringContent stringContent = new StringContent(WriteJsonToString(application), Encoding.UTF8, "application/json");
            requestContent.Add(stringContent, "application");

            // Iterate over partLists and add the part(s) from each list
            // Note: outer var's type is KeyValuePair<String, List<HttpContent>>
            //       inner var's type is HttpContent
            foreach (var partList in partLists)
            {
                // Add each HttpContent part
                // Note: partList.Key is the name common to all parts in this list
                foreach (var part in partList.Value)
                {
                    requestContent.Add(part, partList.Key);
                }
            }

            return requestContent;
        }

        /// <summary>
        /// This utility method accepts a "DataContract" attributed object and produces a serialized JSON
        /// string representing the object
        /// </summary>
        /// <param name="jsonType">The "DataContract" attributed object to serialize</param>
        /// <returns>The string of the JSON serialized object</returns>
        protected static string WriteJsonToString(object jsonType)
        {
            DataContractJsonSerializer jsonSerializer = new DataContractJsonSerializer(jsonType.GetType());
            using (MemoryStream memoryStream = new MemoryStream())
            {
                jsonSerializer.WriteObject(memoryStream, jsonType);
                return Encoding.UTF8.GetString(memoryStream.ToArray());
            }
        }

        /// <summary>
        /// Debug method for viewing the multi-part content of the request.
        /// </summary>
        /// <remarks>This method is meant for debugging requests and should not be called after 
        /// a call to GetResponse() as the BuildRequestContent() will have already consumed the
        /// HttpContent and will throw an exception.
        /// Derived classes requiring more information should override this member</remarks>
        /// <returns>A string representing the multipart content of the request</returns>
        public override string ToString()
        {
            return BuildRequestContent().ReadAsStringAsync().Result;
        }
    }
}
