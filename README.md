# Web Scraping API Documentation

Welcome to the documentation for our Web Scraping API. This guide will provide you with all the necessary information to integrate and utilize our API effectively. Whether you're a seasoned developer or just getting started with web scraping, this documentation will help you leverage the power of our API to retrieve valuable data from websites.

## Table of Contents

1. [Introduction](#introduction)
2. [Endpoint](#endpoint)
3. [Request Parameters](#request-parameters)
5. [Response Format](#response-format)
6. [Error Handling](#error-handling)
7. [Examples](#examples)
8. [Rate Limiting](#rate-limiting)
9. [Support](#support)

## Introduction

Our Web Scraping API allows you to retrieve data from websites in a structured and automated manner. By sending HTTP requests to our API endpoint, you can specify the target URL and define the elements you want to extract from the webpage. The API will process your request and return the extracted data in a convenient format.

## Endpoint

The base URL for our Web Scraping API is:

```
https://beautiful-scrape.vercel.app/api/scrap
```

## Request Parameters

The API supports both GET and POST requests. The following parameters should be included in your requests:

- `url` (required): The URL of the webpage you want to scrape.
- `arguments` (required): An array of objects specifying the scraping instructions. Each object represents a specific scraping action to be performed on the webpage.

The `arguments` array should follow the structure below:

```json
"arguments": [
  {
    "select": ["<CSS selector>"],
    "at_elment": {
      "<optional_method>": ["<optional_method_argument>"]
    }
  },
  ...
]
```

- `select`: An array of CSS selectors representing the elements you want to extract from the webpage.
- `at_elment` (optional): An object specifying additional methods to be applied to the selected elements. This allows you to further manipulate or extract specific data from the elements.

## Response Format

The API response will be in JSON format and will contain the extracted data based on your scraping instructions. The structure of the response will match the structure of the `arguments` array in your request, with each element containing the extracted data for the corresponding scraping action.

## Error Handling

If an error occurs during the processing of your request, the API will return an error response in JSON format. The response will include an `error` field with a description of the encountered error.

## Examples

Here are a few examples to demonstrate how to use our Web Scraping API:

1. Retrieve the text content of all `<h1>` elements from a webpage:

```json
{
  "url": "https://example.com",
  "arguments": [
    {
      "select": ["h1"]
    }
  ]
}
```

2. Retrieve the text content of all `<a>` elements inside a specific `<div>`:

```json
{
  "url": "https://example.com",
  "arguments": [
    {
      "select": ["div.my-div-class a"]
    }
  ]
}
```

3. Retrieve the `href` attribute of the first `<a>` element and extract the domain name from it:

```json
{
  "url": "https://example.com",
  "arguments": [


    {
      "select": ["a:first-child"],
      "at_elment": {
        "get_attribute": ["href"],
        "extract_domain": []
      }
    }
  ]
}
```

## Rate Limiting

To ensure fair usage and maintain optimal performance, our API enforces rate limiting. The specific rate limits will be provided to you when you sign up and obtain an API key.

## Support

If you have any questions, issues, or need assistance while using our Web Scraping API, please don't hesitate to reach out to our support team. We're here to help you make the most of our services and ensure a smooth integration experience.

Contact information:
- Email: support@example.com
- Website: https://www.example.com/support

That's it