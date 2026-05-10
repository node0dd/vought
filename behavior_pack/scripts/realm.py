# -*- coding: utf-8 -*-
from server import system

from modules import SubHub as sub

context = []
player_list = {}

def main():
    context[0].local_method('update', player_list)
    player_list.clear()
    return

@sub.join('realm:update')
def update(id, data):
    player_list[id] = data
    return
print(0)
system.run(main)
