import sys, json, subprocess, paho.mqtt.client as mqtt

# Runs on the phone (Termux): python 6_termux.py <laptop-ip>
if __name__ == "__main__":  # run on the phone; the presentation only shows this file
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(sys.argv[1])
    client.loop_start()
    command = ["termux-sensor", "-s", "accelerometer", "-d", "50"]  # a reading every 50 ms
    sensor = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    chunk = ""
    for line in sensor.stdout:  # termux-sensor prints each reading as multi-line JSON
        chunk += line
        if line.rstrip() in ("}", "{}"):
            for reading in json.loads(chunk).values():
                x, y, z = reading["values"]
                client.publish("pythonid/sensor", json.dumps({"x": x, "y": y, "z": z}))
            chunk = ""
