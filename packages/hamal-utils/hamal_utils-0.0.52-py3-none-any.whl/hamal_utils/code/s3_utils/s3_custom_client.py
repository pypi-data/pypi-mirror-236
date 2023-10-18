import logging
import sys

import numpy as np

from hamal_utils.code.common import MONITOR_TAG_TMPL, EXTENSIONS, FROM_PERCENT, TO_PERCENT, BUCKET_FILES_COUNT
from hamal_utils.code.s3_utils.session import aws_session
from hamal_utils.code.utils.hash_util import hash_string


class CustomS3Client:
    def __init__(self):
        self._base_s3_client = aws_session.client('s3')

    def __getattr__(self, attr):
        if hasattr(self._base_s3_client, attr):
            return getattr(self._base_s3_client, attr)

        return super().__getattribute__(attr)

    def _get_log_tag(self, from_percent, to_percent):
        return MONITOR_TAG_TMPL.format(name=hash_string(sys.argv[0]), from_percent=from_percent, to_percent=to_percent)

    def _has_complete_tag(self, bucket, key):
        tags_response = self.get_object_tagging(bucket, key)

        if 'TagSet' not in tags_response:
            return False

        object_tags = tags_response['TagSet']
        log_tag_key = self._get_log_tag(FROM_PERCENT, TO_PERCENT)

        for tag in object_tags:
            if log_tag_key == tag['Key']:
                return True

        return False

    def _tag_file_as_complete(self, bucket, key):
        log_tag_key = self._get_log_tag(FROM_PERCENT, TO_PERCENT)
        tagging = {'TagSet': [{'Key': log_tag_key, 'Value': 'complete'}]}
        self.put_object_tagging(Bucket=bucket, Key=key, Tagging=tagging)

    def _validate_extensions(self, key):
        return not EXTENSIONS or any(key.lower().endswith(ext.lower()) for ext in EXTENSIONS)

    def list_objects_v2_generator(
            self,
            bucket,
            delimiter=None,
            encoding_type=None,
            max_keys=None,
            prefix=None,
            fetch_owner=None,
            start_after=None,
            request_payer=None,
            expected_bucket_owner=None,
            optional_object_attributes=None,
            enable_log_tag=True,
            ignore_log_tag=True):

        has_counter = FROM_PERCENT != 0 or TO_PERCENT != 1
        counter = 0
        count = self.get_bucket_count(bucket, prefix) if has_counter else -1
        from_counter = np.floor(FROM_PERCENT * count).astype(int)
        to_counter = np.floor(TO_PERCENT * count).astype(int) - 1
        limit = to_counter - from_counter
        logging.debug(f"running from {from_counter} to {to_counter}")

        for file in self._list_objects_v2_generator(
                bucket, delimiter, encoding_type, max_keys, prefix, fetch_owner, start_after, request_payer,
                expected_bucket_owner, optional_object_attributes):

            if has_counter and counter > limit:
                break

            counter += 1

            key = file["Key"]

            if not self._validate_extensions(key):
                continue

            if not ignore_log_tag and self._has_complete_tag(bucket, key):
                continue

            logging.debug(f"Running on item {counter}: {key}")
            yield file

            if enable_log_tag:
                self._tag_file_as_complete(bucket, key)

    def _list_objects_v2_generator(
            self, bucket,
            delimiter=None,
            encoding_type=None,
            max_keys=None,
            prefix=None,
            fetch_owner=None,
            start_after=None,
            request_payer=None,
            expected_bucket_owner=None,
            optional_object_attributes=None):

        args = {
            'Bucket': bucket,
            'Delimiter': delimiter,
            'EncodingType': encoding_type,
            'MaxKeys': max_keys,
            'Prefix': prefix,
            'FetchOwner': fetch_owner,
            'StartAfter': start_after,
            'RequestPayer': request_payer,
            'ExpectedBucketOwner': expected_bucket_owner,
            'OptionalObjectAttributes': optional_object_attributes
        }

        s3_args = {key: value for key, value in args.items() if value}

        while True:
            response = self.list_objects_v2(**s3_args)

            if 'Contents' not in response:
                break

            for file in response['Contents']:
                yield file

            if 'NextContinuationToken' not in response:
                break

            s3_args['ContinuationToken'] = response['NextContinuationToken']

    def get_bucket_count(self, bucket, prefix=None):
        if BUCKET_FILES_COUNT > -1:
            return BUCKET_FILES_COUNT

        count = 0
        paginator = self.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix or '')
        for page in pages:
            if 'Contents' not in page:
                break
            count += len(page['Contents'])
        return count
