Changing a running program: monkeypatching
==========================================

In Python, a module's functions and objects are just names,
so another module can replace them while the program runs:

    import slide_1_whisper as whisper
    laptop_record = whisper.record    # keep the original
    whisper.record = record           # use ours from now on

listen() looks up record() every time it calls it,
so it starts using the phone without changing slide 1.

Duck typing: "if it walks like a duck and quacks like a duck..."
YOLO only calls webcam.isOpened() and webcam.read(),
so any object with those two methods can be its camera (slide 12).
