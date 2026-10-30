import os, json, time, urllib.request

URL, TOKEN = os.environ.get("UPSTASH_REDIS_REST_URL"), os.environ.get("UPSTASH_REDIS_REST_TOKEN")
live, last_push = {"slide": 0, "slides": {}, "text": ""}, 0

def redis(*cmds):
    req = urllib.request.Request(f"{URL}/pipeline", json.dumps(cmds).encode(), {"Authorization": f"Bearer {TOKEN}"})
    return [r["result"] for r in json.load(urllib.request.urlopen(req, timeout=2))]

def push(people):
    global last_push
    if time.time() - last_push < 1:
        return
    last_push, hands = time.time(), sum(1 for l, r in people if l or r)
    row = json.dumps({"t": last_push, "slide": live["slide"], "people": len(people), "hands": hands,
                      "left": sum(l for l, r in people), "right": sum(r for l, r in people)})
    live["slides"][live["slide"]] = max(live["slides"].get(live["slide"], 0), hands)
    now = json.dumps(live)
    try:
        if URL:
            redis(["LPUSH", "history", row], ["LTRIM", "history", "0", "599"], ["SET", "live", now])
        else:
            open("votes.txt", "a").write(row + "\n"), open("live.json", "w").write(now)
    except Exception as e:
        print("push failed:", e, flush=True)

def read():
    if URL:
        rows, now = redis(["LRANGE", "history", "0", "599"], ["GET", "live"])
        return [json.loads(r) for r in rows[::-1]], json.loads(now)
    return [json.loads(r) for r in open("votes.txt").readlines()[-600:]], json.load(open("live.json"))
