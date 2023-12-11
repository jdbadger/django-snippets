from django.contrib.auth.hashers import identify_hasher, make_password
from django.db import models


class HashedCharField(models.CharField):

    """
    Don't store plain text secrets! This implementation of CharField hashes the provided value
    before saving. Heavily based upon django-oauth-toolkit's oauth2_provider.models.ClientSecretField.
    See: https://github.com/jazzband/django-oauth-toolkit/blob/master/oauth2_provider/models.py
    """

    def pre_save(self, model_instance, add):
        # model_instance: the instance this field belongs to
        # add: whether the instance is being saved to the database for the first time
        secret = getattr(model_instance, self.attname)
        try:
            # is the value hashed?
            identify_hasher(secret)
        except ValueError:
            # the value is not hashed...
            # hash the value...
            hashed_secret = make_password(secret)
            # set it to attribute on the model instance...
            setattr(model_instance, self.attrname, hashed_secret)
            # return the value of the attribute
            return hashed_secret
        # default preprocessing before saving
        return super().pre_save(model_instance, add)
