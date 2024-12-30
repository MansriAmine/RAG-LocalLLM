from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import os
import subprocess
from fastapi.responses import StreamingResponse

app = FastAPI()

# Path to the folder where the PDFs are stored
UPLOAD_FOLDER = 'data'

class QuestionRequest(BaseModel):
    question: str
    file_name: str


@app.post("/ask")
async def ask_question(request: QuestionRequest):
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
    async def generate():
        process = subprocess.Popen(
            ['python', 'query.py', question],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line-buffered
            universal_newlines=True,
            encoding='utf-8'
        )
        try:
            for line in process.stdout:
                yield line  # Stream each line of the script's output
            process.stdout.close()
            return_code = process.wait()
            if return_code != 0:
                error_message = process.stderr.read()
                yield f"Error running query.py: {error_message}"
        except Exception as e:
            yield f"Error: {str(e)}"

    # Return the response as a stream
    return StreamingResponse(generate(), media_type="text/plain")
