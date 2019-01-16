import inject

from django.test import TestCase
from django.contrib.auth.models import User
from myapp.user.repositories import UserRepository
from shared.test import CommonException

class RepositoryMock():
    def __init__(self, user, get_exception, create_exception):
        self.user = user
        self.get_exception = get_exception
        self.create_exception = create_exception

    def get_user(self, user_name):
        if self.get_exception is not None:
            raise CommonException(self.get_exception)
        return self.user

    def create_user(self, user_name, email, password):
        if self.create_exception is not None:
            raise CommonException(self.create_exception)
        return self.user

class UserRepositoryTestCaseSuccess(TestCase):
    user = User(
        username='test',
        email='test@test.com',
        password='abcxyz',
    )

    def test_create_user_success(self):
        userNew = UserRepository().create_user("test", "test@test.com", "abcxyz")
        self.assertEqual(self.user, userNew)
