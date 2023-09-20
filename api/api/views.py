from rest_framework.decorators import api_view
from rest_framework.response import Response
from telethon import TelegramClient
from .models import *
from asgiref.sync import sync_to_async
from django.http import HttpResponse
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
from django.http import JsonResponse
from .serializers import PricesSerializer
import re
from django.core.exceptions import ObjectDoesNotExist

def filter(text):
    # Define a regular expression pattern to match the buy and sell values, including trailing zeros
    patternAF = r'(\d+\.\d{2})خـرید (\d+\.\d{2})فــروش'
    patternPK = r'(\d+\.\d{2})خرید (\d+\.\d{2})فروش'

    if('🇵🇰' in text):
        # Use re.search to find the pattern in the text
        match = re.search(patternPK, text)

        # Initialize an empty dictionary
        result_dict = {}
        result_dict['cur'] = 'pk'

        # Check if a match was found
        if match:
            # Extract the buy and sell values as strings from the match
            buy_value_str = match.group(2)
            sell_value_str = match.group(1)

            # Populate the result dictionary
            result_dict['buy'] = buy_value_str
            result_dict['sell'] = sell_value_str

    else:
        # Use re.search to find the pattern in the text
        match = re.search(patternAF, text)

        # Initialize an empty dictionary
        result_dict = {}
        result_dict['cur'] = 'af'

        # Check if a match was found
        if match:
            # Extract the buy and sell values as strings from the match
            buy_value_str = match.group(1)
            sell_value_str = match.group(2)

            # Populate the result dictionary
            result_dict['buy'] = buy_value_str
            result_dict['sell'] = sell_value_str

    return result_dict

async def start_collecting():
    
    message_count = 10
    TELETHON_API_ID = '21422571'
    TELETHON_API_HASH = '40d1adee207c82729abe580235e3c83d'

    api_id = TELETHON_API_ID
    api_hash = TELETHON_API_HASH

    phone_number = '+93794581433'

    channel_username = 'https://t.me/DollarKabul'

    client = TelegramClient('latest_price', api_id, api_hash)

    try:
        # Start the client
        await client.start()

        # Resolve the channel entity
        channel_entity = await client.get_entity(channel_username)

        # Use the GetHistoryRequest to fetch the last 'message_count' messages from the channel
        messages = await client(GetHistoryRequest(
            peer=channel_entity,
            limit=message_count,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        # print(messages)
        # Extract and print the message texts
        full = []
        for i, message in enumerate(messages.messages, start=1):
            try:
                dataset = filter(message.message)
                dataset['id'] = message.id
                if 'sell' in dataset and 'buy' in dataset:
                    full.append(dataset)
            except Exception as e:
                print(f"Error processing message {i}: {e}")

        return sorted(full, key=lambda x: x['id'])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Disconnect and stop the client
        await client.disconnect()
        

    

    # @client.on(events.NewMessage(chats=user_input_channel))
    # async def newMessageListener(event):
    #     newMessage = event.message.message

    #     print(filter(newMessage))

    # # client.sign_in(bot_token=api_hash)

    # with client:
    #     client.run_until_disconnected()




@sync_to_async
def save_price_instance(price_data):
    id_value = int(price_data['id'])

    try:
        existing_price = prices.objects.get(id=id_value)
    except ObjectDoesNotExist:
        # If the record with the same id doesn't exist, create a new one and save it
        new_price = prices(
            id=id_value,
            cur=price_data['cur'],
            sell=price_data['sell'],
            buy=price_data['buy'],
        )
        new_price.save()

@sync_to_async
def get_last_prices():
    return prices.objects.order_by('id')[:5]

@sync_to_async
def serialize_prices(prices):
    serializer = PricesSerializer(prices, many=True)
    return serializer.data

async def realtime(request):
    stocks = await start_collecting()  # Assuming start_collecting is an async function

    if not stocks:
        print("Nothing received, getting stock data from the database.")
        last_price = await get_last_prices()  # Await the asynchronous database query
        serialized_data = await serialize_prices(last_price)
        return JsonResponse(serialized_data, safe=False)
    else:
        print("Data recieved, saving unsaved data to database and then returning it")
        for p in stocks:
            if 'sell' in p:
                await save_price_instance(p)

    return JsonResponse(stocks, status=200, safe=False)