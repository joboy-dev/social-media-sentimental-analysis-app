import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database.models.base import BaseTableModel


class SentimentAnalysis(BaseTableModel):
    __tablename__ = "sentiments"

    text = sa.Column(sa.Text, nullable=False)
    label = sa.Column(sa.Integer, nullable=False)
    label_str = sa.Column(sa.String(10), nullable=False)
    
    user_id = sa.Column(sa.String, sa.ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="sentiments")
    