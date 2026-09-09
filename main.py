"""
Главный файл запуска с FastAPI и Telegram ботом
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def run_bot():
    """Запуск Telegram бота"""
    from bot.main import main
    await main()


async def run_api():
    """Запуск FastAPI сервера"""
    import uvicorn
    from api.main import app
    from database import init_db

    # Инициализация БД
    await init_db()

    # Запуск API
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def run_all():
    """Запуск и бота и API одновременно"""
    from database import init_db

    print("""
╔═══════════════════════════════════════════╗
║                                           ║
║           SendVPN v1.0.0                  ║
║   Bot + API Server                        ║
║                                           ║
╚═══════════════════════════════════════════╝
    """)

    # Инициализация БД
    await init_db()

    # Запускаем оба сервиса параллельно
    await asyncio.gather(
        run_bot(),
        run_api()
    )


if __name__ == '__main__':
    mode = os.getenv('MODE', 'all')  # bot, api, или all

    try:
        if mode == 'bot':
            print("🤖 Запуск только Telegram бота...")
            asyncio.run(run_bot())
        elif mode == 'api':
            print("🌐 Запуск только API сервера...")
            asyncio.run(run_api())
        else:
            print("🚀 Запуск бота и API...")
            asyncio.run(run_all())
    except KeyboardInterrupt:
        print("\n\n👋 Сервисы остановлены")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
