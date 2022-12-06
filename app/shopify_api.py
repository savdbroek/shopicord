from urllib.parse import quote_plus
import requests
import settings
from mergedeep import merge
import datetime

app_token = str(settings.SHOPIFY_API_KEY)

#check if SHOPIFY_URL ends in /
if str(settings.SHOPIFY_URL).endswith('/'):
    api_url = str(settings.SHOPIFY_URL)
else:
    api_url = "".join([str(settings.SHOPIFY_URL), '/'])


def get_open_orders():
    # Set the headers to include the app token for authentication
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    # Make a GET request to the orders/count.json endpoint using the requests library
    # with the query parameter status=open to retrieve the count of open orders
    response = requests.get(f'{api_url}orders/count.json?status=open', headers=headers).text

    # Filter the text response to extract only the numeric digits representing the count of open orders
    orders = ''.join(filter(str.isdigit, response))

    # Return the count of open orders
    return orders

def order_list():
    # Set the headers to include the app token for authentication
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    # Make a GET request to the orders.json endpoint using the requests library
    # with the query parameter status=open to retrieve only open orders
    response = requests.get(f'{api_url}orders.json?status=open', headers=headers)

    # Parse the JSON response to extract the orders data
    order_list = response.json()["orders"]

    # Create a dictionary mapping each order's order number to its
    # creation date and time, the country code of its shipping or billing address,
    # and its Shopify ID
    order_dict = {order["order_number"]: {
        "year": order["created_at"][0:4],
        "month": order["created_at"][5:7],
        "day": order["created_at"][8:10],
        "time": order["created_at"][11:16],
        "country": order["shipping_address"].get("country_code") or order["billing_address"].get("country_code"),
        "id": order["id"]
    } for order in order_list}

    # Return the dictionary of orders
    return order_dict


# Define the function to get a list of closed orders
def closed_order_list():
    # Set the headers for the HTTP request
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    # Make the HTTP request to the Shopify API to get the list of orders
    response = requests.get(f'{api_url}orders.json?status=any&limit=150;', headers=headers)

    # Parse the JSON response to get the list of orders
    order_list = response.json()["orders"]

    # Create a dictionary containing the relevant information about each order
    order_dict = {order["order_number"]: {
        "year": order["created_at"][0:4],
        "month": order["created_at"][5:7],
        "day": order["created_at"][8:10],
        "time": order["created_at"][11:16],
        "country": order["shipping_address"].get("country_code") or order["billing_address"].get("country_code"),
        "id": order["id"]
    } for order in order_list}

    # Return the dictionary containing the closed orders
    return order_dict


# Define the function to get the number of closed orders
def closed_count(today):
    # Set the headers for the HTTP request
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    # Make the HTTP request to the Shopify API to get the number of closed orders
    response = requests.get(f'{api_url}orders/count.json?status=closed&created_at_min={today}', headers=headers).json()

    # Return the number of closed orders
    return response["count"]

# Define the function to get an order
def get_order(uuid):
    # Set the headers for the HTTP request
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    # Get the list of open orders
    orders = order_list()

    # Try to get the order with the specified ID from the list of open orders
    unique_id = orders.get(int(uuid))["id"]

    # If the order with the specified ID is not found in the list of open orders,
    # try to get it from the list of closed orders instead
    if unique_id is None:
        orders = closed_order_list()
        unique_id = orders.get(int(uuid))["id"]

        # If the order is not found in either list, return an error message
        if unique_id is None:
            return "That order number doesn't exist."

    # Construct the URL to make the HTTP request to get the order
    url = 'https://clickeys-nl.myshopify.com/admin/api/2022-04/orders/{}.json'.format(unique_id)

    # Make the HTTP request to the Shopify API to get the order
    response = requests.get(url, headers=headers).json()

    # Get the full order details from the response
    order_full = response['order']

    # Extract the relevant information from the order
    name = order_full['shipping_address']['name']
    order_number = order_full['name']
    email = order_full['contact_email']
    price = order_full['total_line_items_price_set']['shop_money']['amount']
    country = order_full['shipping_address']['country_code']
    products = order_full['line_items']

    # Create a list of tuples containing the name and quantity of each product in the order
    product_list = []
    for product in products:
        product_name = product['name']
        quantity = product['quantity']
        product_tuple = (f"{product_name}",f"{quantity}")
        product_list.append(product_tuple)

    # Create a dictionary containing the information about the order
    order_dict = {order_number: {"name": name, "email": email, "price": price, "country": country, "products": product_list}}

    # Return the dictionary containing the order information
    return order_dict

def random_quote():
    # Set the number of quotes to return from the API to 1
    limit = 1
    
    # Construct the API endpoint URL by formatting the string with the value of the `limit` variable
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    
    # Send a GET request to the API endpoint, including the API key in the request headers
    response = requests.get(api_url, headers={'X-Api-Key': str(settings.NINJA_KEY)})
    
    # If the API responds with a status code of 200, parse the response as JSON and return the first quote
    if response.status_code == requests.codes.ok:
        response = response.json()
        return response[0]["fact"]
    else:
        # If the API responds with any other status code, raise an error
        raise ValueError("Received non-OK response from API: {}".format(response.status_code))

# Define the function to get the balance
def balance():
    # Set the headers for the HTTP request
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    # Make the HTTP request to the Shopify Payments API to get the balance
    response = requests.get(f'{api_url}shopify_payments/balance.json', headers=headers).json()

    # Return the amount of the balance as a string
    return str(response['balance'][0]['amount'])
