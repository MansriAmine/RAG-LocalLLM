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

    # Get the user's question
    question = request.question

    # Print the question in the terminal
    print(f"Received Question: {question}")

    # Run the query.py script and stream the output
    #async def generate():
    X= query_rag(question) 
    print(X)
    print(type(X))

    # try:
    #     print(X)
    #     print(type(X))
    # except Exception as e:
    #     yield f"Error: {str(e)} azerty"
    
    # Return the response as a stream
    #return StreamingResponse(generate(), media_type="text/plain")
    data = {"res":X}
    return data
    #return {"answer": data}

