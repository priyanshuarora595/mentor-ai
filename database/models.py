from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ModelConfig(Base):
    __tablename__ = "model_configs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    provider = Column(String)
    model_name = Column(String)
    api_key = Column(String)


class LearningTopic(Base):
    __tablename__ = "learning_topics"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    topic_name = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
