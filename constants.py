import os
from google.cloud import storage
import google.generativeai as genAI
from langchain_huggingface import HuggingFaceEmbeddings

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'googleCloudStorage-serviceKey.json'
storage_client = storage.Client()
bucket_name = "ncash_task_data_bucket"

with open("generativeAI-serviceKey", "r") as f:
    api_key = f.readline()
genAI.configure(api_key = api_key)

model = genAI.GenerativeModel("gemini-1.5-flash")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")