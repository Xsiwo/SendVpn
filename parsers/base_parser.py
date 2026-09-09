"""
Базовый класс для парсеров VPN конфигураций
"""
import re
import base64
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup


class BaseParser(ABC):
    """Базовый парсер"""

    def __init__(self, source_name: str, source_url: str):
        self.source_name = source_name
        self.source_url = source_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def parse(self) -> List[Dict]:
        """Парсинг конфигураций. Должен вернуть список словарей с серверами"""
        pass

    async def fetch_url(self, url: str) -> Optional[str]:
        """Получить содержимое URL"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"❌ Ошибка загрузки {url}: {e}")
        return None

    def extract_vmess(self, text: str) -> List[Dict]:
        """Извлечь VMess конфигурации"""
        configs = []
        pattern = r'vmess://([A-Za-z0-9+/=]+)'
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                decoded = base64.b64decode(match).decode('utf-8')
                config = json.loads(decoded)
                configs.append({
                    'protocol': 'vmess',
                    'config_data': f"vmess://{match}",
                    'ip_address': config.get('add'),
                    'port': config.get('port'),
                    'country': config.get('ps', '').split()[0] if config.get('ps') else None
                })
            except:
                pass
        return configs

    def extract_vless(self, text: str) -> List[Dict]:
        """Извлечь VLESS конфигурации"""
        configs = []
        pattern = r'vless://([^\s]+)'
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                configs.append({
                    'protocol': 'vless',
                    'config_data': f"vless://{match}",
                    'ip_address': self._extract_ip_from_url(match),
                    'port': self._extract_port_from_url(match)
                })
            except:
                pass
        return configs

    def extract_trojan(self, text: str) -> List[Dict]:
        """Извлечь Trojan конфигурации"""
        configs = []
        pattern = r'trojan://([^\s]+)'
        matches = re.findall(pattern, text)

        for match in matches:
            configs.append({
                'protocol': 'trojan',
                'config_data': f"trojan://{match}",
                'ip_address': self._extract_ip_from_url(match),
                'port': self._extract_port_from_url(match)
            })
        return configs

    def extract_shadowsocks(self, text: str) -> List[Dict]:
        """Извлечь Shadowsocks конфигурации"""
        configs = []
        pattern = r'ss://([A-Za-z0-9+/=]+(?:#[^\s]+)?)'
        matches = re.findall(pattern, text)

        for match in matches:
            configs.append({
                'protocol': 'shadowsocks',
                'config_data': f"ss://{match}",
                'ip_address': None,
                'port': None
            })
        return configs

    def extract_hysteria2(self, text: str) -> List[Dict]:
        """Извлечь Hysteria2 конфигурации"""
        configs = []
        pattern = r'hysteria2://([^\s]+)'
        matches = re.findall(pattern, text)

        for match in matches:
            configs.append({
                'protocol': 'hysteria2',
                'config_data': f"hysteria2://{match}",
                'ip_address': self._extract_ip_from_url(match),
                'port': self._extract_port_from_url(match)
            })
        return configs

    def extract_wireguard(self, text: str) -> List[Dict]:
        """Извлечь WireGuard конфигурации"""
        configs = []
        # Ищем блоки [Interface] и [Peer]
        if '[Interface]' in text and '[Peer]' in text:
            configs.append({
                'protocol': 'wireguard',
                'config_data': text,
                'ip_address': None,
                'port': None
            })
        return configs

    def _extract_ip_from_url(self, url: str) -> Optional[str]:
        """Извлечь IP из URL"""
        match = re.search(r'@?(\d+\.\d+\.\d+\.\d+)', url)
        if match:
            return match.group(1)
        # IPv6 или домен
        match = re.search(r'@?([a-zA-Z0-9.-]+)', url)
        return match.group(1) if match else None

    def _extract_port_from_url(self, url: str) -> Optional[int]:
        """Извлечь порт из URL"""
        match = re.search(r':(\d+)', url)
        if match:
            try:
                return int(match.group(1))
            except:
                pass
        return None
