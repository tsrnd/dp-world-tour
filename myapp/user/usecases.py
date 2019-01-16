import inject
from abc import ABCMeta, abstractmethod
from myapp.user.repositories import *

class UsecaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def create_user(self, user_name, email, password):
        pass


class UserUsecase(UsecaseInterface):
    repo = inject.attr(RepositoryInterface)

    def create_user(self, username, email, password):
        user = self.repo.get_user(username)
        if user is not None:
            return None
        return self.repo.create_user(username = username, email = email, password = password)
