import subprocess, sys, pandas as pd, streamlit as st, presentation_redis

def start():
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", __file__])

if __name__ == "__main__":
    st.title("📊 Live Edge AI Voting Dashboard")
    read = st.cache_data(ttl=1)(presentation_redis.read)

    @st.fragment(run_every=1)
    def live_charts():
        try:
            rows, live = read()
            df, now = pd.DataFrame(rows), rows[-1]
        except Exception:
            return st.info("⏳ Waiting for votes...")
        slide = df[df.slide == now["slide"]]
        df.t, approval = pd.to_datetime(df.t, unit="s"), now["hands"] / max(now["people"], 1)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👥 People", now["people"], f"record {df.people.max()}", delta_color="off")
        c2.metric("✋ Votes", now["hands"], f"record {df.hands.max()}", delta_color="off")
        c3.metric("👍 Approval", f"{approval:.0%}")
        c4.metric("⏱ Reaction", f"{slide.t[slide.hands.idxmax()] - slide.t.min():.0f}s")
        st.progress(min(approval, 1.0))
        st.area_chart(df.set_index("t")[["people", "hands"]], x_label="Time", y_label="Energy")
        a, b = st.columns(2)
        a.bar_chart(pd.DataFrame([{"✋ Up": now["hands"], "🙅 Down": now["people"] - now["hands"]}], index=["Room"]), horizontal=True)
        b.bar_chart({"⬅ Left hand": now["left"], "Right hand ➡": now["right"]}, y_label="Hands", sort=False)
        st.bar_chart(pd.Series(live["slides"], dtype=int), x_label="Slide", y_label="Most hands")
        st.bar_chart(pd.Series(dict(live["words"]), dtype=int), horizontal=True, x_label="Times spoken", sort=False)

    live_charts()
