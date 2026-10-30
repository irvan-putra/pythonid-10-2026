import json, paho.mqtt.client as paho
import slide_1_whisper as whisper, slide_2_yolo as yolo, slide_6_mqtt as mqtt

# A public broker has no password: anyone can read or publish these topics,
# so never send private data through it.
cloud = paho.Client(paho.CallbackAPIVersion.VERSION2)
cloud.connect_async("broker.hivemq.com")
cloud.loop_start()
laptop_show, laptop_update, transcript = whisper.show, yolo.update, []

def publish(topic, data, retain=False):
    mqtt.publish(topic, data, retain)
    cloud.publish(f"irvan-putra/pythonid-10-2026/{topic}", json.dumps(data), retain=retain)

def show(subtitle, text):
    laptop_show(subtitle, text)
    transcript.append(text)
    publish("speech", " ".join(transcript), retain=True)

def update(video, image, people, hands):
    laptop_update(video, image, people, hands)
    publish("votes", {"people": people, "hands": hands})

whisper.show, yolo.update = show, update
