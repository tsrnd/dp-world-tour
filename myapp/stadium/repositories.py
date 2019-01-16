import inject
from abc import ABCMeta, abstractmethod
from myapp.models.stadiums import Stadium



class RepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_list_stadium(self):
        pass


class StadiumRepository(RepositoryInterface):
    def get_list_stadium(self):
        stadium_list = Stadium.objects.all()
        return stadium_list
