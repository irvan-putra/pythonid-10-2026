import queue, numpy as np, slide_1_whisper as whisper
from fastapi import WebSocket, WebSocketDisconnect
from slide_8_sensor import app

chunks, phone, laptop_record = queue.Queue(), {"connected": False}, whisper.record

@app.websocket("/audio")
async def audio(ws: WebSocket):
    await ws.accept()
    phone["connected"], buffer = True, np.zeros(0, np.float32)
    try:
        while True:
            buffer = np.append(buffer, np.frombuffer(await ws.receive_bytes(), np.float32))
            if len(buffer) >= 32000:
                chunks.put(buffer)
                buffer = np.zeros(0, np.float32)
    except WebSocketDisconnect:
        phone["connected"] = False

def record():
    if phone["connected"]:
        try:
            return chunks.get(timeout=3)
        except queue.Empty:
            pass
    return laptop_record()

whisper.record = record
