import csv
import io
from typing import IO
import uuid
import zipfile

from django.db import models
from django.http import (
    FileResponse,
    HttpResponse,
    StreamingHttpResponse
)


class CSVMixin(models.Model):

    """
    Use this mixin to provide CSV write functionality to your model.
    """

    class Meta:
        abstract = True

    def get_csv_row() -> list:
        """
        rtype: list
        """
        raise NotImplementedError("This method must be overridden.")

    @classmethod
    def get_csv_header() -> list:
        """
        rtype: list
        """
        raise NotImplementedError("This method must be overridden.")

    @classmethod
    def stream_csv_response(cls, filename: str, queryset: QuerySet) -> StreamingHttpResponse:
        
        class PseudoBuffer:

            def write(self, value):
                return value

        pseudo_buffer = PseudoBuffer()
        writer = csv.writer(pseudo_buffer)
        content_type = 'text.csv'
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        return StreamingHttpResponse(
            (
                writer.writerow(cls.get_csv_header()) if i == 0 else writer.writerow(obj.get_csv_row())
                for i, obj in enumerate(queryset.iterator())
            )
            content_type=content_type,
            headers=headers
        )

    @classmethod
    def write_csv_response(cls, filename: str, queryset: models.QuerySet) -> HttpResponse:
        content_type = 'text/csv'
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        response = HttpResponse(content_type=content_type, headers=headers)
        writer = csv.writer(response)
        writer.writerow(cls.get_csv_header())
        for obj in queryset:
            writer.writerow(obj.get_csv_row())
        return response


class ZipMixin(models.Model):

    """
    Use this mixin to provide zipfile write functionality to your model.
    """

    class Meta:
        abstract = True

    def get_file_for_zip() -> tuple(IO, str):
        raise NotImplementedError("This method must be overridden")

    @classmethod
    def get_zipfile_name() -> str:
        raise NotImplementedError("This method must be overridden")

    @classmethod
    def write_zip_response(cls, queryset: models.QuerySet, **kwargs) -> FileResponse:
        compression = kwargs.get('compression', zipfile.ZIP_DEFLATED)
        compress_level = kwargs.get('compress_level', 9)
        
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', compression) as zf:
            for obj in queryset:
                file, filename = obj.get_file_for_zip()
                if file and filename:
                    zf.writestr(filename, file, compresslevel)
        buffer.seek(0)
        
        filename = cls.get_zipfile_name()
        return FileResponse(buffer, filename=filename, as_attachment=True)
