from time import monotonic

from textual.app import App
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static, Button


class TimeDisplay(Static):
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self):
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self):
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time):
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f'{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}')

    def start(self):
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self):
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self):
        self.total = 0
        self.time = 0


class Stopwatch(Static):
    def compose(self):
        yield Button('Start', id='start', variant='success')
        yield Button('Stop', id='stop', variant='error')
        yield Button('Reset', id='reset')
        yield TimeDisplay()

    def on_button_pressed(self, event):
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == 'start':
            time_display.start()
            self.add_class('started')
        elif button_id == 'stop':
            time_display.stop()
            self.remove_class('started')
        elif button_id == 'reset':
            time_display.reset()


class StopwatchApp(App):
    CSS_PATH = 'stopwatch.tcss'
    BINDINGS = [
        ('d', 'toggle_dark', 'Toggle dark mode'),
        ('a', 'add_stopwatch', 'Add'),
        ('r', 'remove_stopwatch', 'Remove'),
    ]

    def compose(self):
        yield Header()
        yield Footer()
        yield ScrollableContainer(Stopwatch(), Stopwatch(), Stopwatch(), id='timers')

    def action_toggle_dark(self):
        self.dark = not self.dark

    def action_add_stopwatch(self):
        new_stopwatch = Stopwatch()
        self.query_one('#timers').mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self):
        timers = self.query('Stopwatch')
        if timers:
            timers.last().remove()


def main():
    app = StopwatchApp()
    app.run()


if __name__ == '__main__':
    main()
