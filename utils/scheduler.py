"""
Планировщик задач - автоматический парсинг и проверка серверов
"""
import asyncio
from datetime import datetime
from parsers import GitHubMultiParser, WebParser
from utils.server_manager import ServerManager


class TaskScheduler:
    """Планировщик фоновых задач"""

    def __init__(self, interval: int = 3600):
        self.interval = interval  # секунды
        self.is_running = False

    async def start(self):
        """Запустить планировщик"""
        self.is_running = True
        print("🔄 Планировщик запущен")

        while self.is_running:
            try:
                await self.run_parsing_task()
                await asyncio.sleep(self.interval)
            except Exception as e:
                print(f"❌ Ошибка в планировщике: {e}")
                await asyncio.sleep(60)  # Пауза перед повтором

    async def stop(self):
        """Остановить планировщик"""
        self.is_running = False
        print("⏹️ Планировщик остановлен")

    async def run_parsing_task(self):
        """Запустить задачу парсинга"""
        print(f"\n{'='*50}")
        print(f"🔄 Начало парсинга: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")

        total_added = 0

        # Парсинг GitHub репозиториев
        try:
            github_parser = GitHubMultiParser()
            github_configs = await github_parser.parse_all()
            if github_configs:
                added = await ServerManager.bulk_add_servers(github_configs)
                total_added += added
                print(f"✅ GitHub: добавлено {added} новых серверов")
        except Exception as e:
            print(f"❌ Ошибка парсинга GitHub: {e}")

        # Парсинг веб-сайтов
        try:
            async with WebParser('Web', 'https://web') as web_parser:
                web_configs = await web_parser.parse()
                if web_configs:
                    added = await ServerManager.bulk_add_servers(web_configs)
                    total_added += added
                    print(f"✅ Web: добавлено {added} новых серверов")
        except Exception as e:
            print(f"❌ Ошибка парсинга Web: {e}")

        # Очистка старых серверов
        try:
            removed = await ServerManager.cleanup_old_servers(days=7)
            print(f"🗑️ Удалено {removed} старых серверов")
        except Exception as e:
            print(f"❌ Ошибка очистки: {e}")

        print(f"\n{'='*50}")
        print(f"✅ Парсинг завершен: добавлено {total_added} серверов")
        print(f"⏰ Следующий запуск через {self.interval // 60} минут")
        print(f"{'='*50}\n")


async def run_scheduler():
    """Запуск планировщика"""
    scheduler = TaskScheduler(interval=3600)  # Каждый час
    await scheduler.start()


if __name__ == '__main__':
    asyncio.run(run_scheduler())
