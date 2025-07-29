import asyncio
from typing import Dict
from config import settings

async def run(state: Dict[str, dict], notify):
    while True:
        await asyncio.sleep(settings.SYNC_POS_INTERVAL)
        # Placeholder for syncing positions from KuCoin
        pass
