import datetime
import os
from dataclasses import asdict, dataclass
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


@dataclass
class ProductUrl:
    name: str
    url: str


@dataclass
class ProductDetails:
    url: str
    name: str
    reference: str
    description: str
    image_url: str
    docs_urls: list[str]


def get_products_urls() -> list[ProductUrl]:
    """
    Fetches product URLs from the main product listing page.

    Returns:
    list[ProductUrl]: List of ProductUrl dataclass instances containing product names and URLs.
    """
    print("Getting products urls ...")

    # Request the product listing page
    r = requests.get("https://www.lesindispensables.fr/produits/?limit=2000&order=name&page=1")
    soup = BeautifulSoup(r.content, "html.parser")

    products_urls = []

    # Parse product URLs from the page
    for elem in soup.find("div", {"id": "liste-produits"}).find_all("a", {"class": "prod"}):
        products_urls.append(
            ProductUrl(
                name=elem.attrs.get("title").strip(),
                url=elem.attrs.get("href"),
            )
        )

    print(f"Gotten products urls for {len(products_urls)} products !")
    return products_urls


def get_product_details(product_url: ProductUrl) -> ProductDetails:
    """
    Fetches detailed information about a product from its detail page.

    Parameters:
    product_url (ProductUrl): The ProductUrl dataclass instance containing product name and URL.

    Returns:
    ProductDetails: A ProductDetails dataclass instance containing detailed product information.
    """
    print(f"Gettings product details from '{product_url.url}' ...")

    r = requests.get(product_url.url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Extract product details from the page
    product_name = soup.select_one("div.produit-top div.produit-title")
    product_description = soup.select_one("div.produit-top div.desc")
    product_reference = soup.select_one("div.reference")
    product_image_url = soup.select_one("div.img-ct img").attrs.get("src")
    product_docs_urls = [elem.attrs.get("href") for elem in soup.select("#docsProduit a")]

    product = ProductDetails(
        url=product_url.url,
        name=product_name.text.strip().title() if product_name else None,
        reference=product_reference.text.strip() if product_reference else None,
        description=product_description.text.strip() if product_description else None,
        image_url=product_image_url,
        docs_urls=product_docs_urls,
    )

    return product


def get_products_details(products_urls: list[ProductUrl]) -> list[ProductDetails]:
    """
    Fetches details for a list of products.

    Parameters:
    products_urls (list[ProductUrl]): List of ProductUrl dataclass instances.

    Returns:
    list[ProductDetails]: List of ProductDetails dataclass instances with detailed product information.
    """
    products_details = []

    for product_url in products_urls:
        product_details = get_product_details(product_url)
        products_details.append(product_details)

    return products_details


def download_file_from_url(file_url: str, save_folder: str) -> None:
    """
    Downloads a file from a given URL and saves it to a specified folder.

    Parameters:
    file_url (str): URL of the file to be downloaded.
    save_folder (str): Local folder where the file should be saved.
    """
    r = requests.get(file_url)
    filename = urlparse(file_url).path.split("/")[-1]

    with open(os.path.join(save_folder, filename), "wb") as f:
        f.write(r.content)


def save_output(products_details: list[ProductDetails]) -> None:
    """
    Saves the product details and downloads associated files.

    Parameters:
    products_details (list[ProductDetails]): List of ProductDetails dataclass instances to be saved.
    """
    base_folder_name = f"Scraping output - {datetime.datetime.now().isoformat()[:19].replace(':', '')}"

    for product in products_details:
        folder = os.path.join(base_folder_name, product.name)
        os.makedirs(folder)

        download_file_from_url(product.image_url, folder)
        for doc_url in product.docs_urls:
            download_file_from_url(doc_url, folder)

    df = pd.DataFrame([asdict(elem) for elem in products_details])
    df["docs_urls"] = df["docs_urls"].apply(", ".join)
    df.to_csv(os.path.join(base_folder_name, "products.csv"), index=False, encoding="utf-8")

    print(f"Data saved into folder: '{base_folder_name}'")
    print(f"List of products scraped saved in: '{os.path.join(base_folder_name, 'products.csv')}'")


def main() -> None:
    """
    Main function to run the entire scraping process.
    """
    products_urls = get_products_urls()
    products_details = get_products_details(products_urls)
    save_output(products_details)


if __name__ == "__main__":
    main()
