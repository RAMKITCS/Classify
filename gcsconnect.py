import os,io,json
from difflib import get_close_matches
from google.cloud import storage
from secret import get_service_account
from google.oauth2 import service_account
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
bucket = storage_client.bucket(bucket_name)
from google.cloud import vision
import time
import io
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english')) 
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
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
def list_blob_all(prefix=None):
    blobs = storage_client.list_blobs(os.environ['bucket_name'],prefix=prefix)
    for blob in blobs:
        print(blob.name)
def download_to_local(filename,name):
    blob=bucket.blob(filename)
    blob.download_to_filename(name)