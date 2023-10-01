import uuid
import pymysql
import sys

sys.tracebacklimit = 0

# generate random uuid
#print(uuid.uuid4())

#
# Copy-paste your AWS RDS endpoint here:
#
ENDPOINT="mysql-shraddha-cs310.ckskzf2lj7lo.us-east-2.rds.amazonaws.com"
#
# master username? Default was admin:
#
USER="admin"
#
# what password did you supply for the master user?
#
PASSWORD="Uiopkl8!"
#
# leave this as "sys"
#
DBNAME="sys"

print('starting...')
print()

#
# if all is well, program outputs the current date
# and time GMT (Greenwich Mean Time):
#
try:
  dbconn =  pymysql.connect(
    host=ENDPOINT, 
    user=USER, 
    passwd=PASSWORD, 
    database=DBNAME)
  cursor = dbconn.cursor()
  cursor.execute("""SELECT now()""")
  query_results = cursor.fetchall()
  print(query_results)
except Exception as e:
  print("Database connection failed due to {}".format(e))
  sys.exit(-1)

cursor.close()
dbconn.close()

print()
print('done')
