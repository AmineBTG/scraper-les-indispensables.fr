# Product Scraper

This Python script scrapes product details from the "Les Indispensables" website. It retrieves product URLs, fetches detailed information about each product, and saves the data, including product images and documents, to the local file system.

## Features

- Scrapes product URLs from the main product listing page.
- Extracts detailed information about each product, including name, reference, description, image URL, and document URLs.
- Downloads product images and documents.
- Saves product details to a CSV file.

## Requirements

- Python 3.11.x
- `requests` library
- `beautifulsoup4` library
- `pandas` library
- `openpyxl` library

## Installation

1. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:

    ```sh
    python main.py
    ```

2. The script will create a folder named `Scraping output - <timestamp>` containing subfolders for each product. Each subfolder will contain the product's image and documents, along with a `products.csv` file listing all scraped product details.

## Script Overview

- `get_products_urls()`: Fetches product URLs from the main product listing page.
- `get_product_details(product_url)`: Fetches detailed information about a product from its detail page.
- `get_products_details(products_urls)`: Fetches details for a list of products.
- `download_file_from_url(file_url, save_folder)`: Downloads a file from a given URL and saves it to a specified folder.
- `save_output(products_details)`: Saves the product details and downloads associated files.
- `main()`: Main function to run the entire scraping process.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
