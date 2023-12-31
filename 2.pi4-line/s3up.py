import boto3
from dotenv import load_dotenv
import json
import os

print('s3up.py')

load_dotenv()
client = boto3.client('s3')

# 最新の1件を取得
filename = sorted(os.listdir('./image/all/'))[-1]

# S3へアップロード
buckets = client.list_buckets()['Buckets'][0]['Name']
client.upload_file('./image/all/'+filename, buckets, filename)

