"""
Главная точка входа для запуска SendVPN бота
"""
import sys
import os
import asyncio

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.main import main

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════╗
║                                           ║
║           SendVPN Bot v1.0.0              ║
║   Крупнейший агрегатор бесплатных VPN     ║
║                                           ║
╚═══════════════════════════════════════════╝
    """)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
