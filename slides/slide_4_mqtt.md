What is MQTT?
=============

- A lightweight publish/subscribe messaging protocol over TCP,
  made for small devices and unreliable networks (IoT)
- Created in 1999 at IBM and Arcom, now an OASIS standard

    publisher ──► broker ──► subscribers
      phone       laptop     presentation, dashboard

- Topic: a name like pythonid/sensor that messages are sent to
- Publishers never need to know who is listening
- QoS 0 / 1 / 2: at most once / at least once / exactly once
- Retained message: the broker keeps the last one for new subscribers
- Bridge: a local "edge" broker forwards some topics to a cloud broker,
  and keeps working when the internet is down

Here: Mosquitto on the laptop (port 1883), bridged to the free public
broker.hivemq.com; paho-mqtt is the Python client
