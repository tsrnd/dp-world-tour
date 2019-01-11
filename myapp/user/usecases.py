import inject
from abc import ABCMeta, abstractmethod
from myapp.user.repositories import *


class UsecaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_user(self, user_name, email, password):
        pass


class UserUsecase(UsecaseInterface):
    repo = inject.attr(UserRepository)

    def create_user(self, user_name, email, password):
        # check user ton tai
        # self.repo.get_user()
        # dang ky user vafo database
        return self.repo.create_user(user_name, email, password)
