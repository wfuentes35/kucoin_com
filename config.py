import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    KUCOIN_KEY: str = os.getenv('KUCOIN_KEY', '')
    KUCOIN_SECRET: str = os.getenv('KUCOIN_SECRET', '')
    KUCOIN_PASSPHRASE: str = os.getenv('KUCOIN_PASSPHRASE', '')

    TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID: str = os.getenv('TELEGRAM_CHAT_ID', '')

    DRY_RUN: bool = os.getenv('DRY_RUN', 'true').lower() == 'true'
    ENTRY_USDT: float = float(os.getenv('ENTRY_USDT', '20'))
    STOP_DELTA_USDT: float = float(os.getenv('STOP_DELTA_USDT', '1'))
    STOP_ABS_USDT: float = float(os.getenv('STOP_ABS_USDT', '18'))
    MAX_OPERACIONES_ACTIVAS: int = int(os.getenv('MAX_OPERACIONES_ACTIVAS', '30'))
    MAX_CONCURRENCY: int = int(os.getenv('MAX_CONCURRENCY', '12'))
    SCAN_INTERVAL: int = int(os.getenv('SCAN_INTERVAL', '900'))
    CHECK_INTERVAL: int = int(os.getenv('CHECK_INTERVAL', '600'))
    SYNC_POS_INTERVAL: int = int(os.getenv('SYNC_POS_INTERVAL', '900'))
    STARTUP_DELAY_FOR_PHASE1: int = int(os.getenv('STARTUP_DELAY_FOR_PHASE1', '60'))
    COOLDOWN_SECS: int = int(os.getenv('COOLDOWN_SECS', '14400'))
    MIN_24H_TURNOVER_USDT: float = float(os.getenv('MIN_24H_TURNOVER_USDT', '50000'))
    TRAILING_ATR_ON: bool = os.getenv('TRAILING_ATR_ON', 'false').lower() == 'true'

settings = Settings()
