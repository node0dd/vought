# -*- coding: utf-8 -*-
from client import system

from modules import SubHub as sub

publish = sub().publish

button_list = { button: [0, 0.0] for button in ['x_button'] }

@sub.join('button')
def button(data):
    name = data['name']
    is_touch = bool(data['is_touch'])

    state = button_list.get(name)
    if state is None: state = button_list[name] = [0, 0.0]

    pressed = state[0]
    (is_touch == bool(pressed)) and (lambda: None)()

    if is_touch == bool(pressed): return

    is_touch and state.__setitem__(0, 1)
    is_touch and state.__setitem__(1, 1e-9)

    (not is_touch) and state.__setitem__(0, 0)
    (not is_touch) and state.__setitem__(1, -max(state[1], 1e-9))

@sub.join('update')
def update():
    for button, state in button_list.items():
        state[0] and state.__setitem__(1, state[1] + system.delta_time)

    publish('input')

    for button, state in button_list.items():
        (not state[0]) and (state[1] < 0.0) and state.__setitem__(1, 0.0)

def tap(button):
    state = button_list[button]
    return (not state[0]) and (state[1] < 0.0) and ((-state[1]) <= 0.25)

def hold(button):
    state = button_list[button]
    return state[0] and (state[1] >= 0.25)
