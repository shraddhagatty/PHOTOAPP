#
# awsutil.py
#
# Helper functions that interact with AWS S3.
#
# Original author:
#   Prof. Joe Hummel
#   Northwestern University
#

import boto3
import logging
import uuid
import pathlib


###################################################################
#
# download_file
#
# ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/download_file.html
#
def download_file(bucket, key):
  """
  Downloads a file from an S3 bucket

  Parameters
  ----------
  bucket : S3 bucket to download from, 
  key : object's name in bucket
  
  Returns
  -------
  filename of downloaded file or None upon an error
  """

  try:
    #
    # generate a unique filename:
    #
    filename = str(uuid.uuid4())
    extension = pathlib.Path(key).suffix
    filename += extension
    #
    # downoad:
    #
    bucket.download_file(key, filename)
    #
    return filename

  except Exception as e:
    logging.error("awss3.download_file() failed:")
    logging.error(e)
    return None


###################################################################
#
# upload_file
#
# ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/upload_file.html
#
def upload_file(local_filename, bucket, key):
  """
  Uploads a file to an S3 bucket, setting the content type to "image/jpeg" if
  a jpg file and the permissions to be publicly readable

  Parameters
  ----------
  local_filename : name of local file to upload, 
  bucket : S3 Bucket to upload to,
  key : object's name in the bucket after upload
  
  Returns
  -------
  key that was passed in or None upon an error
  """

  try:
    if key.endswith('jpg'):  # image file
      content_type = 'image/jpeg'
    else:  # default:
      content_type = 'application/octet-stream'

    bucket.upload_file(local_filename,
                       key,
                       ExtraArgs={
                         'ACL': 'public-read',
                         'ContentType': content_type
                       })
    return key

  except Exception as e:
    logging.error("awss3.upload_file() failed:")
    logging.error(e)
    return None
