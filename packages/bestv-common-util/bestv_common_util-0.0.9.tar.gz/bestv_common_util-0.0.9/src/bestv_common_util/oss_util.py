import logging
import os
import oss2

from str_util import extract_bucket, extract_object_key


# def extract_path(filepath):
#     """
#     D:/mnt/data/private/model/20230607 => /mnt/data/private/model/20230607
#     oss://opg211-dev-ds-export/private/model/20230607 => /mnt/data/private/model/20230607
#     :param filepath:
#     :return:
#     """


class OSSUtil:
    ACCESS_KEY_ID = None
    ACCESS_KEY_SECRET = None
    ENDPOINT = None

    def __init__(self, access_key_id, access_key_secret, endpoint):
        self.ACCESS_KEY_ID = access_key_id
        self.ACCESS_KEY_SECRET = access_key_secret
        self.ENDPOINT = endpoint

    def upload_file(self, local_file, remote_file):
        bucket_name = extract_bucket(remote_file)
        object_key = extract_object_key(remote_file)
        if bucket_name:
            bucket = oss2.Bucket(oss2.Auth(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET), self.ENDPOINT, bucket_name)
            with open(local_file, "rb") as f:
                bucket.put_object(object_key, f)
                logging.info("file: %s 上传成功", object_key)
                return True
        else:
            logging.error("file: %s, format error, must be complete!", object_key)

    def upload_dir(self, local_dir, remote_dir, excludes=[]):
        bucket_name = extract_bucket(remote_dir)
        object_path = extract_object_key(remote_dir)
        bucket = oss2.Bucket(oss2.Auth(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET), self.ENDPOINT, bucket_name)
        if os.path.isdir(local_dir):
            for root, dir, files in os.walk(local_dir):
                for filename in files:
                    fullpath = os.path.join(root, filename)
                    object_key = object_path + (fullpath[len(local_dir):].replace('\\', '/'))
                    if not any(item and len(item) > 0 and item in fullpath for item in excludes):
                        with open(fullpath, "rb") as f:
                            bucket.put_object(object_key, f)
                            logging.info("file: %s 上传成功", object_key)
        logging.info("dir: %s 上传成功", local_dir)

    def download_file(self, remote_file, local_file, force=False):
        if not force and os.path.exists(local_file):
            logging.info("file: %s 本地已存在", local_file)
            return True
        bucket_name = extract_bucket(remote_file)
        object_key = extract_object_key(remote_file)
        bucket = oss2.Bucket(oss2.Auth(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET), self.ENDPOINT, bucket_name)
        object_stream = bucket.get_object(object_key)
        local_dir = os.path.dirname(local_file)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        with open(local_file, "wb") as f:
            f.write(object_stream.read())
            logging.info("file: %s 下载成功", local_file)
            return True


# 调用示例
# uploaded = upload_file('D:/mnt/2023-05-06-epg.csv', 'temp/remote_file.csv')
# downloaded = download_file('temp/remote_file.csv', 'D:/mnt/local_file_001.csv')
# upload_dir('D:/mnt/data/private/temp', 'temp/test_dir', [''])
# print(os.path.dirname('D:/mnt/data/private/test/remote_file.csv'))
# print(extract_dir("oss://opg211-dev-ds-export/private/model/20230607"))
# print(extract_dir("s3://opg211-dev-ds-export/private/model/20230607"))
