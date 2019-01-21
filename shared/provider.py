import inject

from shared.base_handler import bh_config
from shared.storage import storage_provider_config

def shared_provider_config(binder: inject.Binder):
    binder.install(bh_config)
    binder.install(storage_provider_config)
