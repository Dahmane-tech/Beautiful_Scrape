# Web Scraping API Documentation

Welcome to the documentation for our Web Scraping API. This guide will provide you with all the necessary information to integrate and utilize our API effectively. Whether you're a seasoned developer or just getting started with web scraping, this documentation will help you leverage the power of our API to retrieve valuable data from websites.

## Table of Contents

1. [Introduction](#introduction)
2. [Endpoint](#endpoint)
3. [Request Parameters](#request-parameters)
4. [Response Format](#response-format)
5. [Error Handling](#error-handling)
6. [Examples](#examples)

## Introduction

Our Web Scraping API allows you to retrieve data from websites in a structured and automated manner. By sending HTTP requests to our API endpoint, you can specify the target URL and define the elements you want to extract from the webpage. The API will process your request and return the extracted data in a convenient format.

## Endpoint

The base URL for our Web Scraping API is:

```
https://beautiful-scrape.vercel.app/api/scrap
```

## Request Parameters

The API supports both GET and POST requests. The following parameters should be included in your requests:

1. **POST Request:**
   - Send a `POST` request to the following URL:
   
   ```
   https://beautiful-scrape.vercel.app/api/scrap
   ```

   - Set the content type to `application/json`.
   - In the request body, provide the payload as a JSON object with the following structure:
   
   ```json
   {
     "url": "URL_ENDPOINT",
     "arguments": [
       ARGUMENT_1,
       ARGUMENT_2,
       ...
     ]
   }
   ```
   
   - Replace `URL_ENDPOINT` with the target URL you want to scrape.
   - Replace `ARGUMENT_X` with the specific BeautifulSoup arguments you want to apply to the target URL.

2. **GET Request:**
   - Use the URL structure to make a GET request with the following parameters:
   
   ```
   https://beautiful-scrape.vercel.app/api/scrap?url=URL_ENDPOINT&arguments=ARGUMENT_1&arguments=ARGUMENT_2&...
   ```
   
   - Replace `URL_ENDPOINT` with the target URL you want to scrape.
   - Replace `ARGUMENT_X` with the specific BeautifulSoup arguments you want to apply to the target URL.

3. **Request Parameters Explanation:**
   - `url` (string): The URL of the webpage you want to scrape.
   - `arguments` (list of objects): Your BeautifulSoup arguments to scrape the URL. Each object in the list represents an argument.
   
     - The object can be one of the following:
       - `attribute_name` (string): The name of the attribute you want to extract. You can directly access common attributes of HTML elements.
       - `method` (dictionary): A dictionary where the key is the method name and the value is an array of arguments for that method. This allows you to apply methods on BeautifulSoup elements.
       
         ```json
         {
           "method_name": ["arg1", "arg2", ...],
           "at_element": [
             {"method_name": ["arg1", "arg2", ...]},
             ...
           ]
         }
         ```
         
         - `at_element` (array, optional): If the method returns an array, you can use the `at_element` parameter to apply additional attributes or methods to each element in the array.
       - `list` (array): An array of attributes or methods to be applied to the current element itself.
   
## Response Format



The API will respond with the extracted data in the following format:

```json
[
  [RESULT_1, RESULT_2, ...],
  [RESULT_1, RESULT_2, ...],
  ...
]
```

- Each inner array represents a result set.
- Each result set contains the extracted data corresponding to the provided arguments.

## Error Handling

In case of errors, the API will respond with an error message in the following format:

```json
{
  "error": "ERROR_MESSAGE"
}
```

- Replace `ERROR_MESSAGE` with the specific error message describing the encountered issue.

## Examples

Here are some examples to demonstrate how to use our Web Scraping API:

1. Scrape all the quotes on the homepage of quotes.toscrape.com:

   ```bash
   # Example POST request
   curl -X POST -H "Content-Type: application/json" -d '{
     "url": "http://quotes.toscrape.com/",
     "arguments": [
       {"find_all": ["div", {"class": "quote"}]},
       {"at_element": [
         {"find": ["span", {"class": "text"}], "as_text": true},
         {"find": ["span", {"class": "author"}], "as_text": true}
       ]}
     ]
   }' https://beautiful-scrape.vercel.app/api/scrap
   ```

2. Scrape the first quote on the homepage of quotes.toscrape.com:

   ```bash
   # Example POST request
   curl -X POST -H "Content-Type: application/json" -d '{
     "url": "http://quotes.toscrape.com/",
     "arguments": [
       {"find": ["div", {"class": "quote"}]},
       {"at_element": [
         {"find": ["span", {"class": "text"}], "as_text": true},
         {"find": ["span", {"class": "author"}], "as_text": true}
       ]}
     ]
   }' https://beautiful-scrape.vercel.app/api/scrap
   ```

3. Scrape quotes by a specific author:

   ```bash
   # Example GET request
   https://beautiful-scrape.vercel.app/api/scrap?url=http://quotes.toscrape.com/quotes/tag/love&page=1&arguments=find_all:div.quote&arguments=find:span.text,span.author
   ```

4. Scrape quotes by a specific tag:

   ```bash
   # Example GET request
   https://beautiful-scrape.vercel.app/api/scrap?url=http://quotes.toscrape.com/quotes/tag/inspirational&page=1&arguments=find_all:div.quote&arguments=find:span.text,span.author
   ```

Feel free to modify the URL and arguments based on your specific scraping requirements.

