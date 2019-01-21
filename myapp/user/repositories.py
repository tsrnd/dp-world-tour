import inject
from abc import ABCMeta, abstractmethod
# from django.contrib.auth.models import User

class RepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_user(self, user_name):
        pass

    # def get_user(self, user_name, password):
    #     pass
    
    @abstractmethod
    def create_user(self, user_name, email, password):
        pass


class UserRepository(RepositoryInterface):
    
    def get_user(self, user_name):
        pass

    # def get_user(self, user_name,password):
    #     user = User.objects.filter(username = user_name, password = password)
    #     if len(user) == 1:
    #         return user[0]
    #     return None


    def create_user(self, user_name, email, password):
        pass

