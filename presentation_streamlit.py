import subprocess, sys, pandas as pd, streamlit as st, presentation_redis
from wordcloud import WordCloud

def start():
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", __file__])

if __name__ == "__main__":
    st.title("📊 Live Edge AI Voting Dashboard")
    read = st.cache_data(ttl=1)(presentation_redis.read)

    @st.fragment(run_every=1)
    def live_charts():
        try:
            rows, live = read()
            history, latest = pd.DataFrame(rows), rows[-1]
        except Exception:
            return st.info("⏳ Waiting for votes...")
        this_slide = history[history.slide == latest["slide"]]
        reaction = this_slide["time"][this_slide.hands.idxmax()] - this_slide["time"].min()  # seconds
        history["time"] = pd.to_datetime(history["time"], unit="s")
        approval = latest["hands"] / max(latest["people"], 1)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👥 People", latest["people"], f"record {history.people.max()}", delta_color="off")
        c2.metric("✋ Votes", latest["hands"], f"record {history.hands.max()}", delta_color="off")
        c3.metric("👍 Approval", f"{approval:.0%}")
        c4.metric("⏱ Reaction", f"{reaction:.0f}s")
        st.progress(min(approval, 1.0))
        st.area_chart(history.set_index("time")[["people", "hands"]], x_label="Time", y_label="Energy")
        room = {"✋ Up": latest["hands"], "🙅 Down": latest["people"] - latest["hands"]}
        st.bar_chart(pd.DataFrame([room], index=["Room"]), horizontal=True)
        st.bar_chart(pd.Series(live["slides"], dtype=int), x_label="Slide", y_label="Most hands")
        cloud = WordCloud(width=800, height=300, background_color="white")
        if words := cloud.process_text(live["text"]):
            st.image(cloud.generate_from_frequencies(words).to_image())

    live_charts()
