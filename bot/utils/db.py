from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///users.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)


def init_db():
    Base.metadata.create_all(engine)


def add_user(user_id: int):
    session = Session()
    exists = session.query(User).filter_by(id=user_id).first()
    if not exists:
        session.add(User(id=user_id))
        session.commit()
    session.close()


def get_all_user_ids(exclude_id=None):
    session = Session()
    query = session.query(User)
    if exclude_id is not None:
        query = query.filter(User.id != exclude_id)
    users = query.all()
    session.close()
    return [user.id for user in users]


def delete_user(user_id: int):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
    session.close()
