import os
from functions import *
from constants import *

flag_create_bucket = func_create_bucket(bucket_name)

directory_path = "DataFiles/"
file_names = os.listdir(directory_path)
for ind, file_name in enumerate(file_names):
    file_path = os.path.join(directory_path, file_name)
    flag_file = func_upload_document(f"documents/Doc-{ind+1}", file_path, bucket_name)
    if flag_file : print(f"File - {file_name} added to the bucket")
    else : print(f"File - {file_name} NOT added to the bucket")