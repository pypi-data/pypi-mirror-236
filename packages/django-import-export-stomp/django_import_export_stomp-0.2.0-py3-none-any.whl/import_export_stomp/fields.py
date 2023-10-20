from django.conf import settings
from django.core.files.storage import get_storage_class
from django.db import models


class ImportExportFileField(models.FileField):
    def __init__(self, *args, **kwargs):
        # If the user has specified a custom storage backend, use it.
        if getattr(settings, "IMPORT_EXPORT_STOMP_STORAGE", None):
            storage_class = get_storage_class(settings.IMPORT_EXPORT_STOMP_STORAGE)
            kwargs["storage"] = storage_class()

        super().__init__(*args, **kwargs)
