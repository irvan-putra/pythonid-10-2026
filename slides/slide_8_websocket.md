FastAPI and WebSockets
======================

- FastAPI: a Python web framework; a decorator turns a function
  into a URL: @app.get("/"), @app.websocket("/audio")
- uvicorn: the web server that runs it

- HTTP: the browser asks, the server answers, done
- WebSocket: one connection that stays open, and both sides can
  send at any time -> good for streaming audio and video

Phone browsers only allow the camera and microphone on secure pages
(https:// or localhost). A Chrome flag treats the laptop's http://
address as secure.

Here: phone browser -> WebSocket -> laptop -> Whisper and YOLO
