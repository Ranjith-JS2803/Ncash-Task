# Document-based Chatbot with Data Analytics and Summarization

MedBot is a chatbot that integrates a large language model (LLM) with retrieval-augmented generation (RAG) to ensure access to the latest knowledge in the medical domain.

## Project Structure

- **`constants.py`**  
  This file initializes the embedding model and the LLM model.

- **`vectorStore.py`**  
  This file handles the extraction of data from the provided documents and stores it in a vector database (Faiss).

- **`medgpt.py`**  
  This file is responsible for generating responses to user queries by using a LLM model with retrieval-augmented generation (RAG) to fetch the necessary context.

- **`server.py`**  
  This file contains the code for the Streamlit application, serving as the front-end for the chatbot.
  
## Demo 
 ![Screenshot 2024-09-27 095925](https://github.com/user-attachments/assets/988c3aa9-ddb2-49df-b1cb-76fd3efe4925)
