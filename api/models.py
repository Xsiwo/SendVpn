"""
Pydantic модели для API
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class ServerResponse(BaseModel):
    """Модель ответа с сервером"""
    id: int
    protocol: str
    config_data: str
    country: Optional[str] = None
    city: Optional[str] = None
    ip_address: Optional[str] = None
    port: Optional[int] = None
    speed_mbps: Optional[float] = None
    ping_ms: Optional[float] = None
    last_checked: Optional[str] = None


class ServerListResponse(BaseModel):
    """Модель ответа со списком серверов"""
    total: int
    limit: int
    offset: int
    servers: List[ServerResponse]


class CategoryResponse(BaseModel):
    """Модель категории"""
    key: str
    name: str
    description: str
    protocols_count: int


class ProtocolResponse(BaseModel):
    """Модель протокола"""
    key: str
    name: str
    emoji: str
    category: str
    description: str
    platforms: List[str]
    config_format: str


class StatsResponse(BaseModel):
    """Модель статистики"""
    total_users: int
    total_servers: int
    active_servers: int
    total_protocols: int
    total_categories: int


class ErrorResponse(BaseModel):
    """Модель ошибки"""
    detail: str
