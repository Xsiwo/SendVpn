"""
Парсер веб-сайтов с VPN конфигурациями
"""
from typing import List, Dict
from bs4 import BeautifulSoup
from .base_parser import BaseParser


class WebParser(BaseParser):
    """Парсер веб-сайтов"""

    # Популярные сайты с бесплатными VPN
    SITES = [
        'https://www.vpngate.net/en/',
        'https://www.freevpn724.com/',
    ]

    async def parse(self) -> List[Dict]:
        """Парсинг конфигураций с веб-сайтов"""
        all_configs = []

        for site in self.SITES:
            try:
                content = await self.fetch_url(site)
                if content:
                    configs = self._parse_site(site, content)
                    all_configs.extend(configs)
            except Exception as e:
                print(f"❌ Ошибка парсинга {site}: {e}")

        print(f"✅ Web Parser: найдено {len(all_configs)} конфигураций")
        return all_configs

    def _parse_site(self, url: str, content: str) -> List[Dict]:
        """Парсинг конкретного сайта"""
        configs = []

        if 'vpngate.net' in url:
            configs.extend(self._parse_vpngate(content))

        # Пробуем извлечь стандартные форматы
        configs.extend(self.extract_vmess(content))
        configs.extend(self.extract_vless(content))
        configs.extend(self.extract_trojan(content))
        configs.extend(self.extract_shadowsocks(content))

        return configs

    def _parse_vpngate(self, content: str) -> List[Dict]:
        """Парсинг VPNGate"""
        configs = []
        soup = BeautifulSoup(content, 'html.parser')

        # VPNGate предоставляет OpenVPN и L2TP
        # Ищем ссылки на .ovpn файлы
        for link in soup.find_all('a', href=True):
            if '.ovpn' in link['href']:
                configs.append({
                    'protocol': 'openvpn',
                    'config_data': link['href'],
                    'source_name': 'VPNGate',
                    'source_url': 'https://www.vpngate.net'
                })

        return configs
