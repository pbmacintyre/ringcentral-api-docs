# Handling asynchronous responses from the Artificial Intelligence API

The Artificial Intelligence API operates in an asynchronous manner. Meaning the results of its operations are not returned in the HTTP response associated with the HTTP request performing the operation. Instead, developers specific a URL in their request, and when the operation completes, the response payload will be posted to the specified URL. 

Th asynchronous nature of the Artificial Intelligence API requires developers to setp a simple web server in order to process results and run sample code in this Developer Guide. Below, you will find simple web servers in a variety of languages to help you in this process. 

## Passing the `webhook` parameter in your requests

Many endpoints in the Artificial Intelligence API take as input a query parameter called `webhook`. When you pass a URL to the API via this query parameter, the server will then transmit the results of the corresponding operation to the provided URL when the operation completes. This will allow the server to process the operation in the background without tying up resources in the process. 

### Correlating requests and responses

When processing files asynchronously, it is important to correlate every request with the proper response, as there is no guarantee in which order a response will be received. To help with this, a `jobId` is returned in the response body of every request, like so:

```json
{"jobId":"a919924e-ce4e-11ed-xxxx-0050568c48bc"}
```

You should parse this response, and store the jobId associated with the media file being processed so that you can reliably associate the response that will come later to the file for which it pertains. 

## Working with asynchronous responses in development

### Install and setup ngrok

If you are doing development on your local laptop, or on a machine that is not publicly accessible on the Internet, then we recommend you download and install [ngrok](https://ngrok.com/download) if you have not already. Once installed, start your ngrok server and make note of its https URL. You will need to use this URL later when specifying the `webhook` in Artificial Intelligence API requests. 

```bash
$ ngrok http 5000
  Forwarding https://xxx-yyy-zzz.ngrok.io -> https://localhost:5000
```

### Create and start a simple web server

Create a file called `server.js` using the contents below. Edit `server.js` to properly reference the `NGROK_URL` generated in the previous step.

=== "Javascript"

    ```js
    {!> code-samples/ai/quick-start-server.js !}
    ```

    Finally, start your server.

    ```bash
    $ node server.js
    ```

=== "Python"

    ```python
    {!> code-samples/ai/quick-start-server.py !}
    ```

    Finally, start your server.

    ```bash
    $ node server.py
    ```

With your web server up and running, and a way to route requests to it via ngrok, you are now ready to run code samples. 