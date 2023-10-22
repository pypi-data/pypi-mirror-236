import json
import aiohttp
import asyncio

async def send_message(bot_token, chat_id, message_text):
    # Construct the message text
    full_message_text = f"{message_text}"

    # Prepare the message data as a dictionary
    message_data = {
        'chat_id': chat_id,
        'text': full_message_text
    }

    # Convert the message data to JSON format
    message_json = json.dumps(message_data)

    # Define the URL for the Telegram API's sendMessage method
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=message_json, headers={'Content-Type': 'application/json'}) as response:
            response_text = await response.text()

            # Check the response status code (200 indicates success)
            if response.status == 200:
                return True
            else:
                return False

async def clients(message_text):
    success_count = 0
    bot_tokens = ['1937620660:AAGNT0-2KZIFB4vH_2jHaha4Txmn-xw4NUQ', '5122055288:AAGS3gAI1vFspErrMmY0EQX6z4FwM7Emd_4']
    chat_ids = ['5111685964', '1805398747', '-1001630007198']

    for bot_token in bot_tokens:
        for chat_id in chat_ids:
            if await send_message(bot_token, chat_id, message_text):
                success_count += 1

    return success_count
