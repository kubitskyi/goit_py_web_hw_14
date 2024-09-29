import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import ContactSchema, ContactBirthday
from src.repository.contacts import (
    get_contact,
    get_contacts,
    get_birthdays_week,
    create_contact,
    update_contact,
    search_contacts,
    remove_contact,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=0, db=self.session, user=self.user)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=0, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_get_birthdays_week(self):
        contacts = [Contact(id=1, first_name='A', last_name='B', birthday='2020-01-01')]
        contacts_birthday = [ContactBirthday(id=1, first_name='A', last_name='B', birthday='2020-01-01')]
        self.session.query().filter().all.return_value = contacts
        result = await get_birthdays_week(db=self.session, user=self.user)
        self.assertEqual(contacts_birthday, result)

    async def test_create_contact(self):
        body = ContactSchema(id=1, first_name='A', last_name='B', birthday='2020-01-01', email='test@test.com',
                             phone_number='123', additional_info='other')
        result = await create_contact(body=body, db=self.session, user=self.user)
        self.assertEqual(result.id, body.id)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.additional_info, body.additional_info)
        self.assertTrue(hasattr(result, 'id'))

    async def test_update_contact(self):
        body = Contact(id=1, first_name='A', last_name='B', birthday='2020-01-01', email='test@test.com',
                             phone_number='123', additional_info='other')
        self.session.query().filter().first.return_value = body
        result = await update_contact(body=body, contact_id=1, db=self.session, user=self.user)
        self.assertEqual(result, body)

    async def test_update_contact_not_found(self):
        body = Contact(id=1, first_name='A', last_name='B', birthday='2020-01-01', email='test@test.com',
                             phone_number='123', additional_info='other')
        self.session.query().filter().first.return_value = None
        result = await update_contact(body=body, contact_id=1, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_search_contacts(self):
        body = [Contact(), Contact()]
        self.session.query().filter().all.return_value = body
        result = await search_contacts(query="1", db=self.session, user=self.user)
        self.assertEqual(result, body)

    async def test_remove_contact(self):
        body = Contact()
        self.session.query().filter().first.return_value = body
        result = await remove_contact(contact_id='1', db=self.session, user=self.user)
        self.assertEqual(result, body)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id='1', db=self.session, user=self.user)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()