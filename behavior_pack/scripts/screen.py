# -*- coding: utf-8 -*-
import mod.client.extraClientApi as client_api
import config

from client import camera
from modules import SubHub as sub

node = client_api.GetScreenNodeCls()
bind = client_api.GetViewBinderCls()
binding = bind.binding
bind_string = bind.BF_BindString

class BaseControl(object):
    def __init__(self, node):
            self.node = node

    def bind_button(self, callback):
        button = self.node.asButton()
        text = 'SetButtonTouch{}Callback'
        button.AddTouchEventParams({'isSwallow': True})
        for binding_type in ['Down', 'Up', 'Move', 'Cancel']:
            getattr(button, text.format(binding_type))(callback)
        return

    def set_alpha(self, value):
        self.node.SetAlpha(value)
        return

class Main(node, sub):
    def __init__(self, namespace, system_name, param):
        super(Main, self).__init__(namespace, system_name, param)
        self.button_list = {name: [item[0]] for name, item in config.button_list.items()}
        self.view_rotation = [0.0, 0.0]

    @binding(bind_string, '#vought.update')
    def update(self):
        self.setup()
        def update():
            self.publish('update')
            return
        self.update = update
        return

    def setup(self):
        root = config.root_path.format
        for name, item in self.button_list.items():
            paths = (root(item[0]), root(item[0]+'/default'), root(item[0]+'/pressed'))
            item.extend([BaseControl(self.GetBaseUIControl(path)) for path in paths])
            item[1].bind_button(self.button)
        return

    def button(self, data=0):
        name = data['ButtonPath'].split('/')[-1]
        button = self.button_list[name]
        event = data['TouchEvent']
        default, pressed = [button[2], button[3]]

        is_touch = event in (1, 4) and 1.0 or 0.0
        [default.set_alpha(1.0 - is_touch), pressed.set_alpha(is_touch)]

        panning = (event == 4)
        point = [data['TouchPosX'], data['TouchPosY']]
        panning and (self.view_rotation[0] or self.view_rotation[1])

        yaw = (point[0] - self.view_rotation[1]) * 0.5
        pitch = (self.view_rotation[0] - point[1]) * -0.5
        x, y, z = camera.get_rotation()
        panning and camera.set_rotation((x + pitch, y + yaw, 0))
        is_touch and setattr(self, 'view_rotation', [point[1], point[0]])

        data = {'name': name, 'is_touch': is_touch}
        self.publish('button', data)
        return
