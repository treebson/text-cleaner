# Data Cleaning Module

A simple module for parsing, cleaning and validating:

- names
- emails
- phone numbers
- URLs
- addresses

## Setup

1. Create a new Python 3.6 environment: `conda create -n text-cleaner python=3.6`
2. Activate conda environment: `conda activate text-cleaner`
3. Install dependencies: `pip install pandas validators nameparser phonenumbers url_normalize geopy pycountry`

## Usage

1. Execute script with `run.py` (this may take a while due to geocoding)
2. Takes as input `data_raw.csv` and outputs to `data_clean.csv`
3. Additional test cases can be added to `data_raw.csv`

## Assumptions

- Data is internationally sourced and is provided in CSV format
- Should handle missing data elegantly
- Make use of open source Python libraries where possible
- Cleaners are abstracted into classes for encapsulation and readability

## Methodology

### Names

- Names are parsed and normalized using the `nameparser` library
- Cleaned names only include first and last name, removes titles (e.g. Mr, Mrs, Ms), and are capitalized
- Validates that name can be parsed and is not null
- Minimal validation is performed on names (see: [Falsehoods Programmers Believe About Names](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/))

### Emails

- Cleaning simply lowercases the email
- Validates using the `validators` library
- Validation runs a bunch of regex checks based based on [Django's email validator](https://github.com/django/django/blob/main/django/core/validators.py)

## URLs

- URLs are cleaned using the `url_normalize` library
- Standardises casing, adds in the host, and encodes paths where appropriate
- Also removes "www." from URLs
- Validates using the `validators` library
- Validation essentially runs a bunch regex checks based on [dperini's URL validator](https://gist.github.com/dperini/729294)

### Addresses

- Uses geocoding and geolocation to parse the address string
- This approach was chosen because cleaning addresses is hard (see: [Falsehoods Programmers Believe About Addresses](https://www.mjt.me.uk/posts/falsehoods-programmers-believe-about-addresses/))
- Using geocoding significantly increases run time due to synchronous API calls
- Leverages the `geopy` library and [ArcGIS](https://www.esri.com/en-us/arcgis/about-arcgis/overview) to extract the street, suburb, city, state, postcode and country
- Validation is based on whether the API returns a candidate location above a certain confidence threshold

### Phone Numbers

- Cleaning uses the `phonenumbers` library to parse the phone number
- Takes in as input the country code to format the number into international format (+61 for Australia)
- Phone numbers will use the country code extracted from geolocation, otherwise default to "AU"
- Validates that the phone number is valid for a region by checking the length and prefix information

## Future Work

- Extract unit numbers from addresses
- Handle address ranges
- Test other geolocation APIs (e.g. Google)
- Speed up performance by parallelising geolocation API calls
