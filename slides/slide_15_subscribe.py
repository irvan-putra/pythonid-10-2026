import json, time, collections, pandas as pd, streamlit as st, paho.mqtt.client as mqtt

CLOUD, TOPIC = "broker.hivemq.com", "irvan-putra/pythonid-10-2026/"

@st.cache_resource
def live():
    data = {"history": collections.deque(maxlen=60 * 10), "text": "", "last": 0}
    def on_message(client, userdata, msg):
        if msg.topic == TOPIC + "speech":
            data["text"] = json.loads(msg.payload)
        elif time.time() - data["last"] >= 1:
            data["last"] = time.time()
            now = pd.Timestamp.now("Asia/Jakarta")
            data["history"].append({"time": now, **json.loads(msg.payload)})
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    topics = [(TOPIC + "votes", 0), (TOPIC + "speech", 0)]
    client.on_connect = lambda client, *args: client.subscribe(topics)
    client.on_message = on_message
    client.connect_async(CLOUD)
    client.loop_start()
    return data
