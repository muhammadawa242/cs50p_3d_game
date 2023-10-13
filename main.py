from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton
from screeninfo import get_monitors
from FirstPersonCamera import FirstPersonCamera
from Player import Player
from Terrain import Terrain
from Zombie import Zombie

# loadPrcFile('config.prc')   # see gloabal config variables page, also ConfigVariableManager.getGlobalPtr().listVariables()
WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height

CAMERA_POS_Z = 50

# set fullscreen
properties = WindowProperties()
properties.setSize(WIDTH,HEIGHT)

class Game(ShowBase):
    def __init__(self):
        super(Game, ShowBase.__init__(self))
        self.win.requestProperties(properties)
        
        self.mouseLook = FirstPersonCamera(self, self.cam, CAMERA_POS_Z, self.render)
        self.mouseLook.start()
        
        Player(self)
        Terrain(self)
        zombie = Zombie(self)
        zombie.get_zombie().loop('walk')
        
        self.camera.setPos(0,0,CAMERA_POS_Z)
        

        
        
game = Game()
game.run()