class Button:
    states = {'inactive', 'active', 'disabled', 'correct', 'incorrect', 'pending'}

    def __init__(self):
        self._state = 'inactive'
        self.contestant = None
        self.group = None
        self.time = 0.0

    def press(self):
        if self.state == 'active':
            if self.group is not None:
                self.group.register_press(self)

    def reset(self):
        self.state = 'inactive'
        self.time = 0.0

    def activate(self):
        if self.state == 'inactive':
            self.state = 'active'

    def enable(self):
        if self.state == 'disabled':
            self.state = 'active'

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state in Button.states:
            self._state = state


class ButtonGroup:

    def __init__(self):
        self.button_list = []
        self.mode = 'single'

    def add_button(self, button):
        if button not in self.button_list:
            self.button_list.append(button)
            button.group = self

    def register_press(self, button):
        if button not in self.button_list:
            return
        if button.state == 'active':
            if self.mode == 'single':
                button.state = 'pending'
                for other_button in self.button_list:
                    if other_button == button:
                        continue
                    if other_button.state == 'active':
                        other_button.state = 'disabled'
            elif self.mode == 'timer':
                button.state = 'pending'
                button.time = 1.0

    def reset(self):
        for button in self.button_list:
            button.reset()

    def activate(self):
        for button in self.button_list:
            button.activate()

    def mark_incorrect(self, button):
        if button not in self.button_list:
            return
        if button.state == 'pending':
            button.state = 'incorrect'
            for other_button in self.button_list:
                if other_button.state == 'disabled':
                    other_button.enable()
