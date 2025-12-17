from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class QueryLog(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), nullable=False)
    query_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    responses = relationship("ResponseLog", back_populates="query")


class ResponseLog(Base):
    __tablename__ = "response_logs"
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    query = relationship("QueryLog", back_populates="responses")
    citations = relationship("Citation", back_populates="response")


class Citation(Base):
    __tablename__ = "citations"
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("response_logs.id"), nullable=False)
    source = Column(String(256), nullable=False)
    link = Column(String(512), nullable=True)

    response = relationship("ResponseLog", back_populates="citations")


class UserSession(Base):
    __tablename__ = "user_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), nullable=False)
    token = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    report_url = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

