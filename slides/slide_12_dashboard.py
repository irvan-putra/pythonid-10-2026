import json, time, subprocess, sys, collections
import pandas as pd, streamlit as st, slide_5_mqtt as mqtt
from wordcloud import WordCloud

def start(root, go):
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", __file__])

@st.cache_resource  # one MQTT subscriber, shared by every phone viewing the dashboard
def live():
    data = {"history": collections.deque(maxlen=60 * 10), "text": "", "last": 0}  # 10 minutes
    def on_message(client, userdata, msg):
        if msg.topic == "pythonid/speech":
            data["text"] = json.loads(msg.payload)
        elif time.time() - data["last"] >= 1:  # votes come every frame: keep 1 row per second
            data["last"] = time.time()
            data["history"].append({"time": data["last"], **json.loads(msg.payload)})
    mqtt.listen(["votes", "speech"], on_message)
    return data

if __name__ == "__main__":
    @st.fragment(run_every=1)
    def live_charts():
        data = live()
        if not data["history"]:
            return st.info("⏳ Waiting for votes...")
        history = pd.DataFrame(list(data["history"]))
        history["time"] = pd.to_datetime(history["time"], unit="s")
        latest = history.iloc[-1]
        approval = latest["hands"] / max(latest["people"], 1)
        c1, c2, c3 = st.columns(3)
        c1.metric("👥 People", latest["people"], f"record {history.people.max()}")
        c2.metric("✋ Votes", latest["hands"], f"record {history.hands.max()}")
        c3.metric("👍 Approval", f"{approval:.0%}")
        st.area_chart(history.set_index("time")[["people", "hands"]])
        cloud = WordCloud(width=800, height=300, background_color="white")
        if words := cloud.process_text(data["text"]):
            st.image(cloud.generate_from_frequencies(words).to_image())

    live_charts()
