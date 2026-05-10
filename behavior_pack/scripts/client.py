# -*- coding: utf-8 -*-
import mod.client.extraClientApi as client_api
import config

from modules import Event as event
from modules import SubHub as sub
from modules import Utils as utils

LEVEL_ID = client_api.GetLevelId()

listen = event.listen
client_system = client_api.GetClientSystemCls()
factory = client_api.GetEngineCompFactory()

class BaseSystem(object):
    def __init__(self):
        pass

    @utils.cached_property
    def comp(self):
        return factory.CreateGame(LEVEL_ID)

    @property
    def delta_time(self):
        delta_time = 1.0 / self.comp.GetFps()
        return delta_time

    @property
    def screen_size(self):
        width, height = self.comp.GetScreenSize()
        return [width, height]

    def run(self, func, delay=0.05):
        self.comp.AddRepeatedTimer(delay, func)
        return

system = BaseSystem()

class BaseWorld(object):
    def __init__(self):
        pass

    @utils.cached_property
    def particle(self):
        comp = factory.CreateParticleSystem(None)
        return comp

    def get_local_player(self):
        return BasePlayer(client_api.GetLocalPlayerId())

    def create_particle(self, name, position):
        self.particle.Create(name, position, (0, 0, 0))
        return

world = BaseWorld()

class Post(object):
    def __init__(self, name):
        self.name = name
        self.post = factory.CreatePostProcess(LEVEL_ID)
        self.post.SetEnableByName(self.name, True)

    def set_parameter(self, param, value):
        self.post.SetParameter(self.name, param, value)
        return

class BaseCamera(object):
    def __init__(self):
        self.camera = factory.CreateCamera(LEVEL_ID)

    def get_rotation(self):
        x, y, z = self.camera.GetCameraRotation()
        return x, y, z

    def set_offset(self, offset):
        self.camera.SetCameraOffset(offset)
        return

    def set_rotation(self, vector3):
        self.camera.SetCameraRotation(vector3)
        return

camera = BaseCamera()

class BaseEntity(object):
    def __init__(self, entity_id):
        self.id = entity_id

    @utils.cached_property
    def rotation(self):
        comp = factory.CreateRot(self.id)
        return comp

    @utils.cached_property
    def molang(self):
        comp = factory.CreateQueryVariable(self.id)
        return comp

    @utils.cached_property
    def resource(self):
        comp = factory.CreateActorRender(self.id)
        return comp

    @property
    def get_rotation(self):
        x, y = self.rotation.GetRot()
        return x, y

    def variable(self, molang=''):
        value = self.molang.EvalMolangExpression(molang)['value']
        return value

class BasePlayer(BaseEntity):
    def __init__(self, player_id):
        super(BasePlayer, self).__init__(player_id)

    def replace_model(self, geometry):
        self.resource.AddPlayerGeometry('default', geometry)
        self.resource.RebuildPlayerRender()
        return

class Main(client_system, event, sub):
    def __init__(self, namespace, system_name):
        super(Main, self).__init__(namespace, system_name)
        event.__init__(self)
        self.loaded = []
        self.player_list = {}
        self.local_player_id = 0

    @listen('UiInitFinished')
    def setup(self, data=[]):
        import main
        main.context.append(self)
        self.local_player_id = main.player.id

        self.server_method('setup')
        self.loaded.append(1.0)
        client_api.RegisterUI(config.pack_name, config.screen_name, config.screen_path, config.screen_name)
        client_api.CreateUI(config.pack_name, config.screen_name, {'isHud': 1})
        return

    @listen('MethodExecutor', config.pack_name, config.system_name)
    def method_executor(self, data):
        getattr(self, data['method'])(*(data.get('data') or ()))
        return

    def server_method(self, method, *data):
        event_data = {'method': method, 'data': data or ()}
        self.NotifyToServer('MethodExecutor', event_data)
        return

    def update(self, data):
        if not self.loaded: return
        for id, value in data.iteritems():
            if id == self.local_player_id: continue
            player = self.player_list.get(id) or { 'self': BasePlayer(id) }
            self.player_list[id] = player
            player['self'].variable(value)
        return
