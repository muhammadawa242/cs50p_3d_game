from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton, Vec3
from screeninfo import get_monitors
from fps_terrain import FpsCamera
from Player import Player
from CraftSystem import *
from Terrain import Terrain
from panda3d.core import TextNode
from panda3d.bullet import BulletBoxShape, BulletWorld, BulletRigidBodyNode, BulletPlaneShape
from Gui import *


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
        # text.setText("Every day in every way I'm getting better and better.")
        textNodePath = base.aspect2d.attach_new_node(text)
        textNodePath.setScale(0.07)
        
        # set lightning to avoid reflection from walls
        base.setBackgroundColor(0,.95,1)
        # ambient = AmbientLight("ambient")
        # ambient.set_color((.5, .5, .5, 0))
        # ambient_np = base.render.attach_new_node(ambient)
        # base.render.set_light(ambient_np)
        
        terrain = Terrain(30, [(1,1,1,1),(0,0,0,0)])
        
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
        movetask = self.taskMgr.add(self.move, "moveTask") # player movement
        
        face_gui = FaceGui(properties, movetask)
        crft = CraftSystem(text, face_gui, self.player_actor)
        inv_gui = InventoryGui(properties, movetask, crft.l)
        invt = Inventory(inv_gui, crft.l, self.player_actor)
    
    def move(self, task):
        # use the mouse to look around and set player's direction
        deltaX, deltaY = mouse_pos(base)
        if self.mouseInvertY:
            deltaY *= -1
            
        if base.win.movePointer(0, (base.win.getXSize() // 2), (base.win.getYSize() // 2)):
            self.camera.update(deltaX, deltaY)

        return Task.cont
    
    def update(self, task):
        set_physics(globalClock, self.world)
        return task.cont
    

def main():
    game = Game()
    game.run()
    
def set_physics(clock, world):
    dt = get_delta(clock)
    world.doPhysics(dt)
    return True

def get_delta(clock):
    return clock.getDt()

def mouse_pos(base):
    md = base.win.getPointer(0)
    deltaX = md.getX() - base.win.getXSize() // 2
    deltaY = md.getY() - base.win.getYSize() // 2
    return deltaX, deltaY
    
    
if __name__ == "__main__":
    main()