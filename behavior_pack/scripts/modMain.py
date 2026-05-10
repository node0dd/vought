# -*- coding: utf-8 -*-
from mod.common.mod import Mod
import mod.server.extraServerApi as server_api
import mod.client.extraClientApi as client_api

import config

@Mod.Binding(name=config.pack_name, version='1.0.0')
class nodeMod(object):
    def __init__(self):
        pass

    @Mod.InitServer()
    def register_server(self):
        server_api.RegisterSystem(config.pack_name, config.system_name, config.server_path)
        return

    @Mod.DestroyServer()
    def destroy_server(self):
        pass

    @Mod.InitClient()
    def register_client(self):
        client_api.RegisterSystem(config.pack_name, config.system_name, config.client_path)
        return

    @Mod.DestroyClient()
    def destroy_client(self):
        pass
