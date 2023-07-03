from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from models import User


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql/sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


# создаем сессию подключения к бд
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

# создаем объект Person для добавления в бд
tom = User(name="Tom", age=38)
db.add(tom)  # добавляем в бд
db.commit()  # сохраняем изменения


def get_session():
    return db
