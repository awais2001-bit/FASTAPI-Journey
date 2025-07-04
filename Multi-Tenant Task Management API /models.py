from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid

class Tenant(Base):
    __tablename__ = 'tenant'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenant.id'), nullable=False)


class Project(Base):
    __tablename__ = 'project'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenant.id'), nullable=False)


class Task(Base):
    __tablename__ = 'task'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    assigned_to_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey('project.id'), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenant.id'), nullable=False)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey('task.id'), nullable=False)




