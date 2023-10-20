import logging
import os.path
from datetime import datetime
from taichu_storage import StorageInterface
from obs import ObsClient, PutObjectHeader

from io import BytesIO


class StorageObs(StorageInterface):

    def __init__(self, cfgs=None):
        if cfgs is None:
            cfgs = {}

        self._bucket = cfgs.get('bucket')
        obs_ak = cfgs.get('ak')
        obs_sk = cfgs.get('sk')
        obs_server = cfgs.get('endpoint_url')

        self._client = ObsClient(
            access_key_id=obs_ak,
            secret_access_key=obs_sk,
            server=obs_server
        )
        resp = self._client.listBuckets()
        if resp.status >= 300:
            raise Exception(f'Failed to connect to OBS,errorCode:{resp.errorCode}, errorMessage: {resp.errorMessage}')
        resp = self._client.headBucket(bucketName=self._bucket)
        if resp.status == 404:
            raise Exception(f'Bucket {self._bucket} does not exist')
        print("Successfully connected to OBS!")

    def list_objects(self, key, delimiter='', skip_empty_file=True):
        max_num = 1000
        mark = None
        result = []
        while True:
            resp = self._client.listObjects(bucketName=self._bucket, prefix=key, marker=mark,
                                            max_keys=max_num, delimiter=delimiter)
            if resp.status < 300:
                folders = []
                for folder in resp.body.commonPrefixs:
                    folders.append({
                        'name': folder.Prefix,
                        'is_dir': True,
                        'size': 0,
                        'last_modified': None,
                    })
                result.extend(folders)
                objects = []
                for content in resp.body.contents:
                    if skip_empty_file and content.key.endswith('/'):
                        continue
                    objects.append({
                        'name': content.key,
                        'is_dir': False,
                        'size': content.size,
                        'last_modified': datetime.strptime(content.lastModified, "%Y/%m/%d %H:%M:%S").strftime(
                            "%Y-%m-%d %H:%M:%S"),
                    })
                result.extend(objects)
                if resp.body.is_truncated is True:
                    mark = resp.body.next_marker
                else:
                    break
            else:
                logging.error(f'list_objects error,error_code:{resp.status}, message:{resp.errorMessage}')
                break

        return result

    def get_object(self, key):
        response = self._client.getObject(self._bucket, key, loadStreamInMemory=True)
        if response.status < 300:
            return BytesIO(response.body.buffer)
        return BytesIO()

    def put_object(self, key, content):
        self._client.putContent(self._bucket, key, content=content)

    def upload_file(self, local_filename, key):
        headers = PutObjectHeader()
        headers.contentType = 'text/plain'
        self._client.putFile(self._bucket, key, local_filename, metadata={}, headers=headers)

    def upload_dir(self, local_dir, key):
        local_dir = local_dir.rstrip('/')
        key = key.rstrip('/')
        self.upload_file(local_dir, key)

    def download_file(self, key, local_filename):
        if local_filename.endswith('/'):
            os.makedirs(local_filename, exist_ok=True)
            local_filename = os.path.join(local_filename, key.split('/')[-1])

        resp = self._client.getObject(self._bucket, key, downloadPath=local_filename)
        if not resp.status < 300:
            logging.error(f"key:{key},local_filename:{local_filename}")
            logging.error(f'errorCode:{resp.errorCode}, errorMessage:{resp.errorMessage}')

    def download_dir(self, key, local_dir):
        if local_dir.endswith('/'):
            local_dir = local_dir[:-1]
        objects = self.list_objects(key, skip_empty_file=False)
        for o in objects:
            local_filename = os.path.join(local_dir, o['name'].replace(key, ''))
            if o['is_dir']:
                continue
            if o['name'].endswith('/'):
                os.makedirs(local_filename, exist_ok=True)
                continue

            self.download_file(o['name'], local_filename)

    def copy_object(self, source_key, dest_key):
        resp = self._client.copyObject(self._bucket, source_key, self._bucket, dest_key)
        if not resp.status < 300:
            logging.error(f'copy_object error,error_code:{resp.errorCode}, message:{resp.errorMessage}')

    def copy_dir(self, source_path, dest_path):
        if not dest_path.endswith('/'):
            dest_path = dest_path + '/'
        objects = self.list_objects(source_path)
        for o in objects:
            source_key = o['name']
            dest_key = source_key.replace(source_path, dest_path)
            self.copy_object(source_key, dest_key)

    def create_dir(self, key):
        if not key.endswith('/'):
            key = key + '/'
        self.put_object(None, key)

    def generate_signed_url(self, key, expiration=3600, use_external_host=True):
        rps = self._client.createSignedUrl("GET", self._bucket, key, expires=expiration)
        return rps.signedUrl

    def generate_upload_credentials(self, key, expiration=3600, use_external_host=True):
        content_type = 'text/plain'
        if key.endswith('txt'):
            content_type = 'text/plain;charset=utf-8'
        elif key.endswith('json'):
            content_type = 'application/json;charset=utf-8'
        response = self._client.createSignedUrl("PUT", self._bucket, key,
                                                expires=expiration, headers={'Content-Type': content_type})
        return response
