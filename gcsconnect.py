import os,io,json
from difflib import get_close_matches
from google.cloud import storage
from secret import get_service_account
from google.oauth2 import service_account
import datetime
#os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.environ['gcp']
if 'gcp_secret' in os.environ and os.environ['gcp_secret'] is not None:
    #os.environ['GOOGLE_APPLICATION_CREDENTIALS']=os.environ['gcp']
    if "SAkey.json" not in os.listdir("Service/"):
        info=get_service_account(os.environ['secret_id'])
        print(info)
        storage_credentials = service_account.Credentials.from_service_account_info(info)
        #print(storage_credentials)
        storage_client = storage.Client(project=info["project_id"], credentials=storage_credentials)
        open("Service/SAkey.json","w").write(json.dumps(info))
        print("Called Secret")
    else:
        print("Called using Cache")
        storage_credentials = service_account.Credentials.from_service_account_info(json.load(open("Service/SAkey.json")))
        storage_client = storage.Client(project=os.getenv("project_id"), credentials=storage_credentials)
#storage_client = storage.Client()
bucket_name=os.environ['bucket_name']
print(bucket_name)
bucket = storage_client.bucket(bucket_name)
bucket2 = storage_client.bucket(bucket_name+"3")
from google.cloud import vision
import time
import io
def read_file(filename):
    blob=bucket.blob(filename)
    return blob.download_as_string()
def read_file_io(filename):
    blob=bucket.blob(filename)
    f=io.BytesIO()
    blob.download_to_file(f)
    f.seek(0)
    return f
def write_file_io(filename,content):
    blob=bucket.blob(filename)
    blob.upload_from_file(content)
    return 'completed'
def write_file(filename,content):
    blob=bucket.blob(filename)
    blob.upload_from_string(content)
    return 'completed'
def write_file_bucket2(filename,content):
    blob=bucket2.blob(filename)
    blob.upload_from_string(content)
    return 'completed'
def list_blob_all(prefix=None):
    blobs = storage_client.list_blobs(os.environ['bucket_name'],prefix=prefix)
    for blob in blobs:
        print(blob.name)
def download_to_local(filename,name):
    blob=bucket.blob(filename)
    blob.download_to_filename(name)
def get_signed_url(filename,action,download_name):
    print((filename,action,download_name))
    blob=bucket2.blob(filename)
    url=blob.generate_signed_url(
        expiration=datetime.timedelta(seconds=20),
        method=action,
        version='v4',
        response_disposition='attachment;filename='+download_name)
    return url
def get_signed_url2(filename,action):
    print((filename,action))
    blob=bucket.blob(filename)
    url=blob.generate_signed_url(
        expiration=datetime.timedelta(seconds=60),
        method=action,
        version='v4')
    return url