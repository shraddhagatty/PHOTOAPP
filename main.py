#
# Main program for photoapp program using AWS S3 and RDS to
# implement a simple photo application for photo storage and
# viewing.
#
# Authors:
#   YOUR NAME
#   Prof. Joe Hummel (initial template)
#   Northwestern University
#   Fall 2023
#

import datatier  # MySQL database access
import awsutil  # helper functions for AWS
import boto3  # Amazon AWS

import uuid
import pathlib
import logging
import sys
import os

from configparser import ConfigParser

import matplotlib.pyplot as plt
import matplotlib.image as img


###################################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number
  
  Parameters
  ----------
  None
  
  Returns
  -------
  Command number entered by user (0, 1, 2, ...)
  """
  print()
  print(">> Enter a command:")
  print("   0 => end")
  print("   1 => stats")
  print("   2 => users")
  print("   3 => assets")
  print("   4 => download")
  print("   5 => download and display")
  print("   6 => upload")
  print("   7 => add user")

  cmd = int(input())
  return cmd


###################################################################
#
# stats
#
def stats(bucketname, bucket, endpoint, dbConn):
  """
  Prints out S3 and RDS info: bucket name, # of assets, RDS 
  endpoint, and # of users and assets in the database
  
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  
  Returns
  -------
  nothing
  """
  #
  # bucket info:
  #
  print("S3 bucket name:", bucketname)

  assets = bucket.objects.all()
  print("S3 assets:", len(list(assets)))

  #
  # MySQL info:
  #
  print("RDS MySQL endpoint:", endpoint)

  sql = """
  select count(*) from users;
  """
  row = datatier.retrieve_one_row(dbConn, sql)
  if row is None:
    print("Database operation failed...")
  elif row == ():
    print("Unexpected query failure...")
  else:
    print("# of users",row[0])

  sql = """
  select count(*) from assets;
  """
  row = datatier.retrieve_one_row(dbConn, sql)
  if row is None:
    print("Database operation failed...")
  elif row == ():
    print("Unexpected query failure...")
  else:
    print("# of assets",row[0])

#########################################################################
#Users
def users(bucketname, bucket, endpoint, dbConn):
  """
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  """
  sql = """
  select * from users order by userid desc;
  """
  row = datatier.retrieve_all_rows(dbConn, sql)
  if row is None:
    print("Database operation failed...")
  elif row == ():
    print("Unexpected query failure...")
  else:
    count=len(row)
    for i in range(count):
      #print(row[i])
      print(f"User id: {row[i][0]}\n Email: {row[i][1]}\n Name: {row[i][2]}\n Folder:{row[i][3]}")
#########################################################################
# Assets
# 
def assets(bucketname, bucket, endpoint, dbConn):
  """
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  """
  sql = """
  select * from assets order by assetid desc;
  """
  row = datatier.retrieve_all_rows(dbConn, sql)
  if row is None:
    print("Database operation failed...")
  elif row == ():
    print("Unexpected query failure...")
  else:
    count=len(row)
    for i in range(count):
      #print(row[i])
      print(f"Asset id: {row[i][0]}\n User id: {row[i][1]}\n Original Name: {row[i][2]}\n Key Name:{row[i][3]}")

#########################################################################
#Download
def download(bucketname, bucket, endpoint, dbConn):
  """
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  """
  a = input("Enter asset id\n")
  sql = f"""
  select assetname,bucketkey,bucketfolder from assets 
  inner join users where assets.userid = users.userid and  assetid = {a};
  """
  row = datatier.retrieve_all_rows(dbConn, sql)
  if row is None:
    print("Database operation failed...")
  elif row == ():
    print("Unexpected query failure...")
  else:
    #print(row)
    bname = awsutil.download_file(bucket, row[0][1])
    os.rename(bname, row[0][0])
    print(f"Downloaded from S3 and saved as '{row[0][0]}'")


#########################################################################
# main
#
print('** Welcome to PhotoApp **')
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
config_file = 'photoapp-config.ini'

print("What config file to use for this session?")
print("Press ENTER to use default (photoapp-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
  pass  # already set
else:
  config_file = s

#
# does config file exist?
#
if not pathlib.Path(config_file).is_file():
  print("**ERROR: config file '", config_file, "' does not exist, exiting")
  sys.exit(0)

#
# gain access to our S3 bucket:
#
s3_profile = 's3readwrite'

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file

boto3.setup_default_session(profile_name=s3_profile)

configur = ConfigParser()
configur.read(config_file)
bucketname = configur.get('s3', 'bucket_name')

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucketname)

#
# now let's connect to our RDS MySQL server:
#
endpoint = configur.get('rds', 'endpoint')
portnum = int(configur.get('rds', 'port_number'))
username = configur.get('rds', 'user_name')
pwd = configur.get('rds', 'user_pwd')
dbname = configur.get('rds', 'db_name')

dbConn = datatier.get_dbConn(endpoint, portnum, username, pwd, dbname)

if dbConn is None:
  print('**ERROR: unable to connect to database, exiting')
  sys.exit(0)

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
  #
  if cmd == 1:
    stats(bucketname, bucket, endpoint, dbConn)
  #
  #
  # TODO
  #
  #
  elif cmd == 2:
    users(bucketname, bucket, endpoint, dbConn)

  elif cmd == 3:
    assets(bucketname, bucket, endpoint, dbConn)

  elif cmd == 4:
    download(bucketname, bucket, endpoint, dbConn)

  else:
    print("** Unknown command, try again...")
  #
  cmd = prompt()

#
# done
#
print()
print('** done **')
