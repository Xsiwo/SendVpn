"""
Парсер GitHub репозиториев с VPN конфигурациями
"""
import re
from typing import List, Dict
from .base_parser import BaseParser


class GitHubParser(BaseParser):
    """Парсер GitHub репозиториев"""

    # Популярные репозитории с VPN конфигурациями
    REPOS = [
        'barry-far/V2ray-Configs',
        'mahdibland/V2RayAggregator',
        'mfuu/v2ray',
        'peasoft/NoMoreWalls',
        'AzadNetCH/3x-ui',
        'yebekhe/TelegramV2rayCollector',
        'MrPooya/v2ray',
        'SasukeFreestyle/FREE-VPN-V2RAY-DECENTRALIZED'
    ]

    def __init__(self, repo: str = None):
        self.repo = repo or self.REPOS[0]
        super().__init__(
            source_name=f"GitHub: {self.repo}",
            source_url=f"https://github.com/{self.repo}"
        )

    async def parse(self) -> List[Dict]:
        """Парсинг конфигураций из GitHub"""
        all_configs = []

        # Получаем raw файлы с конфигурациями
        raw_urls = [
            f"https://raw.githubusercontent.com/{self.repo}/main/All_Configs_Sub.txt",
            f"https://raw.githubusercontent.com/{self.repo}/main/Sub.txt",
            f"https://raw.githubusercontent.com/{self.repo}/main/configs.txt",
            f"https://raw.githubusercontent.com/{self.repo}/main/vmess.txt",
            f"https://raw.githubusercontent.com/{self.repo}/main/vless.txt",
            f"https://raw.githubusercontent.com/{self.repo}/main/trojan.txt",
            f"https://raw.githubusercontent.com/{self.repo}/main/ss.txt",
            f"https://raw.githubusercontent.com/{self.repo}/main/reality.txt",
            f"https://raw.githubusercontent.com/{self.repo}/main/hysteria.txt",
            f"https://raw.githubusercontent.com/{self.repo}/master/All_Configs_Sub.txt",
            f"https://raw.githubusercontent.com/{self.repo}/master/Sub.txt"
        ]

        for url in raw_urls:
            content = await self.fetch_url(url)
            if content:
                # Извлекаем все типы конфигураций
                all_configs.extend(self.extract_vmess(content))
                all_configs.extend(self.extract_vless(content))
                all_configs.extend(self.extract_trojan(content))
                all_configs.extend(self.extract_shadowsocks(content))
                all_configs.extend(self.extract_hysteria2(content))
                all_configs.extend(self.extract_wireguard(content))

        # Добавляем источник к каждой конфигурации
        for config in all_configs:
            config['source_name'] = self.source_name
            config['source_url'] = self.source_url

        print(f"✅ GitHub {self.repo}: найдено {len(all_configs)} конфигураций")
        return all_configs


class GitHubMultiParser:
    """Парсер нескольких GitHub репозиториев"""

    async def parse_all(self) -> List[Dict]:
        """Парсинг всех репозиториев"""
        all_configs = []

        for repo in GitHubParser.REPOS:
            try:
                async with GitHubParser(repo) as parser:
                    configs = await parser.parse()
                    all_configs.extend(configs)
            except Exception as e:
                print(f"❌ Ошибка парсинга {repo}: {e}")

        print(f"🎉 Всего найдено конфигураций: {len(all_configs)}")
        return all_configs
