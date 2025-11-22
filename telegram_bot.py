import os
import logging
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramChatBot:
    def __init__(self):
        self.responses = {
            'привет': ['Привет! Как дела?', 'Здравствуйте!', 'Приветствую!'],
            'как дела': ['Отлично! А у вас?', 'Хорошо, спасибо!', 'Прекрасно!'],
            'погода': ['Сегодня солнечно!', 'Ожидается дождь', 'Погода прекрасная!'],
            'имя': ['Меня зовут Чат-бот', 'Я простой бот', 'Мое имя - Помощник'],
            'спасибо': ['Пожалуйста!', 'Рад помочь!', 'Обращайтесь!'],
            'команды': ['Доступные команды: /start, /help, /about'],
            'помощь': ['Я могу ответить на приветствие, рассказать о погоде, представиться']
        }
    
    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # Поиск ключевых слов
        for keyword, responses in self.responses.items():
            if keyword in user_input:
                return random.choice(responses)
        
        return "Извините, я еще не научился отвечать на это. Напишите 'помощь' для списка возможностей."

# Создаем экземпляр бота
chat_bot = TelegramChatBot()

# Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🤖 Добро пожаловать в чат-бот!

Я могу ответить на простые вопросы. Вот что я умею:
• Поздороваться (привет, здравствуйте)
• Рассказать о погоде
• Представиться
• Помочь с командами

Просто напишите мне сообщение!
    """
    await update.message.reply_text(welcome_text)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📋 Доступные команды:

/start - начать работу
/help - получить помощь
/about - о боте

💬 Я понимаю такие фразы:
• Привет, здравствуйте
• Как дела?
• Какая погода?
• Как тебя зовут?
• Помощь
    """
    await update.message.reply_text(help_text)

# Команда /about
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
О боте:

Это простой чат-бот, созданный на Python.
Использует библиотеку python-telegram-bot.

Бот распознает ключевые слова и отвечает
заранее подготовленными фразами.
    """
    await update.message.reply_text(about_text)

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    
    logger.info(f"User ({update.message.chat.id}) in {message_type}: '{text}'")
    
    if message_type == 'group':
        # В групповых чатах бот отвечает только если к нему обращаются
        if '@' in text or 'бот' in text.lower():
            response = chat_bot.get_response(text)
        else:
            return
    else:
        # В личных сообщениях отвечает на все
        response = chat_bot.get_response(text)
    
    await update.message.reply_text(response)

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")


def setup_environment():
    
    load_dotenv()
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден!")
        print("\n Как установить токен:")
        print("1. Создайте файл .env в папке проекта")
        print("2. Добавьте строку: TELEGRAM_BOT_TOKEN=ваш_токен_здесь")
        print("3. Перезапустите программу")
        print("\n Получить токен можно у @BotFather в Telegram")
        exit(1)
    
    # Проверяем формат токена
    if not token.startswith('') or ':' not in token:
        print("❌ Ошибка: Неверный формат токена!")
        print("Токен должен быть в формате: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
        exit(1)
    
    return token
        
# Основная функция
def main():
    if not TOKEN:
        logger.error("Токен не найден! Убедитесь, что файл .env существует и содержит TELEGRAM_BOT_TOKEN")
        return
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    TOKEN = setup_environment()
    main()
