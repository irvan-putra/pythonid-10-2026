import json, tkinter as tk, paho.mqtt.client as mqtt

# Phone accelerometer -> MQTT -> Python (phone side: experiments/phone_sensor_termux.py)
def on_message(client, led, msg):
    reading = json.loads(msg.payload)
    x, y, z = reading["x"], reading["y"], reading["z"]
    force = (x * x + y * y + z * z) ** 0.5  # m/s², about 9.8 when the phone is still
    color = "red" if force > 15 else "gray"  # shake = LED on (or serial.write to an Arduino)
    led.after(0, led.config, {"fg": color, "text": f"● Phone: {force:4.1f} m/s²"})

def start(root):
    led = tk.Label(root, text="● Waiting for phone...", font=("Consolas", 12), fg="gray")
    led.pack(side="bottom")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=led)
    client.on_connect = lambda client, *args: client.subscribe("pythonid/sensor")
    client.on_message = on_message
    client.connect_async("localhost")  # keeps retrying in the background until Mosquitto runs
    client.loop_start()
