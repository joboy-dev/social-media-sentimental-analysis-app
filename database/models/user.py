import sqlalchemy as sa
from sqlalchemy import event, update
from sqlalchemy.orm import relationship, Session

from database.models.base import BaseTableModel


class User(BaseTableModel):
    __tablename__ = "users"
    
    name = sa.Column(sa.String(255), nullable=True)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    profile_picture = sa.Column(sa.String(255), nullable=True)
    
    sentiments = relationship("SentimentAnalysis", back_populates="user")
    batch_sentiments = relationship("BatchSentimentAnalysis", back_populates="user")


def user_after_insert(mapper, connection, target):
    try:
        # Update expiration time to 1 hour ahead
        connection.execute(
            update(User)
            .where(User.id == target.id)
            .values(
                profile_picture=f"https://ui-avatars.com/api/?name={target.name if target.name else target.email.split('@')[0]}",
            )
        )
    
    except Exception as e:
        print(f'An exception occured: {str(e)}')
        
event.listen(User, 'after_insert', user_after_insert)