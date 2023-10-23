"""
Copyright (c) 2023 Himank Deka & Contributers [See CONTRIBUTERS.txt]
"""
"""
This file contains the Playground class which is the most important thing in the game.
"""
from pytextgame.components import dat
from pytextgame.components.compartments import Room, Door


class Playground :
    def __init__(self, name: str, id = 0) :
        self.id = id
        self.name = name
        self.entry = None
        
        if dat.SHOW_WELCOME_BOX :
            from . import pytextgame_w
            
        else :
            pass
        
    def activate(self, comps) :
        self.compartments = comps
        
    def create_entry_doors(self, dir_en, dir_ex, ex_lock) :
        self.entry_default = Door(self.entry, 'entry-door', dir_en, False)
        self.exit_default = Door(self.entry, 'exit-door', dir_ex, ex_lock)
        
    def create_start(self, objs) :
        self.start = Room(self, 'Start', [self.entry_default, self.exit_default], objs, self.exit_default.direction)
        
        
    

