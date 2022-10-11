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

    response = requests.get(f'{api_url}orders.json?status=open', headers=headers).json()
    order_list = response["orders"]
    order_dict = {}
    for order in order_list:
        id, order_number, order_time, country = order["id"], order["order_number"], order["created_at"], order["shipping_address"]["country_code"]
        year, month, day, time = order_time[0:4], order_time[5:7], order_time[8:10], order_time[11:16]
        try:
            country = order["shipping_address"]["country_code"]
        except KeyError:
            country = order["billing_address"]["country_code"]
        tmp_dict = {order_number: {"year": year, "month": month, "day": day, "time": time, "country": country, "id": id}}
        merge(order_dict, tmp_dict)
    return order_dict

def closed_order_list():
    headers = {
        'X-Shopify-Access-Token': app_token,
    }

    response = requests.get(f'{api_url}orders.json?status=any&limit=150;', headers=headers).json()
    order_list = response["orders"]
    order_dict = {}
    for order in order_list:
        id, order_number, order_time = order["id"], order["order_number"], order["created_at"]
        year, month, day, time = order_time[0:4], order_time[5:7], order_time[8:10], order_time[11:16]
        try:
            country = order["shipping_address"]["country_code"]
        except KeyError:
            country = order["billing_address"]["country_code"]
        tmp_dict = {order_number: {"year": year, "month": month, "day": day, "time": time, "country": country, "id": id}}
        merge(order_dict, tmp_dict)
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
    try:
        unique_id = orders[int(uuid)]["id"]
        response = requests.get(f'{api_url}orders/' + str(unique_id) + '.json', headers=headers).json()
        order_full = response['order']
        product_dict = {}
        name, order_number, email, price, country = order_full['shipping_address']['name'], order_full['name'], order_full['contact_email'], order_full['total_line_items_price_set']['shop_money']['amount'], order_full['shipping_address']['country_code']
        products = order_full['line_items']
        count, product_list = 0, []
        for product in products:
            count +=1
            product_name, quantity = product['name'], product['quantity']
            #product_tmp_dict = {order_number: {count: {"product_name" : product_name, "quantity" : quantity}}}
            product_tuple = (f"{product_name}",f"{quantity}")
            product_list.append(product_tuple)
        order_dict = {order_number: {"name": name, "email": email, "price": price, "country": country, "products": product_list}}
        return order_dict
    except KeyError:
        orders = closed_order_list()
        try:
            unique_id = orders[int(uuid)]["id"]
            response = requests.get(f'{api_url}orders/' + str(unique_id) + '.json', headers=headers).json()
            order_full = response['order']
            product_dict = {}
            name, order_number, email, price, country = order_full['shipping_address']['name'], order_full['name'], order_full['contact_email'], order_full['total_line_items_price_set']['shop_money']['amount'], order_full['shipping_address']['country_code']
            products = order_full['line_items']
            count, product_list = 0, []
            for product in products:
                count +=1
                product_name, quantity = product['name'], product['quantity']
                #product_tmp_dict = {order_number: {count: {"product_name" : product_name, "quantity" : quantity}}}
                product_tuple = (f"{product_name}",f"{quantity}")
                product_list.append(product_tuple)
            order_dict = {order_number: {"name": name, "email": email, "price": price, "country": country, "products": product_list}}
            return order_dict
        except KeyError:
            return "That order number doesn't exist."
        except:
            return Exception
    except:
        return Exception

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
