from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton

class Zombie(DirectObject.DirectObject):
    def __init__(self, game):
        self.game = game
        self.zombie = Actor('assets/zombie2.glb')
        self.zombie.reparentTo(game.render)
        
        print(self.zombie.getAnimNames())
        
    def get_zombie(self):
        return self.zombie