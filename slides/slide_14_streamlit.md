What is Streamlit?
==================

- A Python library that turns a script into a web app:
  st.metric, st.area_chart, st.image... no HTML or JavaScript
- The script reruns from the top whenever something changes;
  @st.fragment(run_every=1) reruns one part every second
- @st.cache_resource keeps one object, our MQTT subscriber,
  shared by every viewer

From raw events to a dashboard:
- publish: YOLO sends a message on every camera frame
- subscribe: keep 1 row per second for 10 minutes (600 rows)
- dashboard: people, votes and approval, their trend, a word cloud

Streamlit Community Cloud hosts it for free, straight from GitHub.
It reads the data from the public MQTT broker on the internet.

Here: open https://pythonid-10-2026.streamlit.app on your phone
