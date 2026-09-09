"""
Database models для SendVPN
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), default='ru')
    is_premium = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)

    # Relationships
    usage_stats = relationship("UsageStats", back_populates="user", cascade="all, delete-orphan")
    donations = relationship("Donation", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.telegram_id} - {self.username}>"


class Server(Base):
    """Модель VPN сервера"""
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    protocol = Column(String(50), nullable=False, index=True)
    config_data = Column(Text, nullable=False)  # JSON или base64
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    ip_address = Column(String(45), nullable=True)
    port = Column(Integer, nullable=True)

    # Статус
    is_active = Column(Boolean, default=True, index=True)
    last_checked = Column(DateTime, default=datetime.utcnow)
    check_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)

    # Метрики
    speed_mbps = Column(Float, nullable=True)
    ping_ms = Column(Float, nullable=True)

    # Источник
    source_url = Column(String(500), nullable=True)
    source_name = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    usage_stats = relationship("UsageStats", back_populates="server", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Server {self.protocol} - {self.country}>"


class UsageStats(Base):
    """Статистика использования серверов"""
    __tablename__ = 'usage_stats'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    server_id = Column(Integer, ForeignKey('servers.id'), nullable=False, index=True)
    accessed_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="usage_stats")
    server = relationship("Server", back_populates="usage_stats")

    def __repr__(self):
        return f"<UsageStats user={self.user_id} server={self.server_id}>"


class Donation(Base):
    """История донатов"""
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default='RUB')
    payment_method = Column(String(50), nullable=True)  # yookassa, stripe, crypto
    transaction_id = Column(String(255), unique=True, nullable=True)
    status = Column(String(20), default='pending')  # pending, completed, failed
    message = Column(Text, nullable=True)  # Сообщение от донатера
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="donations")

    def __repr__(self):
        return f"<Donation {self.amount} {self.currency} from user {self.user_id}>"


class ParserSource(Base):
    """Источники для парсинга"""
    __tablename__ = 'parser_sources'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    source_type = Column(String(50), nullable=False)  # github, telegram, web
    url = Column(String(500), nullable=False)
    protocols = Column(String(500), nullable=True)  # JSON array
    is_active = Column(Boolean, default=True, index=True)
    last_parsed = Column(DateTime, nullable=True)
    success_rate = Column(Float, default=0.0)
    total_parsed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ParserSource {self.name} - {self.source_type}>"
