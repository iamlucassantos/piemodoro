"""Module that implements the Pomodoro timer."""
import time


class Pomo:
    """Pomodoro timer class."""

    def __init__(self,
                 pomodoro: int = 25,
                 short_break: int = 5,
                 long_break: int = 15,
                 long_break_interval: int = 4):
        """Initialize the Pomodoro timer.

        Args:
            pomodoro: Length of a pomodoro in minutes.
            short_break: Length of a short break in minutes.
            long_break: Length of a long break in minutes.
            long_break_interval: Number of pomodoros before a long break.
            """
        self.pomodoro = pomodoro
        self.short_break = short_break
        self.long_break = long_break
        self.long_break_interval = long_break_interval
        self.pomodoro_count = 0
        self.long_break_count = 0
        self.short_break_count = 0
        self.time_left = pomodoro * 60
        self.state = 'pomodoro'
        self.timer = None

    states_to_name = {
        "pomodoro": "Pomodoro",
        "short_break": "Short break",
        "long_break": "Long break",
        "stopped": "Stopped"
    }

    def switch(self):
        """Switch between pomodoro and break."""
        next_state = 'pomodoro'
        if self.state == 'pomodoro':
            self.pomodoro_count += 1
            next_state = 'long_break' if self.pomodoro_count % self.long_break_interval == 0 else 'short_break'
        elif self.state == "long_break":
            self.long_break_count += 1
        else:
            self.short_break_count += 1

        self.time_left = self.get_state_length(next_state) * 60
        self.state = next_state

    def tick(self):
        """Tick the timer."""
        time.sleep(1)
        self.time_left -= 1

    def run(self):
        """Run the timer."""
        while self.time_left > 0:
            self.tick()

    def get_state_length(self, state: str):
        """Return the length of a state"""
        return getattr(self, state)

    def name(self):
        """Return the name of the current state."""
        return self.states_to_name[self.state]

    def __str__(self):
        """Return the string representation of the timer."""
        return f"{self.name()}: {self.time_left} minutes"

    def emoji(self):
        """Return the emoji representation of the timer."""
        pomodoro_sets_complete = self.pomodoro_count // self.long_break_interval
        pomodoros_complete = self.pomodoro_count % self.long_break_interval
        return ':pie:' * pomodoro_sets_complete + ':tomato:' * pomodoros_complete
