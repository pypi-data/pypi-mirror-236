import uuid, base64
import mimetypes, os, asyncio, json, hashlib
from io import BytesIO
from logging import getLogger
from swibots.utils.types import (
    IOClient,
    ReadCallbackStream,
    UploadProgress,
    UploadProgressCallback,
)
from swibots.config import APP_CONFIG
from httpx import AsyncClient
from concurrent.futures import ThreadPoolExecutor

from logging import getLogger

logger = getLogger(__name__)
api_url = "https://api004.backblazeb2.com"


bucket = None
account_id = APP_CONFIG["BACKBLAZE"].get("ACCOUNT_ID")
application_key = APP_CONFIG["BACKBLAZE"].get("APPLICATION_KEY")

bucket_id = APP_CONFIG["BACKBLAZE"].get("BUCKET_ID")

headers = {}
headers["Authorization"] = (
    "Basic "
    + base64.b64encode(f'{account_id}:{application_key}'.encode()).decode()
)
headers["accept"] = "application/json"


class MediaUploadRequest:
    def __init__(
        self,
        path: str | BytesIO,
        file_name: str = None,
        mime_type: str = None,
        caption: str = None,
        description: str = None,
        block: bool = True,
        callback: UploadProgressCallback = None,
        thumbnail: str = None,
        upload_args: tuple = (),
        reduce_thumbnail: bool = True,
        part_size: int = 1 * 1024 * 1024,
        loop=None,
        workers: int = int(os.getenv("UPLOAD_THREADS", 30)),
        min_file_size: int = 10 * (1024**2),
        task_count: int = 10,
    ):
        self.path = path
        self.file_name = file_name
        self.mime_type = mime_type
        self.caption = caption
        self.description = description
        self.block = block
        self.thumbnail = thumbnail
        self.callback = callback
        self.upload_args = upload_args
        self._handle_thumb = reduce_thumbnail
        self._part_size = part_size
        self.loop = asyncio.get_event_loop()
        self._workers = workers
        self._task_count = task_count
        self._exec = ThreadPoolExecutor(self._workers)
        self._progress: UploadProgress = None
        self._min_file = min_file_size
        self._client = AsyncClient(verify=False, timeout=None)
        self.__token = None

    async def getAccountInfo(self):
        response = await self._client.get(
            "https://api.backblazeb2.com/b2api/v2/b2_authorize_account", headers=headers
        )
        data = response.json()
        if token := data.get("authorizationToken"):
            self.__token = token
        return data

    async def upload_large_file(self, content_type, file_name, file_info=None):
        if not self.__token:
            info = await self.getAccountInfo()

        client = IOClient()
        progress = UploadProgress(
            path=self.path, callback=self.callback, callback_args=self.upload_args,
            client=client
        )
        with open(self.path, "rb") as file:
            head = {
                "Content-Type": content_type,
                "X-Bz-File-Name": file_name,
                "Authorization": self.__token,
            }
            data = {
                "fileName": file_name,
                "contentType": content_type,
                "bucketId": bucket.get_id(),
                "fileInfo": file_info,
            }
            partHash = {}
            logger.info("start large file")
            respp = await self._client.post(
                "https://api004.backblazeb2.com/b2api/v2/b2_start_large_file",
                headers=head,
                data=json.dumps(data),
            )
            if respp.status_code != 200:
                logger.error("on large file")
                logger.error(respp.json())

            logger.info(respp.json())
            #       token= respp.json()["authorizationToken"]
            fileId = respp.json()["fileId"]
            part_number = 1
            tasks = []
            while True:
                chunk = file.read(self._part_size)
                if not chunk:
                    break

                async def uploadFile(token, part_number, chunk):
                    sha1_checksum = hashlib.sha1(chunk).hexdigest()

                    respp = await self._client.post(
                        f"{api_url}/b2api/v2/b2_get_upload_part_url",
                        json={"fileId": fileId},
                        headers={"Authorization": token},
                    )
                    if respp.status_code != 200:
                        logger.error("on Part url")
                        logger.error(respp.json())
                    token = respp.json()["authorizationToken"]
                    upload_part_url = respp.json()["uploadUrl"]
                    respp = await self._client.post(
                        upload_part_url,
                        data=chunk,
                        headers={
                            "Authorization": token,
                            "X-Bz-Part-Number": str(part_number),
                            "X-Bz-Content-Sha1": sha1_checksum,
                        },
                    )
                    if respp.status_code != 200:
                        logger.error("onUpload")
                        logger.error(respp.json())
                    hash = respp.json()["contentSha1"]
                    partHash[hash] = respp.json()["partNumber"]
                    await progress.bytes_readed(respp.json()["contentLength"])

                tsk = asyncio.create_task(
                    uploadFile(self.__token, part_number, chunk)
                )  # respp
                tasks.append(tsk)
                if len(tasks) == self._task_count:
                    await asyncio.gather(*tasks)
                    tasks.clear()

                part_number += 1
        if tasks:
            await asyncio.gather(*tasks)
        hashes = list(map(lambda x: x[0], sorted(partHash.items(), key=lambda x: x[1])))

        response = await self._client.post(
            f"{api_url}/b2api/v2/b2_finish_large_file",
            json={
                "fileId": fileId,
                "partSha1Array": hashes,
            },
            headers={"Authorization": self.__token},
        )
        if response.status_code != 200:
            logger.error(response.json())

        return response.json()
    
    async def file_to_response(self, path, mime_type = None, file_name=None):
        
            if not self.__token:
                await self.getAccountInfo()
            head = {
                "Content-Type": "application/json",
                "Authorization": self.__token,
            }
            rsp = await self._client.get(
                f"https://api004.backblazeb2.com/b2api/v2/b2_get_upload_url?bucketId={bucket_id}",
                headers=head,
            )

            token = rsp.json()["authorizationToken"]
            with open(path, "rb") as f:
                content = f.read()
                file_sha1 = hashlib.sha1(content).hexdigest()
                rsp = await self._client.post(
                    rsp.json()["uploadUrl"],
                    headers={
                        "Authorization": token,
                        "X-Bz-File-Name": file_name,
                        "Content-Type": mime_type,
                        "X-Bz-Content-Sha1": file_sha1,
                    },
                    data=content,
                )
                file_response = rsp.json()
                return file_response
                
    async def get_media(self):
        if not self.mime_type:
            self.mime_type = (
                mimetypes.guess_type(self.file_name or self.path)[0]
                or "application/octet-stream"
            )
        _, ext = os.path.splitext(self.path)
        size = os.path.getsize(self.path)
        file_name = f"{uuid.uuid1()}{ext}"
        if size > self._min_file:
            file_response = await self.upload_large_file(self.mime_type, file_name)
        else:
            file_response = await self.file_to_response(self.path, self.mime_type, file_name)
    
        url = f"https://f004.backblazeb2.com/b2api/v2/b2_download_file_by_id?fileId={file_response['fileId']}"
    
        return {
            "caption": self.caption,
            "description": self.description,
            "mimeType": self.mime_type,
            "fileSize": file_response.get("size", os.path.getsize(self.path)),
            "fileName": file_response["fileName"],
            "downloadUrl": url,
            "thumbnailUrl": (
                await self.file_to_url(self.thumbnail) if self.thumbnail != self.path else url
            )
            or url,
            "sourceUri": file_response["fileId"],
            "checksum": file_response["contentSha1"],
        }

    def data_to_request(self):
        return {
            "uploadMediaRequest.caption": self.caption,
            "uploadMediaRequest.description": self.description,
        }

    def data_to_params_request(self):
        return {
            "caption": self.caption,
            "description": self.description,
            "mimeType": self.get_mime_type(),
            "fileSize": os.path.getsize(self.path)
            if os.path.exists(self.path)
            else None,
        }

    def get_mime_type(self):
        path = self.path.name if isinstance(self.path, BytesIO) else self.path
        return (
            self.mime_type
            or mimetypes.guess_type(path)[0]
            or "application/octet-stream"
        )

    def generate_thumbnail(
        self, path, radius: int = 5, resize: bool = False, quality: int = 80
    ):
        if self._handle_thumb:
            try:
                from PIL import Image, ImageFilter

                img = Image.open(path)
                if resize:
                    img.thumbnail((img.width // 2, img.height // 2), Image.BILINEAR)
                img = img.filter(ImageFilter.GaussianBlur(radius))
                obj = BytesIO()
                obj.name = os.path.basename(path)
                img.save(obj, optimize=True, quality=quality)
                return obj
            except ImportError:
                logger.debug(
                    "Pillow is not installed, Install it to add blur filter to thumbnail!"
                )
        return open(path, "rb")

    async def file_to_url(self, path, mime_type: str = None, *args, **kwargs) -> str:
        if path:
            _, ext = os.path.splitext(path)
            file_name = f"{uuid.uuid1()}{ext}"

            file = await self.file_to_response(
                path, mime_type, file_name
            )
            return f"https://f004.backblazeb2.com/b2api/v2/b2_download_file_by_id?fileId={file['fileId']}"


    def file_to_request(self, url):
        d_progress = UploadProgress(
            current=0,
            readed=0,
            file_name=self.file_name,
            client=IOClient(),
            url=url,
            callback=self.callback,
            callback_args=self.upload_args,
        )
        reader = ReadCallbackStream(self.path, d_progress.update)
        d_progress._readable_file = reader
        path = self.path.name if isinstance(self.path, BytesIO) else self.path
        mime = self.get_mime_type()
        result = {"uploadMediaRequest.file": (self.file_name or path, reader, mime)}
        if self.thumbnail:
            if os.path.exists(self.thumbnail):
                thumb = self.generate_thumbnail(self.thumbnail)
                result["uploadMediaRequest.thumbnail"] = (
                    self.thumbnail,
                    thumb,
                    mimetypes.guess_type(self.thumbnail)[0],
                )
            else:
                logger.error(
                    f"provided thumbnail: {self.thumbnail} is not a valid path!"
                )
        return d_progress, result
