import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_user_by_email(self):
        body = User()
        self.session.query().filter().first.return_value = body
        result = await get_user_by_email(email='@', db=self.session)
        self.assertEqual(result, body)

    async def test_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email='@', db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username='Name111', email='@', password='123456', confirmed=True)
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)


if __name__ == '__main__':
    unittest.main()