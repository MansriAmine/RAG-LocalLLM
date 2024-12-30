import streamlit as st
import requests
import os

# Streamlit UI
st.title("LLM-Powered PDF Question Answering")

# Define the folder to store uploaded files
upload_folder = 'data'

# Create the 'data' folder if it doesn't exist
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# File upload
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    # Save the uploaded file to the 'data' folder
    file_path = os.path.join(upload_folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Let the user ask a question
    question = st.text_input("Ask a question about the PDF:")

    if question:
        # Send the question to the FastAPI backend
        url = "http://localhost:8000/ask"  # Adjust the URL if needed
        data = {'question': question, 'file_name': uploaded_file.name}
        
        # Send POST request to FastAPI backend
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            st.write("Answer: ", response.json()['answer'])  # Display the answer
        else:
            st.error("Failed to get an answer from the server")
