What we just built
==================

  laptop or phone mic    ──► Whisper ──► "next" / "back" ──► slides
  laptop or phone mic    ──► Whisper ──► transcript    ──► MQTT ──► word cloud
  laptop or phone camera ──► YOLO    ──► people, hands ──► MQTT ──► dashboard
  phone accelerometer    ──► Termux  ──► MQTT          ──► sensor LED

  MQTT:      Mosquitto on the laptop + the public broker.hivemq.com
  dashboard: Streamlit, on the laptop and online

All of the AI runs on this laptop's CPU: no GPU, no paid API.
Only the dashboard's data goes online, and the rest keeps
working without internet.
