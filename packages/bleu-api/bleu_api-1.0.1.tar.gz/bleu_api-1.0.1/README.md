# BleuAPIClient

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

BleuAPIClient is a Python client for interacting with the Bleu API. It provides a convenient way to access various endpoints for tasks such as KYC verification, face matching, and more.

## Installation

You can install this package using `pip`:

```bash
pip install bleu-api
```

## Usage

To use the BleuAPIClient in your Python project, you need to create an instance of the `BleuAPIClient` class, providing your client ID and client secret. Once initialized, you can call methods to interact with the Bleu API.

Here's an example of how to get started:

```python
from bleu_api.client import *

# Initialize the client with your client ID and client secret
client = BleuAPIClient(client_id='your_client_id', client_secret='your_client_secret')

# Get an access token
client.get_access_token()

# Perform a single KYC verification
response = client.single_kyc_verification(
    selfie_image_path='path/to/selfie_image.jpg',
    doc_front_path='path/to/doc_front.jpg',
    doc_back_path='path/to/doc_back.jpg'
)

# Check the response
if response:
    if response['responseCode'] == BleuAPIClient.RESPONSE_CODES["SUCCESS"]:
        print("Verification successful.")
    else:
        print(f"Verification failed with code {response['responseCode']}")

# Continue using other methods as needed

```

## API Endpoints

The `BleuAPIClient` provides methods for interacting with various API endpoints. Refer to the [API_ENDPOINTS](#api-endpoints) class variable for the available endpoints.

## Response Codes

The `BleuAPIClient` includes a set of predefined response codes to help you interpret the results of your API requests. These codes are available as a dictionary under the `RESPONSE_CODES` class variable.

## Configuration

You can configure the client by modifying its class variables, such as `BASE_URL` or adding new API endpoints and response codes as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions to this project are welcome. Please refer to the [CONTRIBUTING](CONTRIBUTING.md) guidelines for more information on how to contribute.

```

Make sure to replace 'your_client_id' and 'your_client_secret' with your actual credentials. You can also add more detailed information and examples to the README if necessary.