async function streamCamera(stream) {
  video.srcObject = stream;
  await video.play();
  const ws = socket("camera");
  const canvas = document.createElement("canvas");
  const send = () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    canvas.toBlob((jpeg) => ws.send(jpeg), "image/jpeg", 0.7);
  };
  ws.onopen = send;
  ws.onmessage = (event) => { camera.textContent = event.data; send(); };
}
