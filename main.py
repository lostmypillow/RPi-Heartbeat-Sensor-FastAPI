from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import os
from subprocess import Popen, PIPE
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/script")
def run_script():
    script_path = "mock_hb.py"
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Script not found")
    
    try:
        process = Popen(["python", script_path], stdout=PIPE, stderr=PIPE, text=True, bufsize=1)
        def stream_output():
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll()is not None:
                    break
                if output:
                    yield output.strip()
        return StreamingResponse(stream_output(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occured")
