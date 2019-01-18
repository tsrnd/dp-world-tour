import inject
from abc import ABCMeta, abstractmethod
from minio import Minio
from django.conf import settings

class StorageInterface(metaclass=ABCMeta):
    @abstractmethod
    def put_object(self, bucket_name, object_name, data, length, content_type='application/octet-stream', metadata=None):
        pass
    
    @abstractmethod
    def exists_object(self, bucket_name, object_name):
        pass
    
    @abstractmethod
    def get_object(self, bucket_name, object_name):
        pass
    
    @abstractmethod
    def delete_object(self, bucket_name, object_name):
        pass


class Storage(StorageInterface):
    minioInfo = settings.STORAGE
    if minioInfo['need_to_init']:
        minioClient = Minio(minioInfo['endpoint'],
                    minioInfo['access_key'],
                    minioInfo['secret_key'],
                    False,
                    minioInfo['region'])
    
    def put_object(self, bucket_name, object_name, data, length, content_type='application/octet-stream', metadata=None):
        return self.minioClient.put_object(bucket_name, object_name, data, length, content_type, metadata)
    
    def exists_object(self, bucket_name, object_name):
        pass
    
    def get_object(self, bucket_name, object_name):
        pass
    
    def delete_object(self, bucket_name, object_name):
        pass

def storage_provider_config(binder: inject.Binder):
    binder.bind(Storage, Storage())
