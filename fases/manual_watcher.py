import asyncio
from typing import Dict

async def run(state: Dict[str, dict]):
    while True:
        await asyncio.sleep(60)
        # Placeholder for manual watcher
        pass
