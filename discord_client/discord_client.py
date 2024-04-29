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

    async def upload_file(self, file: UploadFile, channel_id: int) -> str:
        logger.info(f"Sending file to Discord: {file.filename}")
        channel = self._client.get_channel(channel_id)
        with open(file.filename, "wb") as f:
            f.write(await file.read())
        discord_file = File(file.filename, filename=file.filename)
        future = asyncio.run_coroutine_threadsafe(channel.send(file=discord_file), self._client.loop)
        message = future.result()
        return message.attachments[0].url
