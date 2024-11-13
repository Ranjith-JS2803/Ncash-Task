from constants import *
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
import torch
import faiss
import pickle
import os

def func_create_bucket(bucket_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        bucket.location = "ASIA-SOUTH1"
        bucket = storage_client.create_bucket(bucket)
        return True
    except Exception as e:
        print(e)
        return False

def func_upload_document(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False

def func_access_blobs(bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()
        return blobs
    except Exception as e:
        print(e)
        return None

def func_vector_store(pages):
    try:
        faiss_index = FAISS.from_documents(pages,embeddings)
        faiss.write_index(faiss_index.index, "docs.index")
        with open("faiss_store.pkl", "wb") as f:
            pickle.dump(faiss_index, f)
        print("FAISS vector Store is created!!")
    except Exception as e:
        print(e)

def func_download_documents(blob_name, local_filename, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(local_filename)
        print(f"Downloaded {blob_name} to {local_filename}.")        
    except Exception as e:
        print(e)

def func_response_generator(query):
    if not os.path.exists("faiss_store.pkl"):
        func_download_documents("vectorDB/faiss_store.pkl", "faiss_store.pkl", bucket_name)
    if not os.path.exists("docs.index"):        
        func_download_documents("vectorDB/docs.index", "docs.index", bucket_name)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    faiss_store_path = os.path.join(current_dir, "faiss_store.pkl")
    docs_index_path = os.path.join(current_dir, "docs.index")

    try:
        with open(faiss_store_path, "rb") as f:
            store = pickle.load(f)
        store.index = faiss.read_index(docs_index_path)
    except Exception as e:
        return f"Error loading FAISS store: {str(e)}" 
    
    prompt_template = PromptTemplate(
            input_variables=["query", "context"],
            template="""
            You are a medical assistant specialized in providing information about health-related queries.
            Please analyze the following symptoms and provide a relevant medical response based on the context provided.

            Question: {query}
            Context: {context}
            """
        )
        
    try:
        relevant_docs = store.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        prompt = prompt_template.format(query=query, context=context)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during processing: {str(e)}"
