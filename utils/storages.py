from django.conf import settings
from storages.backends.s3 import S3Storage


class S3StoragePublic(S3Storage):
    location = 'public'
    default_acl = 'public-read'
    querystring_auth = False
    object_parameters = {
        'CacheControl': 'max-age=86400',
    }
    file_overwrite = False
    custom_domain = f"{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"


class S3StoragePrivate(S3Storage):
    location = 'private'
    default_acl = 'private'
    querystring_auth = True
    object_parameters = {
        'CacheControl': 'max-age=86400',
        'ServerSideEncryption': 'AES256',
    }
    file_overwrite = False
    custom_domain = None
