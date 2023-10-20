import uuid
import mimetypes, os, asyncio, json, hashlib
from io import BytesIO
from logging import getLogger
from swibots.utils.types import (
    IOClient,
    ReadCallbackStream,
    UploadProgress,
    UploadProgressCallback,
)
from threading import Thread
from swibots.config import APP_CONFIG
from httpx import AsyncClient
from concurrent.futures import ThreadPoolExecutor

# from b2sdk.utils import hex_sha1_of_file, hex_sha1_of_bytes, hex_sha1_of_stream
from b2sdk.v2 import B2Api
from logging import getLogger

logger = getLogger(__name__)
api_url = "https://api004.backblazeb2.com"


backblaze = B2Api(max_upload_workers=1000)
backblaze
bucket = None
if (account_id := APP_CONFIG["BACKBLAZE"].get("ACCOUNT_ID")) and (
    application_key := APP_CONFIG["BACKBLAZE"].get("APPLICATION_KEY")
):
    backblaze.authorize_account("production", account_id, application_key)
if (
    bucket_id := APP_CONFIG["BACKBLAZE"].get("BUCKET_ID")
) and backblaze.get_account_id():
    bucket = backblaze.get_bucket_by_id(bucket_id)

minimum_size = backblaze.account_info.get_absolute_minimum_part_size()

headers = {}
headers["Authorization"] = (
    "Basic "
    + "MDA0YjRjZjkwNDFiOWYxMDAwMDAwMDAwNjpLMDA0Zi9BN1FtSkppUW1NWnN5VzN5R3ZoVmNJd2Q0"
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
        min_file_size: int = 100 * (1024**2),
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
        if part_size < minimum_size:
            logger.error(f"part_size is smaller than minimum part size: {minimum_size}")
            part_size = minimum_size
        self._part_size = part_size
        self.loop = asyncio.get_event_loop()
        self._workers = workers
        self._task_count = task_count
        # self.__exec_ = ThreadPoolExecutor(12)
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
            path=self.path,
            callback=self.callback,
            callback_args=self.upload_args
            
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
                "bucketId": "6b741c0f098034a18b190f11",
                "fileInfo": file_info
                #            "fileInfo": {"large_file_sha1": file_sha1},
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

#                    logger.info("get part url")
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
                    # (respp.json(), token)
#                    logger.info("calling upload")
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
#                    logger.info(respp.json())
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

    """
    async def upload_large_file(self, content_type, file_name, file_info={}):
        loop = asyncio.get_event_loop()
        large_file = await loop.run_in_executor(None, backblaze.self._client.start_large_file(
            bucket.get_id(), file_name, content_type, file_info
        ))
        file_parts = []
        file_path = self.path

        with open(file_path, "rb") as file:
            while True:
                piece = file.read(self._part_size)
                if not piece:
                    break
                file_parts.append(piece)

        part_futures = []
        #        with self._exec as executor:
        part_number = 1
        part_sha1_array = []
#        loop = asyncio.get_event_loop()

        def upload_file_part(self, part_number, large_file_id, part_data):
            # Get the upload URL for a part of a large file
            # upload_url, upload_auth_token = backblaze.self._client.get_upload_part_url(large_file_id)

            # Upload the part
            if not self._progress:
                self._progress = UploadProgress(
                    self.path, self.callback, self.upload_args, IOClient()
            )
            bytes_io = BytesIO(part_data)
            stream = ReadCallbackStream(bytes_io, self._progress.update)

            part_sha1 = hex_sha1_of_stream(bytes_io, len(part_data))
#            loop = asyncio.get_event_loop()
            response = backblaze.self._client.upload_part(
                large_file_id,
                part_number,
                len(part_data),
                part_sha1,
                stream,
            )
            print(response)
            part_sha1_array.append(response["contentSha1"])
    #        await self._progress.bytes_readed(response["contentLength"])
            return response
        
        while file_parts:
            parts=  file_parts[:self._workers]
            file_parts = file_parts[self._workers:]
            part_futures = []
            for part_data in parts:
                future = self._exec.submit(lambda: upload_file_part(self, part_number, large_file["fileId"], part_data))
#                th.start()
#                ts.append(th)
                part_futures.append(future)
                part_number += 1
#            for t in ts:
 #               t.join()
            
#        await asyncio.wait(part_futures)
    #    part_sha1_array = [future.result()["contentSha1"] for future in part_futures]

        response = await loop.run_in_executor(None, lambda: backblaze.self._client.finish_large_file(
            large_file["fileId"], part_sha1_array
        ))
        return response
    """

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
            self._progress = UploadProgress(
                self.path,
                callback=self.callback,
                callback_args=self.upload_args,
                loop=self.loop,
            )



            loop = asyncio.get_event_loop()
            file_response = await loop.run_in_executor(None, lambda: bucket.upload_local_file(
                    self.path,
                    file_name=file_name,
                    content_type=self.mime_type,
                    progress_listener=self._progress if self.callback else None,
                ).as_dict()
)
        url = backblaze.get_download_url_for_fileid(file_response["fileId"])

        return {
            "caption": self.caption,
            "description": self.description,
            "mimeType": self.mime_type,
            "fileSize": file_response.get("size", os.path.getsize(self.path)),
            "fileName": file_response["fileName"],
            "downloadUrl": url,
            "thumbnailUrl": (
                self.file_to_url(self.thumbnail) if self.thumbnail != self.path else url
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
            else None
            #            "thumbnail":self.thumbnail
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

    def file_to_url(self, path, mime_type: str = None, *args, **kwargs) -> str:
        if path:
            file = bucket.upload_local_file(
                path, path, content_type=mime_type, *args, **kwargs
            ).as_dict()
            return backblaze.get_download_url_for_fileid(file["fileId"])

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
