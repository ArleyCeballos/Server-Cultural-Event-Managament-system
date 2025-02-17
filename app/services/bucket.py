import asyncio
import base64

from google.cloud.storage import Client

from app.config import settings


class ServiceBucket:
    # storage_client = Client()

    @staticmethod
    async def upload_blob_async(destination_blob_name, contents, content_type):
        try:
            bucket = ServiceBucket.storage_client.bucket(settings.BUCKET_NAME)
            blob = bucket.blob(destination_blob_name)

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, blob.upload_from_string, contents, content_type
            )
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_all_files_in_folder(folder_path):
        try:
            bucket = ServiceBucket.storage_client.bucket(settings.BUCKET_NAME)
            blobs = bucket.list_blobs(prefix=folder_path)
            return [blobs.name for blobs in blobs]
        except Exception as e:
            print(e)
            return None

    @staticmethod
    async def get_file_by_route(blob_name):
        try:
            bucket = ServiceBucket.storage_client.bucket(settings.BUCKET_NAME)
            blob = bucket.blob(blob_name)

            loop = asyncio.get_event_loop()
            bytes_data = await loop.run_in_executor(None, blob.download_as_bytes)
            content_type = blob.content_type
            return {
                "file_bytes": bytes_data,
                "content_type": content_type,
                "file_name": blob_name,
            }
        except Exception as e:
            print(e)
            return {"file_bytes": None, "content_type": None, "file_name": None}

    @staticmethod
    async def delete_file_by_route(blob_name):
        try:
            bucket = ServiceBucket.storage_client.bucket(settings.BUCKET_NAME)
            blob = bucket.blob(blob_name)

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, blob.delete)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def download_blobs_in_folder(folder_path):
        try:
            bucket = ServiceBucket.storage_client.bucket(settings.BUCKET_NAME)
            blobs = list(bucket.list_blobs(prefix=folder_path))
            files_data = []

            loop = asyncio.get_event_loop()

            for blob in blobs:
                bytes_data = await loop.run_in_executor(None, blob.download_as_bytes)
                base64_encoded_data = base64.b64encode(bytes_data).decode()
                files_data.append(
                    {
                        "file_base64": base64_encoded_data,
                        "content_type": blob.content_type,
                        "file_name": blob.name.split("/")[-1],
                    }
                )

            return files_data
        except Exception as e:
            print(e)
            return []


service_bucket = ServiceBucket()
