from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib, Vec3
from panda3d.bullet import BulletCapsuleShape, BulletRigidBodyNode, BulletCharacterControllerNode

class Player(DirectObject.DirectObject):
    def __init__(self, game):
        self.game = game
        self.gun = Actor('assets/pistol_bang.glb')
        self.gun.setScale(2.25)
        self.game.taskMgr.add(self.gun_stuff,'gun_stuff')
        self.game.taskMgr.add(self.set_player_height,'set_player_height')
        self.game.taskMgr.add(self.move_player,'move_player')
        
        self.gun.loop('Idle')
        self.imageObject = OnscreenImage(image='assets/cross.png', pos=(0, 0, 0))
        self.imageObject.setTransparency(TransparencyAttrib.MAlpha)
        self.imageObject.setScale(.05)
        
        # bullet world settings
        shape = BulletCapsuleShape(radius=1, height=3.6) # 2.25 + 1.59(cam height) + {cam own length} = total height
        self.node = BulletCharacterControllerNode(shape, 1, 'capsule_player')
        # node.setMass(7.0)
        # node.addShape(shape)
        self.np = render.attachNewNode(self.node)
        self.np.setPos(0,0,200)
        self.gun.reparentTo(self.np)
        self.game.world.attach(self.node)
        
    def gun_stuff(self,task):
        self.game.ray.setFromLens(self.game.camNode,0,0)
        
        # self.gun.setHpr(self.game.cam, 188,-3,-1)
        # self.gun.setPos(self.game.cam,2.5,10,-47.5)#2-50)

        r = KeyboardButton.ascii_key('r')
        l = MouseButton.button(0)

        is_down = self.game.mouseWatcherNode.is_button_down

        # self.gun.setPlayRate(2.0,'Reload')
        if is_down(r):
            self.gun.play('Reload')
            
        if is_down(l):
            self.gun.play('Shoot')
            if self.game.rayqueue.getNumEntries() > 0:
                self.game.rayqueue.sortEntries()
            
                rayHit = self.game.rayqueue.getEntry(0)
                rayHit_np = rayHit.getIntoNodePath()
                name = rayHit_np.getName()
                self.game.cTrav.removeCollider(rayHit_np)
                rayHit_np.detachNode()
                # hitPos = rayHit.getSurfacePoint(render)
                
                # get the zombie/entry(0) to stop walking and animate death here
                if rayHit_np.hasPythonTag(name):
                    hitObject = rayHit_np.getPythonTag(name)
                    hitObject.die = True
        
        return task.cont


    def move_player(self, task):
        speed_sens = 3
        w = KeyboardButton.ascii_key('w')
        s = KeyboardButton.ascii_key('s')
        a = KeyboardButton.ascii_key('a')
        d = KeyboardButton.ascii_key('d')
        c = KeyboardButton.ascii_key('c')
        
        is_down = self.game.mouseWatcherNode.is_button_down
        
        speed = Vec3(0, 0, 0)
        
        # liner movement (opposite directions: cause camera is 180 to gun remember)
        if is_down(w): speed.setY(-speed_sens)
        if is_down(s): speed.setY( speed_sens)
        if is_down(a): speed.setX( speed_sens)
        if is_down(d): speed.setX(-speed_sens)
        
        self.node.setLinearMovement(speed, True)
        
        # jumping
        if is_down(c):
            self.node.setMaxJumpHeight(5.0)
            self.node.setJumpSpeed(8.0)
        
            self.node.doJump()

        # angular movement
        # implemented in fps_terrain. coupling caution!
        
        return task.cont

        
    
    def set_player_height(self, task):
        xy_pos = self.game.terrain.getElevation(self.np.getX(),self.np.getY())
        
        if self.np.getZ() <= xy_pos:
            self.np.setZ(xy_pos)
        return task.cont