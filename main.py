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
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionRay, CollisionHandlerQueue
import random

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
        
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.rayqueue = CollisionHandlerQueue()
        
        self.ray_node = CollisionNode('ray')
        self.ray = CollisionRay()
        self.ray_node.addSolid(self.ray)
        self.ray_np = self.cam.attachNewNode(self.ray_node)
        
        self.ray_np.node().setFromCollideMask(0x10)
        self.ray_np.setCollideMask(0x1)
        
        Player(self)
        Terrain(self)
        
        self.cTrav.addCollider(self.ray_np, self.rayqueue)
        self.ray_np.show()
        
        flinches = ['laflinch', 'rlflinch', 'llflinch', 'raflinch', 'flinchsmall', 'bigflinch']
        for i in range(6):
            z = Zombie(self, i, random.choice(flinches))
            name = 'zombie'+str(i)
            colliderNode = CollisionNode(name)
            self.zombie = z.get_zombie()
            
            colliderNode.addSolid(CollisionSphere(0, 0, 40, 30))
            colliderNode.setFromCollideMask(0x10)
            collider = self.zombie.attachNewNode(colliderNode)
            collider.setCollideMask(0x10)
            collider.setPythonTag(name, z)
            self.cTrav.addCollider(collider, self.pusher)
            self.pusher.addCollider(collider, self.zombie)
            # collider.show()
        
        self.camera.setPos(0,0,CAMERA_POS_Z)
        

        
        
game = Game()
game.run()