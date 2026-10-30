What is Tkinter?
================

- Python's built-in GUI toolkit: import tkinter, nothing to install
- A thin layer over Tcl/Tk, a GUI toolkit first released in 1991
- Widgets: the window (Tk), labels, buttons, frames, canvases...
- pack() places widgets: side="left", "right", "top" or "bottom"
- mainloop() waits for events (keys, clicks, timers) and redraws

Threads and Tkinter:
- only the main thread may change widgets
- other threads (the mic, the webcam, MQTT) hand work back
  with root.after(0, function, arguments...)

Here: this whole presentation is one Tkinter window,
and every slide is just a file shown as text
