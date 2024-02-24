from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton, Vec3
from screeninfo import get_monitors
from fps_terrain import FpsCamera
from Player import Player
from House import House
# from Terrain import Terrain
from Zombie import Zombie
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionRay, CollisionHandlerQueue
from panda3d.core import TextureStage, TexGenAttrib, Texture, LoaderOptions, TexturePool, Fog, AmbientLight
from panda3d.bullet import BulletBoxShape, BulletWorld, BulletRigidBodyNode, BulletPlaneShape
from direct.showbase.Loader import Loader
import random
import sys


loadPrcFile('config.prc')   # see gloabal config variables page, also ConfigVariableManager.getGlobalPtr().listVariables()
WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height

# set fullscreen
properties = WindowProperties()
properties.setSize(WIDTH,HEIGHT)

class Game(ShowBase):
    def __init__(self):
        super(Game, ShowBase.__init__(self))
        
        # set lightning to avoid reflection from walls
        ambient = AmbientLight("ambient")
        ambient.set_color((.5, .5, .5, 0))
        ambient_np = base.render.attach_new_node(ambient)
        base.render.set_light(ambient_np)

        # house
        house_file = '../side track/console_game/blender_files/house_no_doors_metallic.glb'
        house_scale = 3
        house = House(house_file, house_scale)
        
        # bullet world for physics
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.attach(house.get_bullet_node()) # also do this for player node
        
        self.taskMgr.add(self.update, 'update')
        
        # Player load and movement
        self.taskMgr.add(self.move, "moveTask")
        self._loadPlayer()
        
        self.win.requestProperties(properties)
        
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.rayqueue = CollisionHandlerQueue()
        
        self.ray_node = CollisionNode('ray')
        self.ray = CollisionRay()
        self.ray_node.addSolid(self.ray)
        self.ray_np = self.cam.attachNewNode(self.ray_node)
        
        self.ray_np.node().setFromCollideMask(0x10)
        self.ray_np.setCollideMask(0x1)
        
        # Player(self)
        # t = Terrain(self)
        
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
        

    def _loadPlayer(self):
        # Create the main character
        self.player = Player(self).gun
        
        # fps camera
        self.camera = FpsCamera(self.player)

        self.mouseInvertY = False
        
    
    def move(self, task):
        # use the mouse to look around and set player's direction
        md = base.win.getPointer(0)
        deltaX = md.getX() -200
        deltaY = md.getY() -200
        if self.mouseInvertY:
            deltaY *= -1
            
        if base.win.movePointer(0, 200, 200):
            self.camera.update(deltaX, deltaY)

        return Task.cont
    
    def update(self, task):
        dt = globalClock.getDt()
        
        self.world.doPhysics(dt)
        
        return task.cont
    
game = Game()
game.run()