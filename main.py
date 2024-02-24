from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton, Vec3
from screeninfo import get_monitors
from fps_terrain import FpsCamera
from Player import Player
# from Terrain import Terrain
from Zombie import Zombie
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionRay, CollisionHandlerQueue
from panda3d.core import TextureStage, TexGenAttrib, Texture, LoaderOptions, TexturePool, Fog
from panda3d.bullet import BulletBoxShape, BulletWorld, BulletRigidBodyNode
from direct.showbase.Loader import Loader
import random
import sys

sys.path.insert(1, 'Panda_3d_Procedural_Terrain_Engine/src')
from config import *
from Panda_3d_Procedural_Terrain_Engine.src.sky import Sky
from Panda_3d_Procedural_Terrain_Engine.src.basicfunctions import getMouseLook

loadPrcFile('config.prc')   # see gloabal config variables page, also ConfigVariableManager.getGlobalPtr().listVariables()
WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height

# set fullscreen
properties = WindowProperties()
properties.setSize(WIDTH,HEIGHT)

class Game(ShowBase):
    def __init__(self):
        super(Game, ShowBase.__init__(self))
        from Panda_3d_Procedural_Terrain_Engine.src.terrain import Terrain, TerrainPopulator
        from Panda_3d_Procedural_Terrain_Engine.src.populator import makeTree
        
        # debug bullet code
        from panda3d.bullet import BulletDebugNode
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = render.attachNewNode(debugNode)
        debugNP.show()
        
        
        # Sky configuration
        self.sky = Sky(None)
        self.sky.setTime(1700.0)
        self.sky.start()
        self.sky.paused= True
        
        # bullet world for physics
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        # self.world.setDebugNode(debugNP.node()) #debug bullet code 2
        
        self.taskMgr.add(self.update, 'update')
        
        # populate terrain with trees and stuff
        populator = TerrainPopulator()
        populator.addObject(makeTree, {}, 5)

        if SAVED_HEIGHT_MAPS:
            seed = 666
        else:
            seed = 0
        self.terrain = Terrain('Terrain', base.cam, MAX_VIEW_RANGE, populator, feedBackString=None, id=seed)
        self.terrain.reparentTo(self.render)
        
        # Player load and movement
        self.prevtime = 0
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
        
        # flinches = ['laflinch', 'rlflinch', 'llflinch', 'raflinch', 'flinchsmall', 'bigflinch']
        # for i in range(6):
        #     z = Zombie(self, i, random.choice(flinches))
        #     name = 'zombie'+str(i)
        #     colliderNode = CollisionNode(name)
        #     self.zombie = z.get_zombie()
            
        #     colliderNode.addSolid(CollisionSphere(0, 0, 40, 30))
        #     colliderNode.setFromCollideMask(0x10)
        #     collider = self.zombie.attachNewNode(colliderNode)
        #     collider.setCollideMask(0x10)
        #     collider.setPythonTag(name, z)
        #     self.cTrav.addCollider(collider, self.pusher)
        #     self.pusher.addCollider(collider, self.zombie)
        #     # collider.show()
        

    def _loadPlayer(self):
        # Create the main character
        # actor = Actor('assets/pistol_shaded_test.glb')
        # actor = Actor('assets/pistol_bang.glb')
        # actor_scale = 2.25
        # actor.play('Idle')
        
        self.player = Player(self).gun
        self.focus = self.player
        self.terrain.setFocus(self.focus)
        # Accept the control keys for movement
                
        self.camera = FpsCamera(self.player, self.terrain)
        # self.player.reparentTo(render)
        # self.mouseLook = FirstPersonCamera(self, self.cam, CAMERA_POS_Z, self.render, None)
        # self.mouseLook.start()
        
        
        self.mouseInvertY = False
        self.accept("escape", sys.exit)
        # self.accept("w", self.player.setControl, ["forward", 1])
        # self.accept("a", self.player.setControl, ["left", 1])
        # self.accept("s", self.player.setControl, ["back", 1])
        # self.accept("d", self.player.setControl, ["right", 1])
        # self.accept("shift", self.player.setControl, ["turbo", 1])
        self.accept("1", self.sky.setTime, [300.0])
        self.accept("2", self.sky.setTime, [600.0])
        self.accept("3", self.sky.setTime, [900.0])
        self.accept("4", self.sky.setTime, [1200.0])
        self.accept("5", self.sky.setTime, [1500.0])
        self.accept("6", self.sky.setTime, [1800.0])
        self.accept("7", self.sky.setTime, [2100.0])
        self.accept("8", self.sky.setTime, [0.0])
        # self.accept("n", self.sky.toggleNightSkip)
        # self.accept("w-up", self.player.setControl, ["forward", 0])
        # self.accept("a-up", self.player.setControl, ["left", 0])
        # self.accept("s-up", self.player.setControl, ["back", 0])
        # self.accept("d-up", self.player.setControl, ["right", 0])
        # self.accept("shift-up", self.player.setControl, ["turbo", 0])
        
    
    def move(self, task):
        #self.lightpivot.setPos(self.focus.getPos() + Vec3(0, 0, 4))
        if not getMouseLook():
            return Task.cont

        elapsed = task.time - self.prevtime

        # use the mouse to look around and set player's direction
        md = base.win.getPointer(0)
        deltaX = md.getX() -200
        deltaY = md.getY() -200
        if self.mouseInvertY:
            deltaY *= -1
            
        if base.win.movePointer(0, 200, 200):
            self.camera.update(deltaX, deltaY)
            
        # self.player.update(elapsed)

        self.terrain.setShaderInput("camPos", base.cam.getPos(self.render))
        self.terrain.setShaderInput("fogColor", self.sky.fog.getColor())
        #print self.sky.fog.fog.getColor()
        

        # Store the task time and continue.
        self.prevtime = task.time
        return Task.cont
    
    def update(self, task):
        dt = globalClock.getDt()
        
        self.world.doPhysics(dt)
        
        return task.cont
    
game = Game()
game.run()