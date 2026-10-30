import atexit, pathlib, shutil, subprocess

MOSQUITTO = shutil.which("mosquitto") or r"C:\Program Files\mosquitto\mosquitto.exe"
CONFIG = pathlib.Path(__file__).with_name("slide_5_mosquitto.conf")

def start(root, go):
    try:
        broker = subprocess.Popen([MOSQUITTO, "-c", str(CONFIG)])
        atexit.register(broker.terminate)
        check = lambda: broker.poll() is None or print("Mosquitto stopped: is port 1883 in use?")
        root.after(2000, check)
    except FileNotFoundError:
        print("Mosquitto not found: install it from https://mosquitto.org/download/", flush=True)
