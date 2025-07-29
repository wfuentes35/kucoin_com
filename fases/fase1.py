import asyncio
import time
from typing import Dict
from config import settings
from utils import get_klines, ema, rsi, bollinger_bands, list_usdt_symbols

async def run(state: Dict[str, dict], exclusion: Dict[str, float], notify):
    await asyncio.sleep(settings.STARTUP_DELAY_FOR_PHASE1)
    while True:
        await asyncio.sleep(settings.SCAN_INTERVAL)
        symbols = await list_usdt_symbols()
        new = []
        for sym in symbols:
            if sym in state or sym in exclusion and exclusion[sym] > time.time():
                continue
            df = await get_klines(sym)
            if len(df) < 21:
                continue
            close = df['close']
            vol = df['volume']
            upper, _ = bollinger_bands(close)
            if close.iloc[-1] > upper.iloc[-1] and vol.iloc[-1] >= 2 * vol.tail(20).mean() and rsi(close).iloc[-1] > 50:
                state[sym] = {'status': 'RESERVADA_PRE', 'ts': time.time()}
                new.append(sym)
        if new:
            await notify(f'Fase 1 – nuevas rupturas: {", ".join(new)}')
