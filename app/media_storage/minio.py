from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class MinioStorage:
    def __init__(self, bucket=settings.MINIO_BUCKET, secure: bool = False):
        self._hostname = settings.MINIO_HOSTNAME
        self._access_key = settings.MINIO_ACCESS_KEY
        self._secret_key = settings.MINIO_SECRET_KEY
        self._bucket = bucket
        self._secure = secure

    @property
    def _minio_client(self):
        return Minio(
            endpoint=self._hostname,
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=self._secure
        )

    def get_uploaded_url(self, file: UploadFile) -> str:
        return f"localhost:9000/api/v1/buckets/{self._bucket}/objects/download?preview=true&prefix={file.filename}"

    def upload_image(self, file: UploadFile):
        try:
            self._minio_client.put_object(
                bucket_name=self._bucket,
                object_name=file.filename,
                data=file.file,
                content_type=file.content_type,
                length=-1,
                part_size=100 * 1024 * 1024,
            )
            return self.get_uploaded_url(file)
        except S3Error as err:
            ic(err)

    def delete_image(self, file_name: str):
        try:
            self._minio_client.remove_object(
                bucket_name=self._bucket,
                object_name=file_name
            )
        except S3Error as err:
            ic(err)
