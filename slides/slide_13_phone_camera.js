let turn = 0;
addEventListener("devicemotion", (event) => {
  const { x, y } = event.accelerationIncludingGravity;
  const held = Math.abs(y) > Math.abs(x) ? (y > 0 ? 0 : 180) : (x > 0 ? 90 : 270);
  turn = (held - (screen.orientation?.angle ?? 0) + 360) % 360;
});

async function streamCamera(stream) {
  video.srcObject = stream;
  await video.play();
  const ws = socket("camera");
  const canvas = document.createElement("canvas");
  const send = () => {
    const [w, h] = [video.videoWidth, video.videoHeight];
    [canvas.width, canvas.height] = turn % 180 ? [h, w] : [w, h];
    const draw = canvas.getContext("2d");
    draw.translate(canvas.width / 2, canvas.height / 2);
    draw.rotate((-turn * Math.PI) / 180);
    draw.drawImage(video, -w / 2, -h / 2);
    canvas.toBlob((jpeg) => ws.send(jpeg), "image/jpeg", 0.7);
  };
  ws.onopen = send;
  ws.onmessage = (event) => { camera.textContent = event.data; send(); };
}
