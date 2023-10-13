#
# Main program for photoapp program using AWS S3 and RDS to
# implement a simple photo application for photo storage and
# viewing.
#
# Authors:
#   YOUR NAME
#   Shraddha Ravishanker
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
    print("# of users:",row[0])

  sql = """
  select count(*) from assets;
  """
  row = datatier.retrieve_one_row(dbConn, sql)
  if row is None:
    print("Database operation failed...")
  elif row == ():
    print("Unexpected query failure...")
  else:
    print("# of assets:",row[0])

#########################################################################
#Users
#
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
      print(f"User id: {row[i][0]}\n Email: {row[i][1]}\n Name: {row[i][2]} , {row[i][3]}\n Folder: {row[i][4]}")

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
      print(f"Asset id: {row[i][0]}\n  User id: {row[i][1]}\n  Original name: {row[i][2]}\n  Key name: {row[i][3]}")

#########################################################################
#Download
#
def download(bucketname, bucket, endpoint, dbConn, display):
  """
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  display: Parameter to control whether the function displays the image
  """
  a = input("Enter asset id>\n")
  sql = """
  select assetname,bucketkey,bucketfolder from assets 
  inner join users where assets.userid = users.userid and  assetid = %s;
  """
  row = datatier.retrieve_all_rows(dbConn, sql, [a])
  if not row:
    print("No such asset...")
    #sys.exit()
  else:
    #print(row)
    bname = awsutil.download_file(bucket, row[0][1])
    os.rename(bname, row[0][0])
    print(f"Downloaded from S3 and saved as ' {row[0][0]} '")

    if display:
      image = img.imread(row[0][0])
      plt.imshow(image)
      plt.show()
#########################################################################
#Upload
#
def upload(bucketname, bucket, endpoint, dbConn):
  """
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  """
  local_filename = input("Enter the local filename\n")
  if not os.path.exists(local_filename):
    print(f"local file {local_filename} does not exist...")
    return

  user_id = input("Enter the user id\n")

  sql = """
  select bucketfolder from users where userid = %s;
  """
  row = datatier.retrieve_all_rows(dbConn, sql, [user_id])
  
  if not row :
    print("No such user...")
  else:
    #print(row[0][0])
    uid= str(uuid.uuid4()) + ".jpg"
    keyname = row[0][0] + '/' + uid

    e= awsutil.upload_file(local_filename, bucket, keyname)
    if (e != -1):
        sql = """
        insert into assets (userid,assetname,bucketkey) 
        values( %s, %s, %s)
        """
        insert_result=datatier.perform_action(dbConn, sql,[user_id,local_filename,keyname ])

        if insert_result != -1:
            sql = """
            select last_insert_id()
            """
            row = datatier.retrieve_all_rows(dbConn, sql)
            print(f"Uploaded and stored in S3 as ' {keyname} ' Recorded in RDS under asset id {row[0][0]}")
            assets(bucketname, bucket, endpoint, dbConn)

    
#########################################################################
#Add User
#
def adduser(bucketname, bucket, endpoint, dbConn):
  """
  Parameters
  ----------
  bucketname: S3 bucket name,
  bucket: S3 boto bucket object,
  endpoint: RDS machine name,
  dbConn: open connection to MySQL server
  """
  email= input("Enter user's email\n")
  last_name = input("Enter user's last (family) name\n")
  first_name = input("Enter user's first (given) name\n")
  uid= str(uuid.uuid4()) 

  sql = """
  INSERT INTO users(email, lastname, firstname, bucketfolder)
  values(%s, %s, %s,%s)
  """
  insert_result=datatier.perform_action(dbConn, sql,[email,last_name,first_name, uid ])
  if insert_result != -1:
            sql = """
            select last_insert_id()
            """
            row = datatier.retrieve_all_rows(dbConn, sql)
            print(f" Recorded in RDS under user id {row[0][0]}")


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
    download(bucketname, bucket, endpoint, dbConn, display=False)

  elif cmd == 5:
    
    download(bucketname, bucket, endpoint, dbConn,display=True)

  elif cmd == 6:
    upload(bucketname, bucket, endpoint, dbConn)

  elif cmd == 7:
    adduser(bucketname, bucket, endpoint, dbConn)

  else:
    print("** Unknown command, try again...")
  #
  cmd = prompt()

#
# done
#
print()
print('** done **')
