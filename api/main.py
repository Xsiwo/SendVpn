"""
REST API для SendVPN
Предоставляет endpoints для Android-приложения
"""
import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal, User, Server, UsageStats
from config.protocols import PROTOCOLS, CATEGORIES, get_protocol_by_category
from api.models import (
    ServerResponse,
    CategoryResponse,
    ProtocolResponse,
    StatsResponse,
    ServerListResponse
)

# FastAPI приложение
app = FastAPI(
    title="SendVPN API",
    description="REST API для получения бесплатных VPN серверов",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS для Android-приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_db() -> AsyncSession:
    """Dependency для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "name": "SendVPN API",
        "version": "1.0.0",
        "endpoints": {
            "categories": "/api/categories",
            "protocols": "/api/protocols",
            "servers": "/api/servers",
            "random_server": "/api/servers/random",
            "stats": "/api/stats"
        }
    }


@app.get("/api/categories", response_model=List[CategoryResponse])
async def get_categories():
    """Получить все категории протоколов"""
    result = []
    for cat_key, cat_data in CATEGORIES.items():
        protocols = get_protocol_by_category(cat_key)
        result.append(CategoryResponse(
            key=cat_key,
            name=cat_data['name'],
            description=cat_data['description'],
            protocols_count=len(protocols)
        ))
    return result


@app.get("/api/protocols", response_model=List[ProtocolResponse])
async def get_protocols(category: Optional[str] = None):
    """
    Получить все протоколы или протоколы конкретной категории

    Args:
        category: Ключ категории (опционально)
    """
    if category:
        if category not in CATEGORIES:
            raise HTTPException(status_code=404, detail="Category not found")
        protocols = get_protocol_by_category(category)
    else:
        protocols = [
            {**data, "key": key}
            for key, data in PROTOCOLS.items()
        ]

    return [
        ProtocolResponse(
            key=p['key'],
            name=p['name'],
            emoji=p['emoji'],
            category=p['category'],
            description=p['description'],
            platforms=p['platforms'],
            config_format=p['config_format']
        )
        for p in protocols
    ]


@app.get("/api/servers", response_model=ServerListResponse)
async def get_servers(
    protocol: Optional[str] = None,
    country: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список серверов с фильтрацией

    Args:
        protocol: Фильтр по протоколу
        country: Фильтр по стране
        limit: Количество серверов (1-100)
        offset: Смещение для пагинации
    """
    query = select(Server).where(Server.is_active == True)

    if protocol:
        if protocol not in PROTOCOLS:
            raise HTTPException(status_code=404, detail="Protocol not found")
        query = query.where(Server.protocol == protocol)

    if country:
        query = query.where(Server.country == country)

    # Подсчёт общего количества
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Получение серверов
    query = query.order_by(Server.last_checked.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    servers = result.scalars().all()

    return ServerListResponse(
        total=total,
        limit=limit,
        offset=offset,
        servers=[
            ServerResponse(
                id=s.id,
                protocol=s.protocol,
                config_data=s.config_data,
                country=s.country,
                city=s.city,
                ip_address=s.ip_address,
                port=s.port,
                speed_mbps=s.speed_mbps,
                ping_ms=s.ping_ms,
                last_checked=s.last_checked.isoformat() if s.last_checked else None
            )
            for s in servers
        ]
    )


@app.get("/api/servers/random", response_model=ServerResponse)
async def get_random_server(
    protocol: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Получить случайный сервер для протокола

    Args:
        protocol: Ключ протокола (обязательно)
    """
    if protocol not in PROTOCOLS:
        raise HTTPException(status_code=404, detail="Protocol not found")

    query = select(Server).where(
        Server.protocol == protocol,
        Server.is_active == True
    ).order_by(func.random()).limit(1)

    result = await db.execute(query)
    server = result.scalar_one_or_none()

    if not server:
        raise HTTPException(
            status_code=404,
            detail=f"No active servers found for protocol: {protocol}"
        )

    return ServerResponse(
        id=server.id,
        protocol=server.protocol,
        config_data=server.config_data,
        country=server.country,
        city=server.city,
        ip_address=server.ip_address,
        port=server.port,
        speed_mbps=server.speed_mbps,
        ping_ms=server.ping_ms,
        last_checked=server.last_checked.isoformat() if server.last_checked else None
    )


@app.get("/api/servers/{server_id}", response_model=ServerResponse)
async def get_server(
    server_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить конкретный сервер по ID"""
    server = await db.get(Server, server_id)

    if not server or not server.is_active:
        raise HTTPException(status_code=404, detail="Server not found")

    return ServerResponse(
        id=server.id,
        protocol=server.protocol,
        config_data=server.config_data,
        country=server.country,
        city=server.city,
        ip_address=server.ip_address,
        port=server.port,
        speed_mbps=server.speed_mbps,
        ping_ms=server.ping_ms,
        last_checked=server.last_checked.isoformat() if server.last_checked else None
    )


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Получить статистику проекта"""
    total_users = await db.scalar(select(func.count(User.id))) or 0
    total_servers = await db.scalar(select(func.count(Server.id))) or 0
    active_servers = await db.scalar(
        select(func.count(Server.id)).where(Server.is_active == True)
    ) or 0

    return StatsResponse(
        total_users=total_users,
        total_servers=total_servers,
        active_servers=active_servers,
        total_protocols=len(PROTOCOLS),
        total_categories=len(CATEGORIES)
    )


@app.get("/api/countries")
async def get_countries(db: AsyncSession = Depends(get_db)):
    """Получить список доступных стран"""
    result = await db.execute(
        select(Server.country, func.count(Server.id))
        .where(Server.is_active == True, Server.country.isnot(None))
        .group_by(Server.country)
        .order_by(func.count(Server.id).desc())
    )

    countries = [
        {"country": row[0], "count": row[1]}
        for row in result.all()
    ]

    return {"countries": countries}


@app.get("/health")
async def health_check():
    """Health check для мониторинга"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
