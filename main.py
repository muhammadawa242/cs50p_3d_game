from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile
from screeninfo import get_monitors
from FirstPersonCamera import FirstPersonCamera

loadPrcFile('config.prc')   # see gloabal config variables page, also ConfigVariableManager.getGlobalPtr().listVariables()
WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height

# set fullscreen
properties = WindowProperties()
properties.setSize(WIDTH,HEIGHT)

class Game(ShowBase):
    def __init__(self):
        super(Game, ShowBase.__init__(self))
        self.win.requestProperties(properties)
        
        self.env = self.loader.loadModel('assets/grass.glb')
        self.env.setPos(0,50,-10)
        self.env.reparentTo(self.render)
        
        self.mouseLook = FirstPersonCamera(self, self.cam, self.render)
        self.mouseLook.start()
        
        
game = Game()
game.run()