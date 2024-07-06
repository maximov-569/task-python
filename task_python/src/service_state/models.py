from enum import Enum

from sqlalchemy import String, DateTime, Enum as EnumType, ForeignKey
from src.models import Base
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class StateChoice(Enum):
    work = "work"
    down = "down"
    unstable = "unstable"


class Service(Base):
    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    state: Mapped["StateChoice"] = mapped_column(EnumType(StateChoice), nullable=False)
    history: Mapped[list["ServiceStateHistory"]] = relationship(
        back_populates="service"
    )
    description: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )


class ServiceStateHistory(Base):
    time_in: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(tz=func.timezone.utc),
    )
    time_out: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), nullable=False)
    service: Mapped["Service"] = relationship(back_populates="history")
    state: Mapped["StateChoice"] = mapped_column(EnumType(StateChoice), nullable=False)
    description: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )
