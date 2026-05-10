# -*- coding: utf-8 -*-
class Event(object):
    event_list = []

    def __init__(self):
        for namespace, system_name, event_name, callback in self.event_list:
            self.ListenForEvent(namespace, system_name, event_name, self, callback)

    @classmethod
    def listen(cls, event_name, namespace='Minecraft', system_name='Engine'):
        def binding(callback):
            cls.event_list.append((namespace, system_name, event_name, callback))
            return callback
        return binding

class SubHub(object):
    subs = {}

    @classmethod
    def join(cls, topic_name):
        def binding(callback):
            cls.subs.setdefault(topic_name, []).append(callback)
            return callback
        return binding

    def publish(self, topic_name, *args, **kwargs):
        for callback in self.subs.get(topic_name, []):
            callback(*args, **kwargs)
        return

class Utils(object):
    def __init__(self):
        pass

    class cached_property(object):
        def __init__(self, method):
            self.method = method
            self.__name__ = method.__name__

        def __get__(self, instance, owner):
            if instance is None: return self
            result = self.method(instance)
            instance.__dict__[self.__name__] = result
            return result
