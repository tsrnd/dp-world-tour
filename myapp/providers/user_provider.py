import inject
from myapp.user.repositories import *
from myapp.user.usecases import *


def myapp_providers_config(binder: inject.Binder):
    binder.bind(RepositoryInterface, UserRepository())
    binder.bind(UsecaseInterface, UserUsecase())
