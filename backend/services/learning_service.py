from database.db import engine, SessionLocal
from database.models import Base, LearningTopic

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


class LearningService:
    @staticmethod
    def save_topic(user_id, topic_name, content):
        db = SessionLocal()
        try:
            new_topic = LearningTopic(
                user_id=user_id, topic_name=topic_name, content=str(content)
            )
            db.add(new_topic)
            db.commit()
            db.refresh(new_topic)
            return new_topic
        finally:
            db.close()

    @staticmethod
    def get_user_topics(user_id):
        db = SessionLocal()
        try:
            return (
                db.query(LearningTopic).filter(LearningTopic.user_id == user_id).all()
            )
        finally:
            db.close()

    @staticmethod
    def get_stats(user_id):
        db = SessionLocal()
        try:
            topics_count = (
                db.query(LearningTopic).filter(LearningTopic.user_id == user_id).count()
            )
            return {
                "topics_learned": topics_count,
            }
        finally:
            db.close()

    @staticmethod
    def delete_topic(topic_id):
        db = SessionLocal()
        try:
            topic = db.query(LearningTopic).filter(LearningTopic.id == topic_id).first()
            if topic:
                db.delete(topic)
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def clear_history(user_id):
        db = SessionLocal()
        try:
            db.query(LearningTopic).filter(LearningTopic.user_id == user_id).delete()
            db.commit()
            return True
        finally:
            db.close()
