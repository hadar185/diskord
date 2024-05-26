import logging
import asyncio
import threading

from fastapi import UploadFile
from discord import Client, Intents, File

logger = logging.getLogger(__name__)


class DiscordClient:
    def __init__(self) -> None:
        self._client = Client(intents=Intents.default())

    def start_discord_bot(self, token: str):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        self._client.run(token)

    def run_client(self, token: str) -> None:
        threading.Thread(target=self.start_discord_bot, args=(token,), daemon=True).start()

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
        future = asyncio.run_coroutine_threadsafe(channel.fetch_message(message_id), self._client.loop)
        message = future.result()
        return message.attachments[0].url
