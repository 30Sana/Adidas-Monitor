import requests
import json
import time

# Function to check product availability


def check_product_availability(product_data):
    product_id = product_data['product_id']
    sizes = product_data['_embedded']['variations']

    for size in sizes:
        size_name = size['size']
        stock_level = size['stock_level']
        if stock_level > 0:
            print(
                f"Product {product_id} | Size {size_name} | In Stock [Stock: {stock_level}]")
        else:
            print(f"Product {product_id} | Size {size_name} | Out of Stock")


# Delay between each check (in seconds)
# Adjust this as needed (Botters use 9s at all times and 3s before release date lol)
check_interval = 9

session = requests.Session()

while True:
    # Read product SKUs from a text file
    with open('product_skus.txt', 'r') as file:
        product_skus = file.read().splitlines()

    for product_sku in product_skus:
        paramsGet = {"experiment_product_data": "A"}
        headers = {
            "X-Market": "CA",
            "Accept": "application/hal+json",
            "X-App-Info": "platform/iOS version/5.22.1",
            "X-Api-Key": "m79qyapn2kbucuv96ednvh22",
            "User-Agent": "adidas/2023.3.28.11.8 CFNetwork/1240.0.4 Darwin/20.6.0",
            "Accept-Language": "en-CA",
            "Accept-Encoding": "gzip, deflate"
        }

        response = session.get(
            f"https://api.3stripes.net/gw-api/v2/products/{product_sku}/availability",
            params=paramsGet,
            headers=headers
        )

        if response.status_code == 200:
            product_data = json.loads(response.text)
            check_product_availability(product_data)
        else:
            print(
                f"Failed to retrieve data for product {product_sku}. Status code: {response.status_code}")

    # Wait for the specified interval before checking again
    time.sleep(check_interval)
