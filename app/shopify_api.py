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
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    response = requests.get(f'{api_url}orders/count.json?status=open', headers=headers).text
    orders = ''.join(filter(str.isdigit, response))
    return orders

def order_list():
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    response = requests.get(f'{api_url}orders.json?status=open', headers=headers)
    order_list = response.json()["orders"]
    order_dict = {order["order_number"]: {
        "year": order["created_at"][0:4],
        "month": order["created_at"][5:7],
        "day": order["created_at"][8:10],
        "time": order["created_at"][11:16],
        "country": order["shipping_address"].get("country_code") or order["billing_address"].get("country_code"),
        "id": order["id"]
    } for order in order_list}
    return order_dict


def closed_order_list():
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    response = requests.get(f'{api_url}orders.json?status=any&limit=150;', headers=headers)
    order_list = response.json()["orders"]
    order_dict = {order["order_number"]: {
        "year": order["created_at"][0:4],
        "month": order["created_at"][5:7],
        "day": order["created_at"][8:10],
        "time": order["created_at"][11:16],
        "country": order["shipping_address"].get("country_code") or order["billing_address"].get("country_code"),
        "id": order["id"]
    } for order in order_list}
    return order_dict


def closed_count(today):
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    response = requests.get(f'{api_url}orders/count.json?status=closed&created_at_min={today}', headers=headers).json()
    return response["count"]

def get_order(uuid):
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    orders = order_list()
    unique_id = orders.get(int(uuid))["id"]
    if unique_id is None:
        orders = closed_order_list()
        unique_id = orders.get(int(uuid))["id"]
        if unique_id is None:
            return "That order number doesn't exist."

    url = 'https://clickeys-nl.myshopify.com/admin/api/2022-04/orders/{}.json'.format(unique_id)
    response = requests.get(url, headers=headers).json()
    order_full = response['order']

    name, order_number, email, price, country = order_full['shipping_address']['name'], order_full['name'], order_full['contact_email'], order_full['total_line_items_price_set']['shop_money']['amount'], order_full['shipping_address']['country_code']
    products = order_full['line_items']
    product_list = []
    for product in products:
        product_name, quantity = product['name'], product['quantity']
        product_tuple = (f"{product_name}",f"{quantity}")
        product_list.append(product_tuple)

    order_dict = {order_number: {"name": name, "email": email, "price": price, "country": country, "products": product_list}}
    return order_dict

def random_quote():
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': str(settings.NINJA_KEY)})
    if response.status_code == requests.codes.ok:
        response = response.json()
        return response[0]["fact"]
    else:
        return "Error:"

def balance():
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    response = requests.get(f'{api_url}shopify_payments/balance.json', headers=headers).json()
    return str(response['balance'][0]['amount'])
