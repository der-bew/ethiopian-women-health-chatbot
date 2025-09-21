from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String)
    location = Column(String)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    title = Column(String)
    created_at = Column(DateTime, server_default="NOW()")
    updated_at = Column(DateTime, server_default="NOW()")

class Message(Base):
    __tablename__ = "messages"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(PG_UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default="NOW()")

class KnowledgeBaseMetadata(Base):
    __tablename__ = "knowledge_base_metadata"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String, nullable=False)
    uploaded_by = Column(PG_UUID(as_uuid=True), ForeignKey("auth.users.id"))
    upload_date = Column(DateTime, server_default="NOW()")
    indexed = Column(Boolean, default=False)
