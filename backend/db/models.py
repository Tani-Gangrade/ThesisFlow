from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, Table, DateTime, LargeBinary
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# Thesis table
class Thesis(Base):
    __tablename__ = "thesis"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    sections = relationship("Section", back_populates="thesis")

# Section table
class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)
    thesis_id = Column(Integer, ForeignKey("thesis.id"))
    name = Column(String, nullable=False)   # e.g. "3.2 Computational Efficiency"

    thesis = relationship("Thesis", back_populates="sections")
    claims = relationship("Claim", back_populates="section")

# Claims table
class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.id"))

    text = Column(Text, nullable=False)
    required_evidence = Column(Integer, default=3)
    current_evidence = Column(Integer, default=0)

    section = relationship("Section", back_populates="claims")
    papers = relationship("Paper", secondary="claim_papers")

# Paper table
class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(Text)
    evidence_type = Column(String)      # benchmark / theory / deployment
    limitations = Column(Text)

    claims = relationship("Claim", secondary="claim_papers")

# Memory table
class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)  # user | assistant | system
    content = Column(Text, nullable=False)
    embedding = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Claim to paper mapping
claim_papers = Table(
    "claim_papers",
    Base.metadata,
    Column("claim_id", Integer, ForeignKey("claims.id")),
    Column("paper_id", Integer, ForeignKey("papers.id"))
)
