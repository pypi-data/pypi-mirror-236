from tabulate import tabulate
from itertools import count
from .list import List
from .text import Text
from .core import style_none


class Table(List):
    def __init__(
            self, term, x0, y0, width, height,
            style=style_none,
            style_focus=None,
            contents=None, formatter=None, focus_listeners=None):
        super().__init__(
                term, x0, y0, width, height,
                style=style,
                style_focus=style_focus,
                contents=contents,
                formatter=formatter,
                focus_listeners=focus_listeners)

    def formatted_rows(self):
        return [self.formatter(item) for item in self.contents]

    def render(self):
        self._render(tabulate(self.formatted_rows()).split('\n')[1:-1])

    def _render(self, rows):
        offset = 0
        if self.focus_index is not None:
            offset = max(0, self.focus_index - self.height + 2)
        i = -1
        for i, row in zip(count(), rows[offset:]):
            row = self.term.ljust(row)
            if i + offset == self.focus_index:
                row = self.style_focus(row, self.width)
            self.print_line(i, self.style(row, self.width))
        i += 1
        while i < self.height:
            self.print_line(i, self.style(' ' * self.width, self.width))
            i += 1
        if offset:
            self.print(self.width - 1, 0, self.style('▲', 1))
        if len(self.contents) - offset > self.height:
            self.print(self.width - 1, self.height - 1, self.style('▼', 1))


class HeadedTable:
    def __init__(
            self, term, x0, y0, width, height, headers,
            style=style_none,
            style_headers=style_none,
            style_focus=None,
            contents=None, formatter=None, focus_listeners=None):
        self.table = Table(
                term, x0, y0 + 1, width, height - 1,
                contents=contents,
                formatter=formatter,
                style=style,
                style_focus=style_focus,
                focus_listeners=focus_listeners)
        self.header = Text(term, x0, y0, width, 1, style=style_headers)
        self.headers = headers
        self.term = term

    def resize(self, x0=None, y0=None, width=None, height=None):
        self.table.resize(
                x0, None if y0 is None else y0 + 1,
                width, None if height is None else height - 1)
        self.header.resize(x0, y0, width)

    def render(self):
        rows = tabulate(
                self.table.formatted_rows(),
                headers=self.headers).split('\n')
        self.header.set_text(rows[0])
        self.header.render()
        self.table._render(rows[2:])

    def set_contents(self, contents):
        self.table.set_contents(contents)

    @property
    def focus_index(self):
        return self.table.focus_index

    def set_focus_index(self, index, force_notify=False):
        self.table.set_focus_index(index, force_notify)

    def focus_item(self):
        return self.table.focus_item()
