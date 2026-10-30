import time, tkinter as tk

PLAN = {"slide_0_1_bio.md": 0, "slide_18_community.md": 12, "slide_20_edgeprompt.md": 22,
        "slide_22_toolkit.md": 35}
TOTAL = 45 * 60
clock = lambda seconds: f"{int(seconds) // 60}:{int(seconds) % 60:02d}"

def start(panel, slides, current):
    names = [path.name for path in slides]
    marks = sorted((names.index(name), minutes * 60) for name, minutes in PLAN.items())
    marks.append((len(names), TOTAL))
    label = tk.Label(panel, font=("Consolas", 11))
    label.pack()
    state = {"start": time.time(), "slide": current(), "since": time.time()}

    def planned(i):
        for (a, at), (b, bt) in zip(marks, marks[1:]):
            if a <= i < b:
                return at + (i - a) / (b - a) * (bt - at)

    def tick():
        now = time.time()
        if current() != state["slide"]:
            state["slide"], state["since"] = current(), now
        elapsed = now - state["start"]
        late = elapsed - planned(state["slide"])
        pace = f"{clock(abs(late))} {'behind' if late > 0 else 'ahead'}"
        text = f"⏱ {clock(elapsed)} / {clock(TOTAL)} · slide {clock(now - state['since'])}"
        text += f"\n{pace} · {clock(max(TOTAL - elapsed, 0))} left"
        label.config(text=text, fg="red" if late > 60 else "gray")
        panel.after(1000, tick)

    panel.bind_all("<t>", lambda event: state.update(start=time.time()))
    tick()
