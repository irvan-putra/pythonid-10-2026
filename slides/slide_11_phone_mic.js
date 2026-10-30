function streamMic(stream, ctx) {
  const ws = socket("audio");
  ws.onclose = () => (state.textContent = "Disconnected from laptop");
  const tap = ctx.createScriptProcessor(4096, 1, 1);
  tap.onaudioprocess = (event) => {
    const samples = event.inputBuffer.getChannelData(0);
    if (ws.readyState === 1) ws.send(samples);
    mic.textContent = `🎙 mic level ${Math.max(...samples).toFixed(2)}`;
  };
  ctx.createMediaStreamSource(stream).connect(tap);
  tap.connect(ctx.destination);
}
