import os, json, time, urllib.request

URL, TOKEN = os.environ.get("UPSTASH_REDIS_REST_URL"), os.environ.get("UPSTASH_REDIS_REST_TOKEN")
live, last_push = {"slide": 0, "slides": {}, "text": ""}, 0

def redis(*commands):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    request = urllib.request.Request(f"{URL}/pipeline", json.dumps(commands).encode(), headers)
    return [reply["result"] for reply in json.load(urllib.request.urlopen(request, timeout=2))]

def push(people):
    global last_push
    if time.time() - last_push < 1:
        return
    last_push = time.time()
    hands = sum(1 for left_up, right_up in people if left_up or right_up)
    left = sum(left_up for left_up, right_up in people)
    right = sum(right_up for left_up, right_up in people)
    row = json.dumps({"time": last_push, "slide": live["slide"], "people": len(people),
                      "hands": hands, "left": left, "right": right})
    live["slides"][live["slide"]] = max(live["slides"].get(live["slide"], 0), hands)
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
