import pathlib, threading, uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def page():
    return FileResponse(pathlib.Path(__file__).with_name("slide_9_sensor.html"))

def start(root, go):
    server = {"app": app, "host": "0.0.0.0", "port": 8000, "log_level": "warning"}
    threading.Thread(target=uvicorn.run, kwargs=server, daemon=True).start()
