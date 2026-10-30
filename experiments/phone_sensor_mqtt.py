import json, tkinter as tk, paho.mqtt.client as mqtt

# Runs on the laptop: phone accelerometer -> MQTT -> local "hardware" loop
root = tk.Tk()
root.title("Phone Sensor -> MQTT -> Python")
led = tk.Label(root, text="●", font=("Consolas", 120), fg="gray")
led.pack()
readout = tk.Label(root, text="Waiting for phone...", font=("Consolas", 14))
readout.pack(pady=10)

def on_message(client, userdata, msg):
    reading = json.loads(msg.payload)
    root.after(0, show, reading["x"], reading["y"], reading["z"])

def show(x, y, z):
    force = (x * x + y * y + z * z) ** 0.5  # m/s², about 9.8 when the phone is still
    led.config(fg="red" if force > 15 else "gray")  # shake = LED on (or serial.write to an Arduino)
    readout.config(text=f"x {x:6.1f}  y {y:6.1f}  z {z:6.1f}  |a| {force:5.1f}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost")
client.subscribe("pythonid/sensor")
client.loop_start()
root.mainloop()
