Certainly! Here's an updated version of the `readme.md` file with improved formatting and additional examples:

```markdown
# Web Scraping API Documentation

Welcome to the documentation for our Web Scraping API. This guide will provide you with all the necessary information to integrate and utilize our API effectively. Whether you're a seasoned developer or just getting started with web scraping, this documentation will help you leverage the power of our API to retrieve valuable data from websites.

## Table of Contents

1. [Introduction](#introduction)
2. [Endpoint](#endpoint)
3. [Request Parameters](#request-parameters)
4. [Response Format](#response-format)
5. [Error Handling](#error-handling)
6. [Examples](#examples)
7. [Rate Limiting](#rate-limiting)
8. [Support](#support)

## Introduction

Our Web Scraping API allows you to retrieve data from websites in a structured and automated manner. By sending HTTP requests to our API endpoint, you can specify the target URL and define the elements you want to extract from the webpage. The API will process your request and return the extracted data in a convenient format.

## Endpoint

The base URL for our Web Scraping API is:

```
https://beautiful-scrape.vercel.app/api/scrap
```

## Request Parameters

The API supports both GET and POST requests. The following parameters should be included in your requests:

1. `url` (string, required): The URL of the website you want to scrape.
2. `arguments` (array, required): An array of objects specifying the BeautifulSoup arguments to extract the desired data.

### Arguments Object

Each argument object can have one of the following structures:

1. Attribute Name:
   ```json
   {
     "attribute_name": "name"
   }
   ```

   Example: Extract the text content of a `<span>` tag with class "text".
   ```json
   {
     "find_all": ["span", { "class": "text" }]
   }
   ```

2. Method:
   ```json
   {
     "method_name": ["arg1", "arg2", ...],
     "at_element": [
       {
         "method_name": ["arg1", "arg2", ...]
       },
       ...
     ]
   }
   ```

   Example: Extract the author name and tags associated with each quote.
   ```json
   {
     "find_all": ["div", { "class": "quote" }],
     "at_element": [
       {
         "find": ["span", { "class": "author" }]
       },
       {
         "find_all": ["a", { "class": "tag" }]
       }
     ]
   }
   ```

3. List:
   ```json
   [
     "arg1",
     "arg2",
     ...
   ]
   ```

   Example: Extract the attribute values of all `<a>` tags.
   ```json
   [
     "find_all",
     ["a"],
     ["get", "href"]
   ]
   ```

## Response Format

The API will return the extracted data in JSON format. The structure of the response will depend on the specified arguments.

Example response for extracting quotes from `quotes.toscrape.com`:
```json
[
  [
    "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”",
    "Albert Einstein"
  ],
  [
    "“It is our choices, Harry, that show what we truly are, far more than our abilities.”",
    "J.K. Rowling"
  ],
  ...
]
```

## Error Handling

If an error occurs during the

 scraping process or if the request is invalid, the API will return an error response in the following format:

```json
{
  "error": "Error message here"
}
```

## Examples

### GET Request Example

Retrieve the text content of a `<span>` tag with class "text" from `quotes.toscrape.com`.

```
