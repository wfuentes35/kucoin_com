import asyncio
from telegram.ext import Application
from config import settings
from telegram_commands import setup as setup_commands
from fases import fase1, fase2, fase3, position_sync, manual_watcher

async def notify(msg: str):
    print(msg)

async def main():
    state = {}
    exclusion = {}
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.bot_data['state'] = state
    setup_commands(app, state)

    async def runner():
        await asyncio.gather(
            fase2.run(state, exclusion, notify),
            position_sync.run(state, notify),
            fase1.run(state, exclusion, notify),
            fase3.run(state, notify),
            manual_watcher.run(state)
        )
    task = asyncio.create_task(runner())
    await app.start()
    await app.updater.start_polling()
    await task

if __name__ == '__main__':
    asyncio.run(main())
