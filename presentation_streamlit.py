import subprocess, sys, streamlit as st, presentation_redis

def start():
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", __file__])

if __name__ == "__main__":
    st.title("📊 Live Edge AI Voting Dashboard")
    st.session_state.setdefault("history", [])
    read = st.cache_data(ttl=1)(presentation_redis.read)

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
