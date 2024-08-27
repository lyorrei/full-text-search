from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Text, Computed, Index
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR

class TSVector(sa.types.TypeDecorator):
    impl = TSVECTOR

metadata = MetaData()

Base = declarative_base(metadata=metadata)

class Card(Base):
    __tablename__ = "Card"

    index = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, index=True)

    text_vector = Column(
        TSVector(), 
        Computed("to_tsvector('english', text)", persisted=True)
    )

    __table_args__ = (
        Index('ix_card_text_vector', text_vector, postgresql_using='gin'),
    )