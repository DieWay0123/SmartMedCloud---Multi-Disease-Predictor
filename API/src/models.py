from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, func, DateTime, String, ForeignKey

from datetime import datetime


class Base(DeclarativeBase):
    id_: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, unique=False, index=False, nullable=False, default=func.now())


class MappingKey(Base):
    __tablename__ = "mapping_keys"

    name: Mapped[str] = mapped_column(String(length=50), unique=True, index=False, nullable=False)

    mapping_values: Mapped[list["MappingValue"]] = relationship(
        "MappingValue", primaryjoin="MappingKey.id_ == MappingValue.key_id", uselist=True, back_populates="mapping_key")


class MappingValue(Base):
    __tablename__ = "mapping_values"

    name: Mapped[str] = mapped_column(String(length=100), unique=True, index=False, nullable=False)
    key_id: Mapped[int] = mapped_column(ForeignKey("mapping_keys.id_", ondelete="RESTRICT", onupdate="CASCADE"), 
                                        unique=False, index=False, nullable=False)

    mapping_key: Mapped["MappingKey"] = relationship(
        "MappingKey", primaryjoin="MappingValue.key_id == MappingKey.id_", uselist=False, back_populates="mapping_values")