import signal
from blessed import Terminal


_resized = False


def on_resized(*args):
    global _resized
    _resized = True


def trap_resized():
    signal.signal(signal.SIGWINCH, on_resized)


def reset_resized():
    global _resized
    _resized = False


def resized():
    return _resized


class App:
    def __init__(self, initial_loop):
        self.terminal_resized = False
        self.term = Terminal()
        self.initial_loop = initial_loop
        signal.signal(signal.SIGWINCH, self.on_terminal_resized)

    def initialise(self):
        raise NotImplementedError

    def layout(self):
        raise NotImplementedError

    def on_terminal_resized(self, *args):
        self.terminal_resized = True
        on_resized()

    def run(self):
        self.initialise()
        loop = self.initial_loop
        with self.term.fullscreen():
            self.layout()
            while loop:
                if self.terminal_resized:
                    self.layout()
                    self.terminal_resized = False
                    reset_resized()
                loop = loop()


class Window:
    def __init__(self, term, x0, y0, width, height):
        self.term = term
        self.width_ = min(width, term.width - x0)
        self.height_ = min(height, term.height - y0)
        self.x0_ = x0  # TODO: exception if outside screen?
        self.y0_ = y0

    @property
    def width(self):
        return self.width_

    @property
    def height(self):
        return self.height_

    @property
    def x0(self):
        return self.x0_

    @property
    def y0(self):
        return self.y0_

    def resize(self, x0=None, y0=None, width=None, height=None):
        if x0 is not None:
            self.x0_ = x0
            self.width_ = min(self.width, self.term.width - self.x0)
        if y0 is not None:
            self.y0_ = y0
            self.height_ = min(self.height, self.term.height - self.y0)
        if width is not None:
            self.width_ = min(width, self.term.width - self.x0)
        if height is not None:
            self.height_ = min(height, self.term.height - self.y0)

    def print_line(self, y, text, end='\r'):
        self.print(0, y, self.term.ljust(text, self.width), end=end)

    def print(self, x, y, text, end='\r'):
        if x < self.width and y < self.height:
            x_ = x + self.x0
            y_ = y + self.y0
            print(
                    self.term.move_xy(x_, y_)
                    + self.term.truncate(text, self.width - x),
                    end=end)


def style_none(text, width):
    return text
