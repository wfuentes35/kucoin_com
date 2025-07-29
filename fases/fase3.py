import asyncio
from typing import Dict
from config import settings

async def run(state: Dict[str, dict], notify):
    while True:
        await asyncio.sleep(settings.CHECK_INTERVAL)
        # Placeholder: in real bot, would promote reserved symbols
        pass
