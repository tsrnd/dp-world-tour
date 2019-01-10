import inject
from abc import ABCMeta, abstractmethod


class RepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, user_name):
        pass
    
    @abstractmethod
    def create_user(self, user_name, email, password):
        pass


class UserRepository(RepositoryInterface):
    
    def get_user(self, user_name):
        pass

    def create_user(self, user_name, email, password):
        pass

