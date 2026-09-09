"""
Конфигурация всех поддерживаемых VPN протоколов
"""

PROTOCOLS = {
    # === Основные VPN протоколы ===
    "wireguard": {
        "name": "WireGuard",
        "emoji": "⚡",
        "category": "mainstream",
        "description": "Быстрый и современный протокол",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "wireguard"
    },
    "openvpn": {
        "name": "OpenVPN",
        "emoji": "🔒",
        "category": "mainstream",
        "description": "Проверенный временем протокол",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "ovpn"
    },
    "amneziawg": {
        "name": "AmneziaWG",
        "emoji": "🛡️",
        "category": "mainstream",
        "description": "WireGuard с обфускацией",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "config_format": "wireguard"
    },
    "ikev2": {
        "name": "IKEv2 / IPsec",
        "emoji": "🔐",
        "category": "mainstream",
        "description": "Встроенная поддержка в iOS",
        "platforms": ["Windows", "macOS", "iOS", "Android"],
        "config_format": "ipsec"
    },
    "softether": {
        "name": "SoftEther",
        "emoji": "💎",
        "category": "mainstream",
        "description": "Мультипротокольный VPN",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "softether"
    },
    "sstp": {
        "name": "SSTP",
        "emoji": "🔗",
        "category": "mainstream",
        "description": "Протокол Microsoft",
        "platforms": ["Windows"],
        "config_format": "sstp"
    },
    "l2tp": {
        "name": "L2TP",
        "emoji": "📡",
        "category": "mainstream",
        "description": "Совместим с большинством устройств",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "l2tp"
    },
    "pptp": {
        "name": "PPTP",
        "emoji": "⚠️",
        "category": "mainstream",
        "description": "Устаревший, не рекомендуется",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "pptp"
    },

    # === Proxy протоколы ===
    "http": {
        "name": "HTTP Proxy",
        "emoji": "🌐",
        "category": "proxy",
        "description": "Простой HTTP прокси",
        "platforms": ["All"],
        "config_format": "url"
    },
    "https": {
        "name": "HTTPS Proxy",
        "emoji": "🔒",
        "category": "proxy",
        "description": "Безопасный HTTP прокси",
        "platforms": ["All"],
        "config_format": "url"
    },
    "socks4": {
        "name": "SOCKS4",
        "emoji": "🧦",
        "category": "proxy",
        "description": "SOCKS версия 4",
        "platforms": ["All"],
        "config_format": "url"
    },
    "socks5": {
        "name": "SOCKS5",
        "emoji": "🧦",
        "category": "proxy",
        "description": "SOCKS версия 5 с аутентификацией",
        "platforms": ["All"],
        "config_format": "url"
    },

    # === Shadowsocks семейство ===
    "shadowsocks": {
        "name": "Shadowsocks",
        "emoji": "🥷",
        "category": "shadowsocks",
        "description": "Классический Shadowsocks",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "ss"
    },
    "shadowsocksr": {
        "name": "ShadowsocksR (SSR)",
        "emoji": "🥷",
        "category": "shadowsocks",
        "description": "Shadowsocks с расширениями",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "config_format": "ssr"
    },
    "shadowsocks2022": {
        "name": "Shadowsocks 2022",
        "emoji": "🥷",
        "category": "shadowsocks",
        "description": "Новая версия протокола",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "ss"
    },
    "outline": {
        "name": "Outline",
        "emoji": "📝",
        "category": "shadowsocks",
        "description": "Shadowsocks от Jigsaw",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "ss"
    },

    # === V2Ray / Xray протоколы ===
    "vmess": {
        "name": "VMess",
        "emoji": "✈️",
        "category": "v2ray",
        "description": "Протокол V2Ray",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "vmess"
    },
    "vless": {
        "name": "VLESS",
        "emoji": "✈️",
        "category": "v2ray",
        "description": "Облегченная версия VMess",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "vless"
    },
    "trojan": {
        "name": "Trojan",
        "emoji": "🐴",
        "category": "v2ray",
        "description": "Маскировка под HTTPS",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "trojan"
    },
    "trojan_go": {
        "name": "Trojan-Go",
        "emoji": "🐴",
        "category": "v2ray",
        "description": "Улучшенная версия Trojan",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "config_format": "trojan"
    },

    # === Современные протоколы ===
    "brook": {
        "name": "Brook",
        "emoji": "🌊",
        "category": "modern",
        "description": "Простой и безопасный",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "brook"
    },
    "snell": {
        "name": "Snell",
        "emoji": "🐌",
        "category": "modern",
        "description": "Высокопроизводительный протокол",
        "platforms": ["macOS", "iOS"],
        "config_format": "snell"
    },
    "naiveproxy": {
        "name": "NaiveProxy",
        "emoji": "😇",
        "category": "modern",
        "description": "Обход глубокой инспекции пакетов",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "config_format": "naive"
    },
    "mieru": {
        "name": "Mieru",
        "emoji": "👁️",
        "category": "modern",
        "description": "Протокол обхода цензуры",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "mieru"
    },
    "juicity": {
        "name": "Juicity",
        "emoji": "🧃",
        "category": "modern",
        "description": "QUIC-based протокол",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "juicity"
    },

    # === Hysteria семейство ===
    "hysteria": {
        "name": "Hysteria",
        "emoji": "⚡",
        "category": "hysteria",
        "description": "Для нестабильных сетей",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "hysteria"
    },
    "hysteria2": {
        "name": "Hysteria2",
        "emoji": "⚡",
        "category": "hysteria",
        "description": "Улучшенная версия Hysteria",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "hysteria2"
    },
    "tuic": {
        "name": "TUIC",
        "emoji": "🚀",
        "category": "hysteria",
        "description": "QUIC-based протокол",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "tuic"
    },

    # === Обфускация и транспорты ===
    "reality": {
        "name": "Reality",
        "emoji": "🌌",
        "category": "obfuscation",
        "description": "VLESS + Reality обфускация",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "config_format": "vless"
    },
    "anytls": {
        "name": "AnyTLS",
        "emoji": "🔐",
        "category": "obfuscation",
        "description": "TLS обфускация",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "custom"
    },
    "shadowtls": {
        "name": "ShadowTLS",
        "emoji": "🥷",
        "category": "obfuscation",
        "description": "TLS маскировка",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "custom"
    },
    "xhttp": {
        "name": "XHTTP",
        "emoji": "🌐",
        "category": "obfuscation",
        "description": "HTTP/2 транспорт",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "custom"
    },
    "vision": {
        "name": "Vision (XTLS)",
        "emoji": "👁️",
        "category": "obfuscation",
        "description": "XTLS-Vision",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "custom"
    },
    "obfs4": {
        "name": "obfs4",
        "emoji": "🎭",
        "category": "obfuscation",
        "description": "Pluggable transport",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "custom"
    },
    "meek": {
        "name": "meek",
        "emoji": "🐭",
        "category": "obfuscation",
        "description": "Domain fronting",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "custom"
    },
    "snowflake": {
        "name": "Snowflake",
        "emoji": "❄️",
        "category": "obfuscation",
        "description": "WebRTC transport",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "custom"
    },

    # === Анонимные сети ===
    "tor": {
        "name": "Tor",
        "emoji": "🧅",
        "category": "anonymous",
        "description": "Сеть анонимности",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "config_format": "tor"
    },
    "i2p": {
        "name": "I2P",
        "emoji": "🔒",
        "category": "anonymous",
        "description": "Невидимый интернет-проект",
        "platforms": ["Windows", "macOS", "Linux", "Android"],
        "config_format": "i2p"
    },
    "freenet": {
        "name": "Freenet",
        "emoji": "🆓",
        "category": "anonymous",
        "description": "Децентрализованная сеть",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "freenet"
    },
    "lokinet": {
        "name": "Lokinet",
        "emoji": "🔐",
        "category": "anonymous",
        "description": "Анонимная overlay сеть",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "lokinet"
    },
    "nym": {
        "name": "Nym",
        "emoji": "🎭",
        "category": "anonymous",
        "description": "Mixnet для приватности",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "nym"
    },
    "yggdrasil": {
        "name": "Yggdrasil",
        "emoji": "🌳",
        "category": "anonymous",
        "description": "Mesh сеть",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "yggdrasil"
    },
    "cjdns": {
        "name": "CJDNS",
        "emoji": "🌐",
        "category": "anonymous",
        "description": "Шифрованная IPv6 сеть",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "cjdns"
    },

    # === DNS протоколы ===
    "doh": {
        "name": "DNS-over-HTTPS",
        "emoji": "🌐",
        "category": "dns",
        "description": "DNS через HTTPS",
        "platforms": ["All"],
        "config_format": "url"
    },
    "dot": {
        "name": "DNS-over-TLS",
        "emoji": "🔒",
        "category": "dns",
        "description": "DNS через TLS",
        "platforms": ["All"],
        "config_format": "url"
    },
    "doq": {
        "name": "DNS-over-QUIC",
        "emoji": "⚡",
        "category": "dns",
        "description": "DNS через QUIC",
        "platforms": ["All"],
        "config_format": "url"
    },
    "dnscrypt": {
        "name": "DNSCrypt",
        "emoji": "🔐",
        "category": "dns",
        "description": "Шифрованный DNS",
        "platforms": ["All"],
        "config_format": "dnscrypt"
    },

    # === Туннели ===
    "ssh": {
        "name": "SSH-туннель",
        "emoji": "🔑",
        "category": "tunnel",
        "description": "SSH туннелирование",
        "platforms": ["Windows", "macOS", "Linux", "iOS", "Android"],
        "config_format": "ssh"
    },
    "stunnel": {
        "name": "Stunnel",
        "emoji": "🔒",
        "category": "tunnel",
        "description": "TLS туннель",
        "platforms": ["Windows", "macOS", "Linux"],
        "config_format": "stunnel"
    },
}

# Категории для удобной навигации
CATEGORIES = {
    "mainstream": {
        "name": "🌟 Основные VPN",
        "description": "Популярные и надежные протоколы"
    },
    "proxy": {
        "name": "🌐 Прокси",
        "description": "HTTP, HTTPS, SOCKS протоколы"
    },
    "shadowsocks": {
        "name": "🥷 Shadowsocks",
        "description": "Семейство Shadowsocks протоколов"
    },
    "v2ray": {
        "name": "✈️ V2Ray / Xray",
        "description": "VMess, VLESS, Trojan"
    },
    "modern": {
        "name": "🚀 Современные",
        "description": "Новые протоколы обхода"
    },
    "hysteria": {
        "name": "⚡ Hysteria / QUIC",
        "description": "Протоколы на базе QUIC"
    },
    "obfuscation": {
        "name": "🎭 Обфускация",
        "description": "Транспорты для обхода DPI"
    },
    "anonymous": {
        "name": "🧅 Анонимные сети",
        "description": "Tor, I2P и другие"
    },
    "dns": {
        "name": "🌐 DNS протоколы",
        "description": "Безопасный DNS"
    },
    "tunnel": {
        "name": "🔑 Туннели",
        "description": "SSH, Stunnel и другие"
    }
}

def get_protocol_by_category(category: str) -> list:
    """Получить все протоколы по категории"""
    return [
        {**data, "key": key}
        for key, data in PROTOCOLS.items()
        if data.get("category") == category
    ]

def get_all_categories() -> dict:
    """Получить все категории с количеством протоколов"""
    result = {}
    for cat_key, cat_data in CATEGORIES.items():
        protocols = get_protocol_by_category(cat_key)
        result[cat_key] = {
            **cat_data,
            "count": len(protocols)
        }
    return result
