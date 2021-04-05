import unittest
from app.button import Button, ButtonGroup


class ButtonTestCase(unittest.TestCase):
    def test_states(self):
        button = Button()
        self.assertEqual(button.state, 'inactive')
        button.state = 'active'
        self.assertEqual(button.state, 'active')
        button.state = 'invalid state'
        self.assertEqual(button.state, 'active')


class ButtonGroupTestCase(unittest.TestCase):

    def setUp(self):
        self.button_list = [
            Button(),
            Button(),
            Button(),
            Button()
        ]
        self.button_group = ButtonGroup()
        self.button_group.mode = 'single'
        for button in self.button_list:
            self.button_group.add_button(button)

    def test_intial_state(self):
        self.button_group.reset()
        for button in self.button_list:
            self.assertEqual(button.state, 'inactive')

    def test_button_press(self):
        self.button_group.reset()
        pressed_button = self.button_list[1]
        pressed_button.press()
        for button in self.button_list:
            self.assertEqual(button.state, 'inactive')
        self.button_group.activate()
        pressed_button.press()
        self.assertEqual(pressed_button.state, 'pending')
        self.assertEqual(self.button_list[0].state, 'disabled')
        self.assertEqual(self.button_list[2].state, 'disabled')
        self.assertEqual(self.button_list[3].state, 'disabled')
        self.button_group.reset()
        for button in self.button_list:
            self.assertEqual(button.state, 'inactive')

    def test_incorrect_answer(self):
        self.button_group.reset()
        self.button_group.activate()

        self.button_list[1].press()
        self.button_group.mark_incorrect(self.button_list[0])
        self.assertEqual(self.button_list[0].state, 'disabled')
        self.assertEqual(self.button_list[1].state, 'pending')

        self.button_group.mark_incorrect(self.button_list[1])
        self.assertEqual(self.button_list[0].state, 'active')
        self.assertEqual(self.button_list[1].state, 'incorrect')
        self.assertEqual(self.button_list[2].state, 'active')
        self.assertEqual(self.button_list[3].state, 'active')

        self.button_list[1].press()
        self.assertEqual(self.button_list[0].state, 'active')
        self.assertEqual(self.button_list[1].state, 'incorrect')
        self.assertEqual(self.button_list[2].state, 'active')
        self.assertEqual(self.button_list[3].state, 'active')

        self.button_list[2].press()
        self.assertEqual(self.button_list[0].state, 'disabled')
        self.assertEqual(self.button_list[1].state, 'incorrect')
        self.assertEqual(self.button_list[2].state, 'pending')
        self.assertEqual(self.button_list[3].state, 'disabled')

        self.button_group.mark_incorrect(self.button_list[2])

        self.assertEqual(self.button_list[0].state, 'active')
        self.assertEqual(self.button_list[1].state, 'incorrect')
        self.assertEqual(self.button_list[2].state, 'incorrect')
        self.assertEqual(self.button_list[3].state, 'active')
