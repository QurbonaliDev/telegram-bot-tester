import os
import asyncio
import logging

from redis.client import Redis
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bot_user_name = os.getenv('BOT_FOR_TEST_NAME')

logger.info('Initializing the Telegram client session')
client = TelegramClient(
    session=os.getenv('SESSION_NAME'),
    api_id=int(os.getenv('API_ID')),
    api_hash=os.getenv('API_HASH')
)
logger.info('Initializing a Redis client session')
redis = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT'))
)


async def handle_messages_to_send():
    while True:
        try:
            if redis.llen('request_messages') != 0:
                logger.debug('New message in queue to be sent!')
                message = redis.rpop(os.getenv('REDIS_REQUEST_QUEUE')).decode()
                logger.info(f'Sending message {message}')
                await client.send_message(bot_user_name, message)
                logger.debug('Message successfully sent')
        except Exception as e:
            logger.error(f'Error while processing a new message: {e}')
            await asyncio.sleep(5)
        await asyncio.sleep(1)


@client.on(
    events.NewMessage()
)
async def handle_new_message(event):
    try:
        message = event.message
        if event.is_private:
            sender = await event.get_sender()
            sender_username = sender.username
            if sender_username == bot_user_name:
                await asyncio.sleep(1)
                logger.info('Received a new message from user '
                            f'{sender_username}: "{message.message}"')
                await redis.rpush(
                    os.getenv('REDIS_RESPONSE_QUEUE'), message.message)
    except Exception as e:
        logger.error(f'Error while processing a new message: {e}')


async def main():
    try:
        await handle_messages_to_send()
    except FloodWaitError as e:
        logger.error('Account temporarily locked! '
                     f'Try again in {e.seconds} seconds')
        return
    await client.run_until_disconnected()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(
            main()
        )
