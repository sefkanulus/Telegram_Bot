from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters
import asyncio
from exchange_rate_api import data

bot_token = "YOUR TOKEN"
yourchatid = "Your chat id"

async def daha_fazla(update: Update, context: CallbackContext):
    data_new = ""
    conversion_rates = data["conversion_rates"]
    for i, (para, deger) in enumerate(conversion_rates.items()):
        if i < 11 and para !=  "USD":            
            data_new = f"1 USD = {deger} {para} \n"  + data_new
    await context.bot.send_message(chat_id=yourchatid, text=data_new)    

async def background_task(application):
    data_new = ""
    conversion_rates = data["conversion_rates"]
    while True:
        for para, deger in conversion_rates.items():
            if para in {"TRY", "EUR", "GBP"}:
                data_new = f"1 USD = {deger} {para} \n"  + data_new
        data_new = data_new + "/daha_fazla"
        await application.bot.send_message(chat_id= yourchatid, text=data_new)
        await asyncio.sleep(5*60)  # 5 dakika bekle
        data_new = ""

async def search(update: Update, context: CallbackContext):
    conversion_rates = data["conversion_rates"]
    user_message = update.message.text
    for i, (para,deger) in enumerate(conversion_rates.items()):
        if (para == user_message.upper()):
            await update.message.reply_text(f"1 USD = {deger} {para}")

async def main(application):
    application.add_handler(CommandHandler("daha_fazla", daha_fazla))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    asyncio.create_task(background_task(application))
    
app = ApplicationBuilder().token(bot_token).post_init(main).build()

app.run_polling()



