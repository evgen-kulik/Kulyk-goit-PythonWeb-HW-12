from typing import Type
from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import UserModel


async def get_users(skip: int, limit: int, db: Session) -> list[Type[User]]:
    return db.query(User).offset(skip).limit(limit).all()


async def get_user(user_id: int, db: Session) -> Type[User] | None:
    return db.query(User).filter(User.id == user_id).first()


# Тепер контакт додається тільки під час SignUp
# async def create_user_by_user(body: UserModel, db: Session) -> User:
#     contacts = db.query(Contact).filter(Contact.id.in_(body.contacts)).all()
#     user = User(name=body.name, last_name=body.last_name, day_of_born=body.day_of_born, email=body.email,
#                 description=body.description, contacts=contacts)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
# ---------------


async def remove_user(user_id: int, db: Session, user: User) -> User | None:
    # user = db.query(User).filter(User.id == user_id).first()
    user = db.query(User).filter(and_(User.id == user_id, User.id == user.id)).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def update_user(
    user_id: int, body: UserModel, db: Session, user: User
) -> User | None:
    user = db.query(User).filter(and_(User.id == user_id, User.id == user.id)).first()
    # User.id == user_id - підтягує юзера, з id, який задано
    # User.id == user.id - підтягує тільки юзера з id, який задано, щоб юзер міг редагувати тільки себе
    if user:
        phones = db.query(Contact).filter(Contact.id.in_(body.contacts)).all()
        user.name = body.name
        user.last_name = body.last_name
        user.day_of_born = body.day_of_born
        user.email = body.email
        user.description = body.description
        user.phones = phones
        db.commit()
    return user


async def find_user_by_name(user_name: str, db: Session) -> Type[User] | None:
    return db.query(User).filter(User.name == user_name).first()


async def find_user_by_last_name(user_last_name: str, db: Session) -> Type[User] | None:
    return db.query(User).filter(User.last_name == user_last_name).first()


async def find_user_by_email(user_email: str, db: Session) -> Type[User] | None:
    return db.query(User).filter(User.email == user_email).first()


async def find_next_7_days_birthdays(db: Session) -> list[Type[User]] | None:
    today_date = date.today() + timedelta(days=1)
    seventh_day_date = today_date + timedelta(days=7)
    return (
        db.query(User)
        .filter(
            (
                func.date_part("month", User.day_of_born)
                == today_date.month | seventh_day_date.month
            )
            & (func.date_part("day", User.day_of_born) >= today_date.day)
            & (func.date_part("day", User.day_of_born) <= seventh_day_date.day)
        )
        .all()
    )


# -------------------Авторизаційні функції-----------------
async def create_user(body: UserModel, db: Session) -> User:
    contacts = db.query(Contact).filter(Contact.id.in_(body.contacts)).all()
    new_user = User(
        name=body.name,
        last_name=body.last_name,
        day_of_born=body.day_of_born,
        email=body.email,
        description=body.description,
        password=body.password,
        contacts=contacts,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()


# ---------Верифікація-----------
async def confirmed_email(email: str, db: Session) -> None:
    """Мета цієї функції – встановити атрибут confirmed користувача в значення True у базі даних."""
    user = await find_user_by_email(email, db)
    user.confirmed = True
    db.commit()
