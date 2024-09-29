from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create user.

    :param body: User body.
    :type body: UserModel
    :param db: Database session.
    :type db: Session
    :return: Created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update user token

    :param user: Current user.
    :type user: User
    :param token: User's token.
    :type token: str
    :param db: Database session.
    :type db: Session
    :return: Not return result.
    """
    user.refresh_token = token
    db.commit()
    
async def confirmed_email(email: str, db: Session) -> None:
    """
    Set user's e-mail confirmed.

    :param email: User's e-mail
    :type email: str
    :param db: Database session.
    :type db: Session
    :return: Not return result.
    """

    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    """
    Update user's avatar

    :param email: User's e-mail.
    :type email: str
    :param url: User avatar link.
    :type url: str
    :param db: Database session.
    :type db: Session
    :return: Updated user.
    :rtype: User

    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
