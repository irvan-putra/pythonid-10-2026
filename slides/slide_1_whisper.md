What is Whisper?
================

- A speech-to-text model by OpenAI, open source (MIT licence, 2022)
- Trained on 680,000 hours of audio in many languages
- A Transformer: audio goes in, text comes out
- Sizes from tiny (39M parameters) to large (1.5B)

This talk uses faster-whisper:
- the same model, re-implemented on CTranslate2 for speed
- tiny.en: the smallest model, English only
- int8: weights stored as 8-bit integers instead of 32-bit floats,
  about 4x smaller, fast enough for a laptop CPU

Here: 2 seconds of mic audio -> text -> "next" / "back" changes the slide
