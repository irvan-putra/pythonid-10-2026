MQTT vs CoAP: two ways to talk IoT
==================================

                MQTT                        CoAP (IETF, 2014)
  Model         publish/subscribe           request/response, like HTTP
  Transport     TCP                         UDP: tiny headers
  Middleman     always a broker             none: the sensor is a server
  "On change"   subscribe to a topic        the Observe option
  Security      TLS                         DTLS (TLS for UDP)

Pick MQTT when many receivers need the same data, through a broker
that can also reach the cloud: phones, gateways, dashboards.

Pick CoAP for tiny battery-powered sensors on weak networks, talking
directly to each other: coap://sensor/temperature

This talk uses MQTT: one phone, many receivers, and a free public
broker for the online dashboard.
