from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import os
import subprocess
from fastapi.responses import FileResponse

app = FastAPI()

# Path to the folder where the PDFs are stored
UPLOAD_FOLDER = 'data'

class QuestionRequest(BaseModel):
    question: str
    file_name: str


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Handle the question and return the answer"""
    # Construct the file path
    file_path = os.path.join(UPLOAD_FOLDER, request.file_name)
    
    if not os.path.exists(file_path):
        return {"error": "PDF file not found"}

    # Get the user's question
    question = request.question

    # Print the question in the terminal
    print(f"Received Question: {question}")

    # Run the query.py script with the question as an argument
    answer = run_query_script(question)

    # Print the answer in the terminal
    print(f"Answer: {answer}")

    # Return the response (the answer from the query.py script)
    return {"answer": answer}


def run_query_script(question: str) -> str:
    """Run the query.py script with the question"""
    # Construct the command to run query.py with the question
    command = ['python', 'query.py', question]

    # Print the command for debugging purposes
    print(f"Running command: {' '.join(command)}")

    try:
        # Run the command and capture the output, handle Unicode characters
        result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.strip()  # Return the output of the script (answer)
    except subprocess.CalledProcessError as e:
        # If there is an error while running the script, return the error message
        return f"Error running query.py: {e.stderr}"
