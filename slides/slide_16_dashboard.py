import pandas as pd, streamlit as st, slide_15_subscribe as subscribe
from wordcloud import WordCloud

if __name__ == "__main__":
    @st.fragment(run_every=1)
    def live_charts():
        data = subscribe.live()
        if not data["history"]:
            return st.info("⏳ Waiting for votes...")
        history = pd.DataFrame(list(data["history"]))
        latest = history.iloc[-1]
        approval = latest["hands"] / max(latest["people"], 1)
        c1, c2, c3 = st.columns(3)
        c1.metric("👥 People", latest["people"], f"record {history.people.max()}")
        c2.metric("✋ Votes", latest["hands"], f"record {history.hands.max()}")
        c3.metric("👍 Approval", f"{approval:.0%}")
        st.area_chart(history.set_index("time")[["people", "hands"]])
        cloud = WordCloud(width=800, height=300, background_color="white")
        if words := cloud.process_text(data["text"]):
            st.image(cloud.generate_from_frequencies(words).to_image())

    live_charts()
