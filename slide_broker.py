import atexit, shutil, subprocess

# Local Mosquitto MQTT broker; phone/mosquitto.conf lets the phone on the same Wi-Fi connect
MOSQUITTO = shutil.which("mosquitto") or r"C:\Program Files\mosquitto\mosquitto.exe"

def start():
    try:
        broker = subprocess.Popen([MOSQUITTO, "-c", "phone/mosquitto.conf"])
        atexit.register(broker.terminate)  # stop the broker when the presentation closes
    except FileNotFoundError:
        print("Mosquitto not found: install it from https://mosquitto.org/download/", flush=True)
