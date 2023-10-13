from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton

class Terrain(DirectObject.DirectObject):
    def __init__(self, game):
        self.game = game
        
        self.env = self.game.loader.loadModel('assets/grass.glb')
        self.env.setPos(0,50,-10)
        self.env.reparentTo(self.game.render)