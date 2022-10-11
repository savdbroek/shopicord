from random import Random
import discord
import datetime
import settings
import logging
import shopify_api as sapi


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

authors = [] # list of Discord User ID's of people that are allowed to use the bot

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

def is_us(author_id):
    if author_id in authors:
        return True

def return_closed_orders():
    currentDate = datetime.date.today()
    firstDayOfMonth = datetime.date(currentDate.year, currentDate.month, 1)
    closed_order_count = sapi.closed_count(firstDayOfMonth)
    shopify_desc_closed = "".join(["**Shopify Closed:** ", str(closed_order_count)])

    return shopify_desc_closed

def balance():
    balance = sapi.balance()
    balance_desc = "".join(["**Shopify Balance:** €", balance, "\n"])
    return balance_desc

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith('!orders'):
        if is_us(message.author.id):
            mention = "".join(["<@", message.author.i, ">"])
            shopify_orders= sapi.get_open_orders()
            shopify = "".join(["**Orders: **", shopify_orders])

            if int(shopify_orders) > 0:
                shopify_dict, shopify_tmp_message, shopify_message = sapi.order_list(), "", ""

                if shopify_dict:
                    for key, value in shopify_dict.items():
                        if isinstance(value, dict):
                            shopify_message += shopify_tmp_message.join([f"**#{key}** - {value['day']}/{value['month']}/{value['year']} - Time: **{value['time']}** - **{value['country']}**\n"])
                    shopify_desc = "".join(["**Shopify:**\n", shopify_message, "\n"])
                else: 
                    shopify_desc = ""
            
            else:
                shopify_desc = ""
            
            shopify_desc_closed = return_closed_orders()
            shopify_balance = balance()
            
            if shopify_desc == "":
                quote = sapi.random_quote()
                orders = discord.Embed(
                    description="".join([shopify, "\n\n", quote, "\n\n", shopify_desc_closed, "\n", shopify_balance]),
                    colour=discord.Colour.blurple()
                )

            else:
                orders = discord.Embed(
                    description="".join([shopify, "\n\n", shopify_desc, shopify_desc_closed, "\n", shopify_balance]),
                    colour=discord.Colour.blurple()
                )

            await message.channel.send(mention, embed=orders)
    
    if message.content.startswith('!order') and message.content != '!orders':
        uuid = message.content
        if is_us(message.author.id):
            order_dict, shopify_tmp_message= sapi.get_order(uuid.replace("!order ","")), ""
            if isinstance(order_dict, dict):
                shopify_message = ""
                for key in order_dict:
                    products = ""
                    for product in order_dict[key]['products']:
                        products += "".join([product[0], " - **Quantity** ", product[1], "\n"])
                    shopify_message += shopify_message.join(f"**{key}**\n**Name: **{order_dict[key]['name']}\n**Email: **{order_dict[key]['email']}\n**Price: **€{order_dict[key]['price']}\n**Country: **{order_dict[key]['country']}\n\n**Products:**\n{products}")
                order = discord.Embed(
                    description="".join(shopify_message),
                    colour=discord.Colour.blurple()
                )
            else:
                order = discord.Embed(
                    description="".join(order_dict),
                    colour=discord.Colour.blurple()
                )
        
            await message.channel.send(embed=order)

client.run(str(settings.DISCORD_WEBHOOK))
