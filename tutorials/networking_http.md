# HTTP Protocol

## Overview

The **Hypertext Transfer Protocol (HTTP)** is an application-level protocol that is being widely used over the Web.
HTTP is a **request/response** protocol, which means, the client sends a request to the server (request method, URI, protocol version, followed by headers, and possible body content). 
The server responds (status code line, a success or error code, followed by server headers information, and possible entity-body content).

![][http-req-res]

Under the hood, HTTP requests and responses are sent over a TCP socket with default port 80 (on the server side). The HTTP client first initiates a TCP connection with the server, once the connection is established, the client and the server access TCP through their respective socket interfaces.
Servers should be able to handle thousands of simultaneous TCP connections.

Here we see one of the great advantages of the layered architecture of the OSI model — HTTP doesn't need to worry about data loss and integrity. 
This is the job of TCP and other protocols in lower layers.

HTTP is said to be a **stateless protocol**.
The server sends the requested content to clients without storing any information about the client. If a particular client sends the same request twice in a period of a few seconds, the server does not respond by saying that it just served the same request to the client. 
Instead, the server re-sends the data, as it has completely forgotten what it did earlier.

Nevertheless, although HTTP itself is stateless by design, most modern servers have a complex backend logic that stores information about logged-in clients, and by this means, we can say that those servers are **stateful**.

## HTTP Request and Response

We can learn a lot by taking a closer look on a raw HTTP request and response that sent over the network:

```text
curl -v http://httpbin.org/html
```

Below is the actual raw HTTP request sent by `curl` to the server:

```text
GET /html HTTP/1.1
Host: httpbin.org
User-Agent: curl/7.58.0
Accept: */*
```

The server response is:

```text
HTTP/1.1 200 OK
Date: Wed, 05 Apr 2023 12:43:42 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 3741
Connection: keep-alive
Server: gunicorn/19.9.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

<!DOCTYPE html>
<html>
  <head>
....
```

The MDN web docs [specify the core components of request and response objects](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview#http_flow), review this resource.

## Status code

HTTP response status codes indicate how a specific HTTP request was completed.

Responses are grouped in five classes:

- Informational (100–199)
- Successful (200–299)
- Redirection (300–399)
- Client error (400–499)
- Server error (500–599)

Try yourself to perform the below two HTTP requests, and [read](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) about the meaning of each status code.

```bash
curl -i httpbin.org/status/0
curl -v -X PUT httpbin.org/path/to/nowhere
```

## Flask webserver

So far we've seen how to communicate with a server as **clients**.

The below exercise demonstrates how a **server** might look and operate.

We'll run a simple Python server based on a Python package called [Flask](https://flask.palletsprojects.com/en/3.0.x/quickstart/), and communicate with the server locally from the same machine.

1. Fork and clone the [NetflixMovieCatalog][NetflixMovieCatalog] repo, which is an app containing a sample movie catalog API.

> [!NOTE]
> An **API (Application Programming Interface)** can be thought of as a collection of all server endpoints that together define the functionality that is exposed to the client.
> Each endpoint typically accepts input parameters in a specific format and returns output data in a standard format such as JSON or XML.
> For example, a web API for a social media platform might include endpoints for retrieving a user's profile information, posting a new status update, or searching for other users. 
> Each endpoint would have a unique URL and a specific set of input parameters and output data.
> Many platforms expose both API, and GUI.

2. If haven't done yet, create a Python virtual environment (**venv**) in your cloned repo project.
3. Open up a Terminal session in your IDE (e.g. PyCharm). Make sure the venv is activated in the opened terminal. 
4. Install the flask package by: `pip install flask`.
5. Run the server by: `python app.py`
6. The default endpoint `/` can be accessed via your web browser or using `curl`.


Take a closer look at the output you've got from the `/discover` endpoint, this is the so-called JSON format.

**JavaScript Object Notation (JSON)** is a standard text-based format for representing structured data based on JavaScript object syntax. 
It is commonly used for transmitting data in web applications. JSON can be used independently from JavaScript, and many programming environments feature the ability to read and generate JSON.

# Exercises

### :pencil2: `Accept` header

1. Use `curl` to perform an HTTP GET request to `http://httpbin.org/image`.
   Add an `Accept` header to your requests to indicate that you anticipate a `png` image.
2. Read carefully the Warning message written by `curl` at the end of the server response, follow the instructions to save the image on the file system. 
3. Execute another `curl` to save the image in the file system.

Which animal appears in the served image?


### :pencil2: Status code

1. Perform an HTTP `GET` request to `google.com`
2. What does the server response status code mean? Follow the response headers and body to get the real Google's home page.
3. Which HTTP version does the server use in the above response?

### :pencil2: Connection close

The server of httpbin.org uses `keep-alive` connection by default, indicating that the server would like to keep the TCP connection open, so further requests to the server will use the same underlying TCP socket.

Perform an HTTP `POST` request to the `/anything` endpoint and tell the server that the client (you) would like to close the connection immediately after the server has responded.

Make sure the server's response contains the `Connection: close` header which means that the TCP connection used to serve the request was closed.

### :pencil2: Sending data to the server


Perform an HTTP POST request to http://httpbin.org/anything. You should send the following json to the server

```json
{
  "test": "me"
}
```

Upon success request, the response body will be a JSON format with a `json` key and your data as a value, as follows:

```json
"json": {
  "test": "me"
}
```

Bad requests would be responded by:

```text
"json": null
```

### :pencil2: Working with GitHub API

Review the official GitHub API docs on how to make requests to the API:    
https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api?apiVersion=2022-11-28#making-a-request

1. Use the API to get information about the [NetflixMovieCatalog][NetflixMovieCatalog] repository.   
   **Endpoint:** https://api.github.com/repos/{owner}/{repo}     
   **Method:** `GET`

   Use `jq` to extract and print the following information from the JSON response:

   - Repository name
   - Description
   - Star count
   - Fork count

2. Use the API to find out the most starred repository of the **Netflix** organization and print its name and star count.    
   Hint: You can use the endpoint https://api.github.com/orgs/{org}/repos to list all repositories in an organization and then `sort` by the `stargazers_count` field.


[http-req-res]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/networking_http-req-res.png
[networking_cookies]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/networking_cookies.png
[NetflixMovieCatalog]: https://github.com/exit-zero-academy/NetflixMovieCatalog.git

