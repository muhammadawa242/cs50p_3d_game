from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib

class Player(DirectObject.DirectObject):
    def __init__(self, game):
        self.game = game
        self.gun = Actor('assets/pistol_bang.glb')
        self.gun.setScale(30)
        self.game.taskMgr.add(self.gun_stuff,'gun_stuff')
        
        self.gun.reparentTo(self.game.render)
        self.gun.loop('Idle')
        self.imageObject = OnscreenImage(image='assets/cross.png', pos=(0, 0, 0))
        self.imageObject.setTransparency(TransparencyAttrib.MAlpha)
        self.imageObject.setScale(.05)
        
    def gun_stuff(self,task):
        self.game.ray.setFromLens(self.game.camNode,0,0)
        
        self.gun.setHpr(self.game.cam, 188,-3,-1)
        self.gun.setPos(self.game.cam,2.5,10,-47.5)#2-50)

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
                # rayHit_np.removeNode()
                # hitPos = rayHit.getSurfacePoint(render)
                
                # get the zombie/entry(0) to stop walking and animate death here
                if rayHit_np.hasPythonTag(name):
                    hitObject = rayHit_np.getPythonTag(name)
                    hitObject.die = True
        
        return task.cont