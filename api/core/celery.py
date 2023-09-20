import os
import re
from telethon import TelegramClient, events, sync
# from celery import Celery
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from telethon.sync import TelegramClient
from django_telethon.sessions import DjangoSession
from django_telethon.models import App, ClientSession
from telethon.errors import SessionPasswordNeededError

# Use your own values from my.telegram.org
API_ID = '21422571'
API_HASH = '40d1adee207c82729abe580235e3c83d'


app, is_created = App.objects.update_or_create(
    api_id=API_ID,
    api_hash=API_HASH
)
cs, cs_is_created = ClientSession.objects.update_or_create(
    name='default',
)
telegram_client = TelegramClient(DjangoSession(client_session=cs), app.api_id, app.api_hash)
telegram_client.connect()

print("Yes")

if not telegram_client.is_user_authorized():
    phone = input('Enter your phone number: ')
    telegram_client.send_code_request(phone)
    code = input('Enter the code you received: ')
    try:
        telegram_client.sign_in(phone, code)
    except SessionPasswordNeededError:
        password = input('Enter your password: ')
        telegram_client.sign_in(password=password)  



# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# app = Celery('telethon')

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()

# # @background(schedule=60)
# def start_collecting():
#     print("Working")
#     TELETHON_API_ID = '21422571'
#     TELETHON_API_HASH = '40d1adee207c82729abe580235e3c83d'

#     api_id = TELETHON_API_ID
#     api_hash = TELETHON_API_HASH

#     phone_number = '+93794581433'

#     user_input_channel = 'https://t.me/DollarKabul'

#     client = TelegramClient('your_session_name', api_id, api_hash)

#     def filter(text):
#         # Define a regular expression pattern to match the buy and sell values, including trailing zeros
#         patternAF = r'(\d+\.\d{2})خـرید (\d+\.\d{2})فــروش'
#         patternPK = r'(\d+\.\d{2})خرید (\d+\.\d{2})فروش'

#         if('🇵🇰' in text):
#             # Use re.search to find the pattern in the text
#             match = re.search(patternPK, text)

#             # Initialize an empty dictionary
#             result_dict = {}

#             # Check if a match was found
#             if match:
#                 # Extract the buy and sell values as strings from the match
#                 buy_value_str = match.group(2)
#                 sell_value_str = match.group(1)

#                 # Populate the result dictionary
#                 result_dict['buy'] = buy_value_str
#                 result_dict['sell'] = sell_value_str

#         else:
#             # Use re.search to find the pattern in the text
#             match = re.search(patternAF, text)

#             # Initialize an empty dictionary
#             result_dict = {}

#             # Check if a match was found
#             if match:
#                 # Extract the buy and sell values as strings from the match
#                 buy_value_str = match.group(1)
#                 sell_value_str = match.group(2)

#                 # Populate the result dictionary
#                 result_dict['buy'] = buy_value_str
#                 result_dict['sell'] = sell_value_str

#         return result_dict


#     @client.on(events.NewMessage(chats=user_input_channel))
#     async def newMessageListener(event):
#         newMessage = event.message.message

#         print(filter(newMessage))
#         print("----------------")

#     # client.sign_in(bot_token=api_hash)

#     with client:
#         client.run_until_disconnected()
