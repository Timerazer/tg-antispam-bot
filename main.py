import asyncio
import re
from aiogram import Bot, Dispatcher
from aiogram.types import Message

# Твой токен от BotFather
BOT_TOKEN = "8622320029:AAFHn9XxR9GT8hYnMyEi0aGSfaZDlflImuQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Полная объединённая база паттернов спама и скама
SPAM_PATTERNS = [
    # 1. Ссылки, инвайты и сокращатели (старое)
    r"t\.me/\+",
    r"t\.me/joinchat",
    r"bit\.ly|tinyurl|clck\.ru",
    r"fragment\.com",              # Фишинговые зеркала Fragment
    r"getgems|market.*nft",

    # 2. Скам по NFT, подаркам, звёздам и юзернеймам (новое)
    r"куплю.*(нфт|nft|подарок|подарки|гифт|gift)",
    r"продай.*(нфт|nft|подарок|подарки|юзер|тег|username)",
    r"скупаю.*(нфт|nft|подарки|gifts|звезд|stars)",
    r"цена.*(нфт|nft|подарк|профил)",
    r"продать.*(нфт|nft|подарок|подарки)",

    # 3. Крипта, инвестиции и схемы заработка (старое)
    r"крипт|доход|инвестиц|заработ",
    r"пассивный доход|раскрутка",
    r"вывод средств|дарю|выиграл",
    r"дроп|usdt|airdrop|tonkeeper",

    # 4. Накрутки и сомнительные услуги (старое)
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

# Обработка входящих сообщений через режим секретаря (Business)
@dp.business_message()
async def handle_incoming_business_message(message: Message):
    text = message.text or message.caption or ""
    
    if is_spam(text):
        try:
            # Удаляем спам-сообщение из твоего личного диалога
            await bot.delete_messages(
                chat_id=message.chat.id,
                message_ids=[message.message_id]
            )
            # Отправляем предупреждение спамеру от твоего имени
            await message.answer(
                "⚠️ Ваше сообщение удалено автоматическим спам-фильтром."
            )
            print(f"[BLOCKED] Скам/спам от {message.from_user.id}: {text[:40]}...")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
    else:
        # Чистое сообщение — спокойно остаётся в диалоге
        print(f"[OK] Чистое сообщение от {message.from_user.id}")

async def main():
    print("Бизнес-фильтр успешно запущен и слушает входящие сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
