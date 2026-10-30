import atexit, pathlib, shutil, subprocess

# Local Mosquitto MQTT broker; mosquitto.conf lets the phone on the same Wi-Fi connect
MOSQUITTO = shutil.which("mosquitto") or r"C:\Program Files\mosquitto\mosquitto.exe"
CONFIG = pathlib.Path(__file__).with_name("mosquitto.conf")

def start(root, go):
    try:
        broker = subprocess.Popen([MOSQUITTO, "-c", str(CONFIG)])
        atexit.register(broker.terminate)  # stop the broker when the presentation closes
    except FileNotFoundError:
        print("Mosquitto not found: install it from https://mosquitto.org/download/", flush=True)
