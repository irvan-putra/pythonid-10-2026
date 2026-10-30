function streamMic(stream, actx) {
  const ws = socket("audio");
  ws.onclose = () => (state.textContent = "Disconnected from laptop");
  const tap = actx.createScriptProcessor(4096, 1, 1);
  tap.onaudioprocess = (event) => {
    const samples = event.inputBuffer.getChannelData(0);
    if (ws.readyState === 1) ws.send(samples);
    mic.textContent = `🎙 mic level ${Math.max(...samples).toFixed(2)}`;
  };
  actx.createMediaStreamSource(stream).connect(tap);
  tap.connect(actx.destination);
}
