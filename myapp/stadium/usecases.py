import inject
from abc import ABCMeta, abstractmethod
from myapp.stadium.repositories import *


class UsecaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_list_stadium(self):
        pass


class StadiumUsecase(UsecaseInterface):
    repo = inject.attr(RepositoryInterface)

    def get_list_stadium(self, r):
        return self.repo.get_list_stadium(r)
