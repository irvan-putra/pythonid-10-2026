import json, time, collections, pandas as pd, streamlit as st, slide_6_mqtt as mqtt

@st.cache_resource
def live():
    data = {"history": collections.deque(maxlen=60 * 10), "text": "", "last": 0}
    def on_message(client, userdata, msg):
        if msg.topic == "pythonid/speech":
            data["text"] = json.loads(msg.payload)
        elif time.time() - data["last"] >= 1:
            data["last"] = time.time()
            data["history"].append({"time": pd.Timestamp.now(), **json.loads(msg.payload)})
    mqtt.listen(["votes", "speech"], on_message)
    return data
