import uuid

from datetime import datetime

from .extensions import db

from sqlalchemy.dialects.postgresql import UUID

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feedback_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "feedback_text": self.feedback_text,
            "created_at": self.created_at.isoformat()
        }

class Classification(db.Model):
    __tablename__ = 'classification'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sentiment = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    feedbacks_id = db.Column(UUID(as_uuid=True), db.ForeignKey('feedbacks.id'), nullable=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "code": self.code,
            "reason": self.reason,
            "feedbacks_id": str(self.feedbacks_id),
            "created_at": self.created_at.isoformat()
        }