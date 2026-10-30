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

Here: open http://<laptop-ip>:8501 on your phone
