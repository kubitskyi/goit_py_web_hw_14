from datetime import date, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Contact, User
from src.schemas import ContactSchema, ContactBirthday


async def create_contact(body: ContactSchema, db: Session, user: User):
    """
    Create contact

    :param body: Contact body.
    :type body: ContactSchema
    :param db: Database session.
    :type db: Session
    :param user: Current user.
    :type user: User
    :return: Created contact.
    :rtype: Contact
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(limit: int, offset: int, db: Session, user: User):
    """
    Return all user's contacts

    :param limit: The maximum number of notes to return.
    :type limit: int
    :param offset: Offset.
    :type offset: int
    :param db: Database session.
    :type db: Session
    :param user: Current user.
    :type user: User
    :return: Contacts.
    :rtype: List[Contact]
    """
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id)).limit(limit).offset(offset).all()
    return contacts


async def get_contact(contact_id: int, db: Session, user: User):
    """
    Get contact by ID

    :param contact_id: Contact's ID.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param user: Current user.
    :type user: User
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def update_contact(body: ContactSchema, contact_id: int, db: Session, user: User):
    """
    Update contact by ID

    :param body: Contact body.
    :type body: ContactSchema
    :param contact_id: Contact's ID.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param user: Current user.
    :type user: User
    :return: Update contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User):
    """
    Remove contact by ID

    :param contact_id: Contact's ID.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param user: Current user.
    :type user: User
    :return: Contact.
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session, user: User):
    """
    Search contact by some text

    :param query: String for search
    :type query: str
    :param db: Database session.
    :type db: Session
    :param user: Current user.
    :type user: User
    :return: List founded contacts.
    :rtype: List[Contact]
    """
    contacts = db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            (
                (Contact.first_name.contains(query)) |
                (Contact.last_name.contains(query)) |
                (Contact.email.contains(query))
            )
        )
    ).all()
    return contacts


async def get_birthdays_week(db: Session, user: User):
    """
    List of contacts who have a birthday in the next 7 days.

    :param db: Database session.
    :type db: Session
    :param user: Current user.
    :type user: User
    :return: List founded contacts.
    :rtype: List[Contact]
    """
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (Contact.user_id == user.id) &
        (extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day)
        & (extract('month', Contact.birthday) == end_date.month) & (extract('day', Contact.birthday) <= end_date.day)
    ).all()
    return [
        ContactBirthday(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            birthday=contact.birthday
        )
        for contact in contacts
    ]