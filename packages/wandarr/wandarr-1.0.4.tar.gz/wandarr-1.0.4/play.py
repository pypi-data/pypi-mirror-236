
import time
from threading import Thread

from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel

layout = Layout(name="root")
layout.split_column(
    Layout(name="log"),
    Layout(name="main"),
)

m = Table("main stuff")
logs = Table("output")
layout["log"].update(Panel(logs))
layout["main"].update(Panel(m))

class Feeder(Thread):
    def __init__(self, live, logs, m):
        super().__init__(daemon=True)
        self.live = live
        self.logs = logs
        self.m = m

    def run(self):
        for _ in range(30):
            self.logs.add_row("hello, world")
            self.m.add_row("hello, again")
            self.live.update(layout, refresh=True)
            time.sleep(1)


with Live(screen=False, auto_refresh=False) as live:
    t = Feeder(live, logs, m)
    t.start()
    t.join()

