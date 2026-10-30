import slide_1_whisper as whisper, slide_2_yolo as yolo, slide_5_mqtt as mqtt

laptop_show, laptop_update, transcript = whisper.show, yolo.update, []

def show(subtitle, text):
    laptop_show(subtitle, text)
    transcript.append(text)
    mqtt.publish("speech", " ".join(transcript), retain=True)  # retained: late subscribers get it

def update(video, image, people, hands):
    laptop_update(video, image, people, hands)
    mqtt.publish("votes", {"people": people, "hands": hands})

whisper.show, yolo.update = show, update
