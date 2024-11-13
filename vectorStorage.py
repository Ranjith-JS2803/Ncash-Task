from functions import *
from constants import *
from langchain_community.document_loaders import PyPDFLoader

directory_path = "DataFiles/"
pages = []

for ind, file_name in enumerate(os.listdir(directory_path)):
    pdf_path = directory_path + file_name
    loader = PyPDFLoader(pdf_path)
    pages += loader.load_and_split()
    print(f"Extracted from Document - {ind+1}")
    
func_vector_store(pages)
if func_upload_document("vectorDB/faiss_store.pkl", "faiss_store.pkl", bucket_name):
    print("FAISS pickle file stored in GCS!!")
if func_upload_document("vectorDB/docs.index", "docs.index", bucket_name):
    print("FAISS DOCS index file stored in GCS!!")