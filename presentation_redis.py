import os, json, time, urllib.request

URL, TOKEN = os.environ.get("UPSTASH_REDIS_REST_URL"), os.environ.get("UPSTASH_REDIS_REST_TOKEN")
live, last_push = {"text": ""}, 0

def redis(*commands):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    request = urllib.request.Request(f"{URL}/pipeline", json.dumps(commands).encode(), headers)
    return [reply["result"] for reply in json.load(urllib.request.urlopen(request, timeout=2))]

def push(people, hands):
    global last_push
    if time.time() - last_push < 1:
        return
    last_push = time.time()
    row = json.dumps({"time": last_push, "people": people, "hands": hands})
    live_json = json.dumps(live)
    try:
        if URL:
            redis(["LPUSH", "history", row], ["LTRIM", "history", "0", "599"], ["SET", "live", live_json])
        else:
            open("votes.txt", "a").write(row + "\n"), open("live.json", "w").write(live_json)
    except Exception as error:
        print("push failed:", error, flush=True)

def read():
    if URL:
        rows, live_json = redis(["LRANGE", "history", "0", "599"], ["GET", "live"])
        return [json.loads(row) for row in rows[::-1]], json.loads(live_json)
    return [json.loads(row) for row in open("votes.txt").readlines()[-600:]], json.load(open("live.json"))
