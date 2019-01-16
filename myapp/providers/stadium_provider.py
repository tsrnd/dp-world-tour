import inject
from myapp.stadium.repositories import *
from myapp.stadium.usecases import *


def myapp_providers_config(binder: inject.Binder):
    binder.bind(RepositoryInterface, StadiumRepository())
    binder.bind(UsecaseInterface, StadiumUsecase())
