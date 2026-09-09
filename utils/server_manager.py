"""
Менеджер серверов - управление VPN серверами
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from database import AsyncSessionLocal, Server


class ServerManager:
    """Управление VPN серверами"""

    @staticmethod
    async def add_server(
        protocol: str,
        config_data: str,
        country: str = None,
        city: str = None,
        ip_address: str = None,
        port: int = None,
        source_url: str = None,
        source_name: str = None
    ) -> Server:
        """Добавить новый сервер"""
        async with AsyncSessionLocal() as session:
            server = Server(
                protocol=protocol,
                config_data=config_data,
                country=country,
                city=city,
                ip_address=ip_address,
                port=port,
                source_url=source_url,
                source_name=source_name,
                is_active=True,
                last_checked=datetime.utcnow()
            )
            session.add(server)
            await session.commit()
            await session.refresh(server)
            return server

    @staticmethod
    async def get_random_server(protocol: str) -> Optional[Server]:
        """Получить случайный активный сервер"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Server)
                .where(Server.protocol == protocol, Server.is_active == True)
                .order_by(Server.last_checked.desc())
                .limit(10)
            )
            servers = result.scalars().all()
            if servers:
                import random
                return random.choice(servers)
            return None

    @staticmethod
    async def get_servers_by_protocol(
        protocol: str,
        limit: int = 10,
        offset: int = 0
    ) -> List[Server]:
        """Получить список серверов по протоколу"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Server)
                .where(Server.protocol == protocol, Server.is_active == True)
                .order_by(Server.last_checked.desc())
                .limit(limit)
                .offset(offset)
            )
            return result.scalars().all()

    @staticmethod
    async def deactivate_server(server_id: int):
        """Деактивировать сервер"""
        async with AsyncSessionLocal() as session:
            server = await session.get(Server, server_id)
            if server:
                server.is_active = False
                server.fail_count += 1
                await session.commit()

    @staticmethod
    async def update_server_metrics(
        server_id: int,
        speed_mbps: float = None,
        ping_ms: float = None
    ):
        """Обновить метрики сервера"""
        async with AsyncSessionLocal() as session:
            server = await session.get(Server, server_id)
            if server:
                if speed_mbps is not None:
                    server.speed_mbps = speed_mbps
                if ping_ms is not None:
                    server.ping_ms = ping_ms
                server.last_checked = datetime.utcnow()
                await session.commit()

    @staticmethod
    async def bulk_add_servers(servers_data: List[dict]) -> int:
        """Массовое добавление серверов"""
        added = 0
        async with AsyncSessionLocal() as session:
            for data in servers_data:
                # Проверяем, не существует ли уже такой сервер
                existing = await session.execute(
                    select(Server).where(
                        Server.protocol == data['protocol'],
                        Server.config_data == data['config_data']
                    )
                )
                if not existing.scalar_one_or_none():
                    server = Server(**data, is_active=True)
                    session.add(server)
                    added += 1

            await session.commit()
        return added

    @staticmethod
    async def cleanup_old_servers(days: int = 7):
        """Удалить старые неактивные серверы"""
        from datetime import timedelta
        async with AsyncSessionLocal() as session:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            result = await session.execute(
                select(Server).where(
                    Server.is_active == False,
                    Server.last_checked < cutoff_date
                )
            )
            servers = result.scalars().all()
            for server in servers:
                await session.delete(server)
            await session.commit()
            return len(servers)
