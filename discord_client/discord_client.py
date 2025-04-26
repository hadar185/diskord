import logging
import asyncio
import time

from discord import Client, Intents, File

logger = logging.getLogger(__name__)


class DiscordClient:
    def __init__(self) -> None:
        self._client = Client(intents=Intents.default())

    def start_discord_bot(self, token: str) -> None:
        loop = asyncio.get_event_loop()
        loop.create_task(self._client.start(token))

    async def upload_file(self, path: str, file_name: str, channel_id: int) -> int:
        logger.info(f"Sending file to Discord: {path}")
        channel = self._client.get_channel(channel_id)
        discord_file = File(path, filename=file_name)
        future = asyncio.run_coroutine_threadsafe(channel.send(file=discord_file), self._client.loop)
        message = future.result()
        return message.id

    async def fetch_attachment_url(self, message_id: int, channel_id: int) -> str:
        logger.info(f"Fetching url of message: {message_id}")
        channel = self._client.get_channel(channel_id)
        start_time = time.time()
        message = await channel.fetch_message(message_id)
        logger.debug(time.time() - start_time)
        return message.attachments[0].url
