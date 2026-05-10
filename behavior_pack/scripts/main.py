# -*- coding: utf-8 -*-
from client import system, world
from client import Post

from modules import SubHub as sub
from input import tap, hold

context = []
player_list = []
player = world.get_local_player()

def main():
    return

@sub.join('update')
def update():
    return

@sub.join('input')
def input():
    return

system.run(main)
