import sys, json, subprocess, paho.mqtt.client as mqtt

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(sys.argv[1])
    client.loop_start()
    command = ["termux-sensor", "-s", "accelerometer", "-d", "50"]  # 50ms delay = 20 readings / second
    sensor = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    chunk = ""
    for line in sensor.stdout:
        chunk += line
        if line.rstrip() in ("}", "{}"):
            for reading in json.loads(chunk).values():
                x, y, z = reading["values"]
                client.publish("pythonid/sensor", json.dumps({"x": x, "y": y, "z": z}))
            chunk = ""
