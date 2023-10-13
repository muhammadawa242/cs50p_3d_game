from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton

class Player(DirectObject.DirectObject):
    def __init__(self, game):
        self.game = game
        self.gun = Actor('assets/pistol_bang.glb')
        self.gun.setScale(30)
        self.game.taskMgr.add(self.gun_stuff,'reload')
        
        self.gun.reparentTo(self.game.render)
        self.gun.loop('Idle')
        
    def gun_stuff(self,task):
        self.gun.setHpr(self.game.cam, 180,0,-1)
        self.gun.setPos(self.game.cam,0,10,2-50)

        r = KeyboardButton.ascii_key('r')
        l = MouseButton.button(0)

        is_down = self.game.mouseWatcherNode.is_button_down

        # self.gun.setPlayRate(2.0,'Reload')
        if is_down(r):
            self.gun.play('Reload')
            
        if is_down(l):
            self.gun.play('Shoot')
        
        return task.cont