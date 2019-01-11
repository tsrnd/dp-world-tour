import inject

from django.test import TestCase
from django.contrib.auth.models import User
from myapp.user.repositories import *
from myapp.user.usecases import UserUsecase
from shared.test import CommonException


class RepositoryMock(RepositoryInterface):
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


def CreateUserSuccessTestCase(TestCase):
    user = User(
        username='test',
        email='test@test.com',
        password='abcxyz',
    )
    def setUp(self):
        inject.clear_and_configure(lambda binder: binder.bind(
            RepositoryInterface, RepositoryMock(user, None, None)
        ))

    def test_create_user_success(self):
        userNew = UserUsecase().create_user("test", "test@test.com", "abcxyz")
        self.assertEqual(user, userNew)

    def tearDown(self):
        inject.clear()

def CreateUserFailTestCase(TestCase):
    user = User(
        username='test',
        email='test@test.com',
        password='abcxyz',
    )
    def setUp(self):
        inject.clear_and_configure(lambda binder: binder.bind(
            RepositoryInterface, RepositoryMock(user, None, "can't create")
        ))

    def test_create_user_fail(self):
        with self.assertRaises(CommonException):
            UserUsecase().create_user('test', 'test@test.com', 'abcxyz')

    def tearDown(self):
        inject.clear()