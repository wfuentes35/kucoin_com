from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import settings

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bot running.')

async def listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.bot_data.get('state', {})
    active = [s for s in state if state[s]['status'].startswith('COMPRADA')]
    reserved = [s for s in state if state[s]['status'] == 'RESERVADA_PRE']
    msg = f"\uD83C\uDFF0 {len(active)}/{settings.MAX_OPERACIONES_ACTIVAS} operaciones activas\n"
    msg += 'Reservadas: ' + ', '.join(reserved)
    await update.message.reply_text(msg)

def setup(app: Application, state: dict):
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('listar', listar))
