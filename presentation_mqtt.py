import json, paho.mqtt.client as mqtt

def listen(topics, on_message, userdata=None):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=userdata)
    subscriptions = [(f"pythonid/{topic}", 0) for topic in topics]  # (topic, QoS 0)
    client.on_connect = lambda client, *args: client.subscribe(subscriptions)
    client.on_message = on_message
    client.connect_async("localhost")  # keeps retrying in the background until Mosquitto runs
    client.loop_start()

sender = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # YOLO and Whisper publish through it
sender.connect_async("localhost")
sender.loop_start()

def publish(topic, data, retain=False):  # retain: broker keeps the last one for new subscribers
    sender.publish(f"pythonid/{topic}", json.dumps(data), retain=retain)

# Phone accelerometer -> MQTT -> Python (phone side: phone/sensor_termux.py)
def on_message(client, led, msg):
    reading = json.loads(msg.payload)
    x, y, z = reading["x"], reading["y"], reading["z"]
    force = (x * x + y * y + z * z) ** 0.5  # m/s², about 9.8 when the phone is still
    color = "red" if force > 15 else "gray"  # shake = LED on (or serial.write to an Arduino)
    led.after(0, led.config, {"fg": color, "text": f"● Phone: {force:4.1f} m/s²"})

def start(root):
    import tkinter as tk  # only the presentation needs Tk; the dashboard imports this file too
    led = tk.Label(root, text="● Waiting for phone...", font=("Consolas", 12), fg="gray")
    led.pack(side="bottom")
    listen(["sensor"], on_message, led)
