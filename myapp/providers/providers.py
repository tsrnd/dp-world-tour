import inject
from myapp.providers.stadium_provider import stadium_providers_config
from myapp.providers.user_provider import user_providers_config


def myapp_providers_config(binder: inject.Binder):
    binder.install(stadium_providers_config)
    binder.install(user_providers_config)
