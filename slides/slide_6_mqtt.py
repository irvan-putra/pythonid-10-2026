import json, math, paho.mqtt.client as mqtt

def listen(topics, on_message, userdata=None):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=userdata)
    subscriptions = [(f"pythonid/{topic}", 0) for topic in topics]
    client.on_connect = lambda client, *args: client.subscribe(subscriptions)
    client.on_message = on_message
    client.connect_async("localhost")
    client.loop_start()

sender = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
sender.connect_async("localhost")
sender.loop_start()

def publish(topic, data, retain=False):
    sender.publish(f"pythonid/{topic}", json.dumps(data), retain=retain)

def on_message(client, led, msg):
    reading = json.loads(msg.payload)
    x, y, z = reading["x"], reading["y"], reading["z"]
    force = math.sqrt(x * x + y * y + z * z)
    color = "red" if force > 15 else "gray"
    led.after(0, led.config, {"fg": color, "text": f"● Phone: {force:4.1f} m/s²"})

def start(root, go):
    import tkinter as tk
    led = tk.Label(root, text="● Waiting for phone...", font=("Consolas", 12), fg="gray")
    led.pack(pady=5)
    listen(["sensor"], on_message, led)
