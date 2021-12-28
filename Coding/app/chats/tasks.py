# import requests
# from celery import shared_task
# from channels.layers import get_channel_layer
# from .models import Profile
# from django.forms.models import model_to_dict
# from asgiref.sync import async_to_sync
# import asyncio
#
# channel_layer = get_channel_layer()
#
#
# @shared_task
# def update():
#     url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"
#     data = requests.get(url).json()
#     state = None
#     coins = []
#     for coin in data:
#         # print(coin)
#         obj, created = Coin.objects.get_or_create(symbol=coin['symbol'])
#         obj.name = coin['name']
#         obj.symbol = coin['symbol']
#         if obj.price > coin['current_price']:
#             state = 'fall'
#         elif obj.price == coin['current_price']:
#             state = 'same'
#         elif obj.price < coin['current_price']:
#             state = 'raise'
#         obj.price = coin['current_price']
#         obj.rank = coin['market_cap_rank']
#         obj.image = coin['image']
#         obj.save()
#         new_data = model_to_dict(obj)
#         new_data.update({'state': state})
#         coins.append(new_data)
#     # async_to_sync(channel_layer.group_send('coins', {'type': 'send_new_data1', 'text': coins}))
#     async_to_sync(channel_layer.group_send)(
#         "coins",
#         {
#             'type': 'send.data',
#             'text': coins
#         }
#     )
#
#
