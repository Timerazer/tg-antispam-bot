import asyncio
import os
import re
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message

# Вставьте сюда актуальный токен бота из BotFather без пробелов по краям
BOT_TOKEN = "8622320029:AAFHn9XxR9GT8hYnMyEi0aGSfaZDlflImuQ"

bot = Bot(token=BOT_TOKEN.strip())
dp = Dispatcher()

# Шаблоны спама, скама, NFT и подарков
SPAM_PATTERNS = [
    r"t\.me/\+",
    r"t\.me/joinchat",
    r"bit\.ly|tinyurl|clck\.ru",
    r"fragment\.com",
    r"getgems|market.*nft",
    r"куплю.*(нфт|nft|подарок|подарки|гифт|gift)",
    r"продай.*(нфт|nft|подарок|подарки|юзер|тег|username)",
    r"скупаю.*(нфт|nft|подарки|gifts|звезд|stars)",
    r"цена.*(нфт|nft|подарк|профил)",
    r"продать.*(нфт|nft|подарок|подарки)",
    r"крипт|доход|инвестиц|заработ",
    r"пассивный доход|раскрутка",
    r"вывод средств|дарю|выиграл",
    r"дроп|usdt|airdrop|tonkeeper",
    r"накрутк|продвижени|взлом",
]

def is_spam(text: str) -> bool:
    if not text:
        return False
    lower_text = text.lower()
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, lower_text):
            return True
    return False

@dp.business_message()
async def handle_incoming_business_message(message: Message):
    text = message.text or message.caption or ""
    if is_spam(text):
        try:
            await bot.delete_messages(
                chat_id=message.chat.id,
                message_ids=[message.message_id]
            )
            await message.answer(
                "⚠️ Ваше сообщение удалено автоматическим спам-фильтром."
            )
            print(f"[BLOCKED] Спам от {message.from_user.id}: {text[:30]}...")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
    else:
        print(f"[OK] Чистое сообщение от {message.from_user.id}")

async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def main():
    # Фейковый веб-сервер для бесплатного тарифа Render (порт из переменной PORT или 10000)
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Веб-сервер слушает порт {port}")

    print("Бизнес-фильтр успешно запущен и слушает входящие сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

