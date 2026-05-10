# -*- coding: utf-8 -*-
import mod.server.extraServerApi as server_api
import config

from modules import Event as event
from modules import SubHub as sub
from modules import Utils as utils

LEVEL_ID = server_api.GetLevelId()

listen = event.listen
server_system = server_api.GetServerSystemCls()
factory = server_api.GetEngineCompFactory()

class BaseSystem(object):
    def __init__(self):
        pass

    @utils.cached_property
    def comp(self):
        return factory.CreateGame(LEVEL_ID)

    def run(self, func, delay=0.05):
        self.comp.AddRepeatedTimer(delay, func)
        return

system = BaseSystem()

class Main(server_system, event, sub):
    def __init__(self, namespace, system_name):
        super(Main, self).__init__(namespace, system_name)
        event.__init__(self)

    @listen('MethodExecutor', config.pack_name, config.system_name)
    def method_executor(self, data):
        getattr(self, data['method'])(*(data.get('data') or ()))
        return

    def local_method(self, method, *data):
        event_data = {'method': method, 'data': data or ()}
        self.BroadcastToAllClient('MethodExecutor', event_data)
        return

    def setup(self):
        import realm
        realm.context.append(self)
        return

    def update(self, id, data):
        self.publish('realm:update', id, data)
        return
