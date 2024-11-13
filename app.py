import streamlit as st
import requests
import time
import pandas as pd
import os
import re
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

API_QUERY = "http://127.0.0.1:5000/query"
CSV_FILE = "user_queries.csv"

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["timestamp", "user_query", "assistant_response", "symptoms", "relevant_context", "query", "assistant_feedback"])
    df.to_csv(CSV_FILE, index=False)

def generator(response):
    words = response.split(" ")
    for word in words:
        yield word + " "
        time.sleep(0.02)

def func_plot_data(csv_file):

    df = pd.read_csv(csv_file)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    df['date'] = df['timestamp'].dt.date
    df['week'] = df['timestamp'].dt.to_period('W')

    daily_queries = df.groupby('date').size()

    weekly_queries = df.groupby('week').size()

    st.subheader("Queries Over Time (Daily)")
    fig, ax = plt.subplots(figsize=(10, 6))
    daily_queries.plot(kind='line', marker='o', ax=ax)
    ax.set_title("User Queries Over Time (Daily)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Queries")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("Queries Over Time (Weekly)")
    fig, ax = plt.subplots(figsize=(10, 6))
    weekly_queries.plot(kind='line', marker='o', ax=ax)
    ax.set_title("User Queries Over Time (Weekly)")
    ax.set_xlabel("Week")
    ax.set_ylabel("Number of Queries")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(True)
    st.pyplot(fig)

    def clean_query(query):
        return re.findall(r'\b\w+\b', query.lower())

    all_queries = ' '.join(df['query'].dropna())
    words = clean_query(all_queries)

    word_counts = Counter(words)

    most_common_words = word_counts.most_common(20)
    temp = []
    for key, val in most_common_words:
        if key not in stopwords.words("english"):
            temp.append((key, val))
    top_words = dict(temp)

    st.subheader("Top 10 Keywords Frequency")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_words.keys(), top_words.values())
    ax.set_title("Most Common Keywords in User Queries")
    ax.set_xlabel("Keywords")
    ax.set_ylabel("Frequency")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)


page = st.radio("Choose a page", ("Chat", "Report"))

if page == "Chat":
    st.title("ChatBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = requests.post(API_QUERY, json={"query": prompt})
            
            if response.status_code == 200:
                assistant_response = response.json().get("response", "Sorry, I couldn't process your request.")
            else:
                assistant_response = "There was an error processing your request. Please try again."

            with st.chat_message("assistant"):
                st.write_stream(generator(assistant_response))

            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([[timestamp, prompt, assistant_response, "", "", prompt, ""]], 
                                   columns=["timestamp", "user_query", "assistant_response", "symptoms", "relevant_context", "query", "assistant_feedback"])

            df = pd.read_csv(CSV_FILE)
            df = df.append(new_row, ignore_index=True)
            df.to_csv(CSV_FILE, index=False)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            with st.chat_message("assistant"):
                st.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

elif page == "Report":
    func_plot_data(CSV_FILE)