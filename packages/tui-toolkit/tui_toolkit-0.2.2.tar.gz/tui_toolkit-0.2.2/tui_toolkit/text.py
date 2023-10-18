from .core import Window, style_none, resized


class Text(Window):
    def __init__(
            self, term, x0, y0, width, height,
            text='', style=style_none):
        super().__init__(term, x0, y0, width, height)
        self.text = text
        self.style = style

    def render(self):
        self.print_line(0, self.style(self.text, self.width))

    def set_text(self, text):
        self.text = text
        self.render()


class TextBlock(Text):
    def __init__(
            self, term, x0, y0, width, height,
            text='', style=style_none):
        super().__init__(term, x0, y0, width, height, text, style)

    def render(self):
        i = 0
        for paragraph in self.text.split('\n'):
            line = ''
            for word in paragraph.split(' '):
                if len(line) + len(word) + 1 < self.width:
                    line = line + ' ' + word
                else:
                    self.print_line(
                            i, self.style(line, self.width))
                    i += 1
                    if i >= self.height:
                        return
                    line = word
            self.print_line(i, self.style(line, self.width))
            i += 1
            if i >= self.height:
                return


class Input(Window):
    def __init__(
            self, term, x0, y0, width, height, text='',
            style=style_none,
            style_focus=style_none,
            change_listeners=None):
        super().__init__(term, x0, y0, width, height)
        self.text = text
        self.style = style
        self.style_focus = style_focus
        self.change_listeners = ([] if change_listeners is None
                                 else change_listeners)

    def set_text(self, text):
        if self.text != text:
            for listener in self.change_listeners:
                listener(text)
            self.text = text
            self.render()

    def render(self, hasFocus=False):
        if hasFocus:
            self.print_line(
                    0,
                    self.style_focus(self.text + '▉', self.width))
        else:
            self.print_line(0, self.style(self.text, self.width))

    def interact(self, action_keys):
        with self.term.cbreak(), self.term.keypad():
            while not resized():
                self.render(True)
                k = self.term.inkey(1)
                if k.is_sequence:
                    match k.code:
                        case a if a in action_keys:
                            return a
                        case  self.term.KEY_DELETE | self.term.KEY_BACKSPACE:
                            self.set_text(self.text[:-1])
                else:
                    match k:
                        case a if a in action_keys:
                            return a
                        case c:
                            self.set_text(self.text + c)


class BlockingInput(Window):
    def __init__(self, term, x0, y0, width, height, prompt=''):
        super().__init__(term, x0, y0, width, height)
        self.prompt = prompt

    def render(self):
        pass

    def interact(self):
        self.print(0, 0, '')
        return input(self.prompt)
