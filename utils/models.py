from django.db import models


class BaseModel(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )

    created_at = models.DatTimeField(
        auto_add_now=True,
        editable=False,
        help_text="The date/time this object was created."
    )

    modified_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        help_text="The date/time this object was last modified."
    )

    class Meta:
        abstract = True
