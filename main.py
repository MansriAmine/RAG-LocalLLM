from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import os
import subprocess
from fastapi.responses import StreamingResponse
from query import query_rag 
app = FastAPI()

# Path to the folder where the PDFs are stored
UPLOAD_FOLDER = 'data'

class QuestionRequest(BaseModel):
    question: str
    file_name: str


@app.post("/ask")
def ask_question(request: QuestionRequest):
    """Handle the question and stream the answer"""
    # Construct the file path
    file_path = os.path.join(UPLOAD_FOLDER, request.file_name)
    
    if not os.path.exists(file_path):
        return {"error": "PDF file not found"}
    else :
        print("PDF file found")
        # call createDB fucntion
        

    # Get the user's question
    question = request.question

    # Print the question in the terminal
    print(f"Received Question: {question}")

    # Run the query.py script and stream the output
    answer = query_rag(question) 
    #print(answer)

    data = {"res":answer}
    return data

