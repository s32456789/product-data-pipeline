# Product Data Pipeline & Report

A Python data processing pipeline that retrieves paginated product data from a REST API, cleans and transforms the dataset with Pandas, and generates CSV reports for analysis.

## Overview

This project demonstrates an end-to-end data processing workflow:

```text
REST API
   ↓
Pagination
   ↓
Data Collection
   ↓
Data Validation
   ↓
Pandas DataFrame
   ↓
Data Cleaning
   ↓
Aggregation
   ↓
CSV Reports
```

The goal is to turn raw API data into structured datasets that can be immediately used for analysis.

## Features

* Retrieve data from a REST API
* Handle API pagination using `skip` and `limit`
* Avoid unnecessary requests
* Reuse HTTP connections with `requests.Session`
* Validate API response structure
* Handle request failures
* Retry appropriate temporary failures
* Respect `Retry-After` when available
* Convert API data into a Pandas DataFrame
* Remove duplicate records
* Remove rows with missing required values
* Sort data by price
* Generate category-level statistics
* Export cleaned datasets to CSV

## Tech Stack

* Python
* Requests
* Pandas

## API

The project uses the DummyJSON Products API:

`https://dummyjson.com/products`

The API provides product information including:

* Product ID
* Title
* Price
* Category
* Stock

## Generated Files

### `products.csv`

Contains the cleaned product dataset:

```text
id
title
price
category
stock
```

Products are sorted by price in descending order.

### `category_report.csv`

Contains aggregated information for each product category:

```text
category
average_price
total_stock
```

## Data Processing

The pipeline performs several data quality operations.

### Duplicate Removal

Products are deduplicated using the product ID:

```text
id = unique product identifier
```

### Missing Data

Rows with missing:

* `price`
* `stock`

are removed before generating the final reports.

### Aggregation

The category report calculates:

* Average product price
* Total stock

for each category.

## HTTP Reliability

The API client includes several reliability measures:

* Request timeout
* HTTP status checking
* Retry handling for temporary failures
* Handling for HTTP 429 responses
* Support for `Retry-After`
* Handling for server-side 5xx errors
* Response structure validation

The implementation avoids repeatedly requesting the API after the required dataset has already been retrieved.

## Project Structure

```text
product-data-pipeline/
├── main.py
├── products.csv
├── category_report.csv
└── README.md
```

## How to Run

Install dependencies:

```bash
pip install requests pandas
```

Run:

```bash
python main.py
```

## Skills Demonstrated

* Python automation
* REST API integration
* API pagination
* HTTP error handling
* Retry logic
* Data validation
* Pandas
* Data cleaning
* Grouped data analysis
* CSV report generation

## Practical Applications

The same workflow can be adapted for many business use cases, such as:

* Product catalog processing
* Inventory reports
* Sales data preparation
* API data exports
* Automated reporting
* Data cleaning pipelines

## Why This Project Matters

A useful data automation script is not just about collecting data.

The important part is turning unreliable raw input into a consistent dataset that can be analyzed or delivered to another system.

This project demonstrates that complete workflow from API request to final report.
