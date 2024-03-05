from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton, Vec3
from screeninfo import get_monitors
from fps_terrain import FpsCamera
from Player import Player
from CraftSystem import CraftSystem
from Terrain import Terrain
from Zombie import Zombie
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionRay, CollisionHandlerQueue
from panda3d.core import TextureStage, TexGenAttrib, Texture, LoaderOptions, TexturePool, Fog, AmbientLight
from panda3d.core import TextNode
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
        
        self.win.requestProperties(properties)
                        
        # set 2d text on screen temporarily - can be converted to HUD
        text = TextNode('node name')
        text.setText("Every day in every way I'm getting better and better.")
        textNodePath = base.aspect2d.attach_new_node(text)
        textNodePath.setScale(0.07)
        
        # set lightning to avoid reflection from walls
        # ambient = AmbientLight("ambient")
        # ambient.set_color((.5, .5, .5, 0))
        # ambient_np = base.render.attach_new_node(ambient)
        # base.render.set_light(ambient_np)

        CraftSystem(text)
        terrain = Terrain(5, [(1,1,1,1),(0,0,0,0)])
        
        # load player
        self.player_actor = Actor('assets/KayKit_Adventurers_1.0_FREE/KayKit_Adventurers_1.0_FREE/Characters/gltf/Barbarian.glb')
        self.player = Player(self.player_actor, 1)
        
        # fps camera
        self.camera = FpsCamera(self.player_actor)
        self.mouseInvertY = False
        
        # bullet world for physics
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.attach(terrain.get_bullet_node())
        self.world.attach(self.player.get_bullet_node())
        
        self.taskMgr.add(self.update, 'update') # bullet update
        self.taskMgr.add(self.move, "moveTask") # player movement
                
        
    
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