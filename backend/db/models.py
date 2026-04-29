"""
SQLAlchemy models for PostgreSQL — documents, queries, audit_logs.
"""
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String(50), unique=True, index=True)
    document_type = Column(String(100))
    source = Column(String(200))
    date = Column(String(50))
    client_ref = Column(String(50), index=True)
    status = Column(String(50))
    mandatory = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    client_ref = Column(String(50), nullable=True)
    query_text = Column(Text)
    response_summary = Column(Text, nullable=True)
    risk_score = Column(Float, nullable=True)
    compliance_flag = Column(String(20), nullable=True)
    tools_used = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)
    event_type = Column(String(100))   # tool_call | agent_start | agent_end | error
    tool_name = Column(String(100), nullable=True)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
