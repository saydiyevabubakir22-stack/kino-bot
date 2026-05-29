from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8844307417:AAGRIFQ791M-Iyb1WzqzVFg2bug4JjhiNm4"
CHANNEL = -1003588766770
ADMIN = 8476805197
DB = {}

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text("Salom! Kino nomini yozing")

async def add(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if u.effective_user.id != ADMIN:
        await u.message.reply_text("Faqat admin")
        return
    if len(c.args) < 2:
        await u.message.reply_text("Misol: /add Titanic 5")
        return
    mid = int(c.args[-1])
    name = " ".join(c.args[:-1])
    DB[name.lower()] = {"name": name, "mid": mid}
    await u.message.reply_text(name + " qoshildi")

async def lst(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not DB:
        await u.message.reply_text("Kino yoq")
        return
    await u.message.reply_text("\n".join(v["name"] for v in DB.values()))

async def search(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.message.text.lower()
    found = [v for k, v in DB.items() if q in k]
    if not found:
        await u.message.reply_text("Topilmadi")
        return
    try:
        await c.bot.forward_message(u.effective_chat.id, CHANNEL, found[0]["mid"])
    except:
        await u.message.reply_text("Xato")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", lst))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
app.run_polling()

