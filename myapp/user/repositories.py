import inject
from abc import ABCMeta, abstractmethod
from django.contrib.auth.models import User


class RepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, user_name):
        pass
    
    @abstractmethod
    def create_user(self, username, email, password):
        pass


class UserRepository(RepositoryInterface):
    
    def get_user(self, user_name):
        user = User.objects.filter(username = user_name)
        if len(user) == 0:
            return None
        return user

    def create_user(self, username, email, password):
        user = User.objects.create_user(pk= 12,username = username,password = password,email = email)
        user.save()
        return user

