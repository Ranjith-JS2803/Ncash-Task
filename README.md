# Document-based Chatbot with Data Analytics and Summarization

This project is focused on building a chatbot system that interacts with users by analyzing documents stored in Google Cloud Storage (GCS). The system searches relevant data based on user questions and utilizes a Large Language Model (LLM) for summarizing responses. In addition to chatbot functionalities, the project includes a data analytics component that tracks and analyzes user queries to generate insights.

## Project Structure

- **`constants.py`**  
  This file initializes the embedding model and the LLM model.

- **`dataStorage.py`**  
  This file is responsible for storing the PDF files as blob objects in Google Cloud Storage.

- **`vectorStorage.py`**  
  This file handles the extraction of data from the provided documents and stores it in a vector database (Faiss).

- **`functions.py`**  
  This file is composed of modules to create bucket in GCS, upload the documents to GCS, access blob objects from GCS, download blob from GCS and generate response for user queries.

- **`api.py`**  
  This file has the endpoint for generating the response from extracted text from the PDF files.  

- **`app.py`**  
  This file contains the code for the Streamlit application, serving as the front-end for the chatbot.

## Project setup instructions
- Have a Direcory *DataFiles* to store all the PDF files.
- use the command **`python -m Streamlit run app.py`** to get the user interface (frontend).
- Before running the above command run **`python api.py`** which starts the backend server for fetching the reponse.

## Google Cloud Storage
 ![GCS_page](https://github.com/user-attachments/assets/cbbec1d6-5ecf-4182-b744-e82558da7cb0)

## Postman API test
![api_test](https://github.com/user-attachments/assets/8fa1daf4-1585-44ce-8255-d748aad5eeeb)

## Demo
 ![chat_page](https://github.com/user-attachments/assets/9e512cb1-db89-4427-92c0-1d04c4322f44)

![report_page](https://github.com/user-attachments/assets/d05e45ba-aaa9-46ba-bdd7-ddc7abec4e5d)
