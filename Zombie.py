from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton
import math
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode

class Zombie(DirectObject.DirectObject):
    def __init__(self, game, x_pos, flinch):
        self.game = game
        self.zombie = Actor('assets/zombie2.glb')
        self.zombie.loop(flinch)
        self.zombie.reparentTo(game.render)
        self.zombie.setPos(x_pos*90,50,0)
        self.walking = False
        self.die = False
        self.once = True
        self.game.taskMgr.add(self.zombie_walk, 'zombie_walk')
        
        # print(self.zombie.getAnimNames())
        
    def get_zombie(self):
        return self.zombie
    
    def zombie_walk(self, task):
        if not self.die:
            # Don't allow zombie move along vertical plane on collisions
            self.zombie.setZ(0)
            
            # 2D plane movement
            if self.zombie.getX() - self.game.cam.getX() > 0:
                self.zombie.setX(self.zombie.getX() - 1)
            elif self.zombie.getX() - self.game.cam.getX() < 0:
                self.zombie.setX(self.zombie.getX() + 1)
                
            if self.zombie.getY() - self.game.cam.getY() > 0:
                self.zombie.setY(self.zombie.getY() - 1)
            elif self.zombie.getY() - self.game.cam.getY() < 0:
                self.zombie.setY(self.zombie.getY() + 1)
            
            # direct zombie's front towards the camera constantly
            if self.game.cam.getX() != 0:
                self.zombie.setH(((math.atan2((self.game.cam.getY()*(math.pi/180)),(self.game.cam.getX()*(math.pi/180))))*180/math.pi)+90)
            
            self.zombie.setP(0)
            self.zombie.setR(0)

        else:
            if self.once:
                self.zombie.play('dieheadshot2')
                self.once = False
            
        return task.cont