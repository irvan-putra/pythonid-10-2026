import os, json, time, urllib.request

# Upstash Redis REST relay: laptop pushes, deployed dashboard reads (falls back to local votes.txt)
URL, TOKEN = os.environ.get("UPSTASH_REDIS_REST_URL"), os.environ.get("UPSTASH_REDIS_REST_TOKEN")
last_push = 0

def redis(cmd):
    req = urllib.request.Request(f"{URL}/{cmd}", headers={"Authorization": f"Bearer {TOKEN}"})
    return json.load(urllib.request.urlopen(req, timeout=2))["result"]

def push(people, hands):
    global last_push
    if URL and time.time() - last_push > 1:
        last_push = time.time()
        try:
            redis(f"set/votes/{people},{hands}")
        except Exception as e:
            print("push failed:", e, flush=True)

def read():
    return redis("get/votes") if URL else open("votes.txt").read()
