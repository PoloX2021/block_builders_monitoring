import psycopg2
from dotenv import load_dotenv
import os
import re
import json
from identifyBlock import list_bundles
import datetime

load_dotenv()  # take environment variables from .env.
pw = os.getenv("PASSWORD")

connection = psycopg2.connect(
    host="cow-analytics-db.cgabamo3x0wl.eu-central-1.rds.amazonaws.com",
    database="solver_slippage",
    user="solver_slippage_readonly",
    password=pw
)
print(datetime.datetime.fromtimestamp(1615864957))
minBlock = 19511131
maxBlock = 19511163 +1

l = list_bundles(minBlock, maxBlock)
print(len(l))
print(l[0].keys())
j = 0
for i in l:
    j+=1
    with connection.cursor() as cursor:     
                cursor.execute(
                    "INSERT INTO bundlesmevblocker (bundleId, blockNumber, timestamp, transactions) VALUES ('%s', '%s', TO_TIMESTAMP(%s, 'YYYY-MM-DD HH24:MI:SS.US'), %s)",
                    (int(i['blockNumber']), int(i['bundleId']), str( datetime.datetime.fromtimestamp(int(i['timestamp'])/1000)), json.dumps(json.loads(i['transactions'])))
                )
    connection.commit()
    if j%100==0:
        print(j)
