import asyncio
import time
from pathlib import Path
from typing import Dict
import pandas as pd
from config import settings
from utils import get_klines, ema, append_sale_to_excel

EXCEL_PATH = Path('historial_ventas.xlsx')

async def run(state: Dict[str, dict], exclusion: Dict[str, float], notify):
    while True:
        await asyncio.sleep(settings.CHECK_INTERVAL)
        to_remove = []
        for sym, rec in list(state.items()):
            if rec.get('status') == 'RESERVADA_PRE':
                df = await get_klines(sym)
                if len(df) < 10:
                    continue
                ema9 = ema(df['close'], 9)
                bb_upper, _ = None, None
                if df['low'].iloc[-2] <= ema9.iloc[-2] and df['close'].iloc[-1] > df['close'].iloc[-2]:
                    price = df['close'].iloc[-1]
                    qty = settings.ENTRY_USDT / price
                    state[sym] = {
                        'status': 'COMPRADA',
                        'entry_price': price,
                        'entry_cost': settings.ENTRY_USDT,
                        'quantity': qty,
                        'max_value': price * qty,
                        'stop_delta': price * qty - settings.STOP_DELTA_USDT,
                        'stop_abs': settings.STOP_ABS_USDT,
                    }
                    await notify(f'Comprado {sym} @ {price:.4f}')
            elif rec.get('status', '').startswith('COMPRADA'):
                df = await get_klines(sym)
                if not len(df):
                    continue
                last = df['close'].iloc[-1]
                ema9 = ema(df['close'],9).iloc[-1]
                value_now = last * rec['quantity']
                rec['max_value'] = max(rec['max_value'], value_now)
                rec['stop_delta'] = max(rec['stop_delta'], rec['max_value'] - settings.STOP_DELTA_USDT)
                if last < ema9 or value_now <= rec['stop_delta'] or value_now <= rec['stop_abs']:
                    pnl = value_now - rec['entry_cost']
                    await notify(f'Venta {sym} pnl {pnl:.2f}')
                    append_sale_to_excel(EXCEL_PATH, {
                        'timestamp': pd.Timestamp.utcnow().isoformat(),
                        'symbol': sym,
                        'side': 'SELL',
                        'valor_vendido_usdt': value_now,
                        'fee_usdt': 0,
                        'pnl_usdt': pnl,
                        'pnl_pct': pnl / rec['entry_cost'] * 100,
                        'resultado': 'positivo' if pnl>0 else 'negativo',
                    })
                    exclusion[sym] = time.time() + settings.COOLDOWN_SECS
                    to_remove.append(sym)
        for sym in to_remove:
            state.pop(sym, None)

