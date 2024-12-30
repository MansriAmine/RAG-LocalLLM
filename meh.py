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
        # Send the question and file to your backend (replace the URL with your app's API endpoint)
        url = "http://127.0.0.1:8000"  # Replace with your app's API endpoint
        files = {'pdf': open(file_path, 'rb')}
        data = {'question': question}
        
        # Send POST request to the server with PDF file and question
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            st.write("Answer: ", response.text)  # Display the answer returned from your backend
        else:
            st.error("Failed to get an answer from the server")
