import os, json, time, subprocess, sys, urllib.request, streamlit as st

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

@st.cache_data(ttl=1)
def read():
    return redis("get/votes") if URL else open("votes.txt").read()

def start():
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", __file__])

if __name__ == "__main__":
    st.title("📊 Live Edge AI Voting Dashboard")
    st.session_state.setdefault("history", [])

    @st.fragment(run_every=1)
    def live_charts():
        try:
            people, hands = map(int, read().split(","))
        except Exception:
            people, hands = 0, 0
        st.session_state.history.append({"People": people, "Votes (Hands)": hands})
        c1, c2 = st.columns(2)
        c1.metric("👥 People", people)
        c2.metric("✋ Votes (Hands Up)", hands)
        st.bar_chart({"People": people, "Votes (Hands)": hands})
        st.line_chart(st.session_state.history[-30:])

    live_charts()
