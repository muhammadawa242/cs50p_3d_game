from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton
import math
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode

# this class might need full restructuring
class Zombie(DirectObject.DirectObject):
    def __init__(self, game, x_pos, flinch, textNodePath):
        self.textNodePath = textNodePath
        self.game = game
        # self.zombie = Actor('assets/zombie2.glb')
        self.zombie = Actor('assets/KayKit_Adventurers_1.0_FREE/KayKit_Adventurers_1.0_FREE/Characters/gltf/Rogue.glb')
        self.zombie.setScale(2)
        # self.zombie.loop(flinch)
        self.zombie.reparentTo(game.render)
        self.zombie.setPos(x_pos*9,50,1.05)
        self.walking = False
        self.die = False
        self.once = True
        self.displace = 0
        self.game.taskMgr.add(self.zombie_walk, 'zombie_walk')
        
        # print(self.zombie.getAnimNames())
        # testing animations
        self.anim_list = self.zombie.getAnimNames()
        self.anim = 0
        self.anim_over = True
        
    def get_zombie(self):
        return self.zombie
    
    def zombie_walk(self, task):
        if not self.die:
            # Don't allow zombie move along vertical plane on collisions
            # self.zombie.setZ(0)
            
            # 2D plane movement
            if self.zombie.getX() - self.game.cam.getX() > 0:
                self.zombie.setX(self.zombie.getX() - self.displace)
            elif self.zombie.getX() - self.game.cam.getX() < 0:
                self.zombie.setX(self.zombie.getX() + self.displace)
                
            if self.zombie.getY() - self.game.cam.getY() > 0:
                self.zombie.setY(self.zombie.getY() - self.displace)
            elif self.zombie.getY() - self.game.cam.getY() < 0:
                self.zombie.setY(self.zombie.getY() + self.displace)
            
            # direct zombie's front towards the camera constantly
            if self.game.cam.getX() != 0:
                self.zombie.setH(((math.atan2((self.game.cam.getY()*(math.pi/180)),(self.game.cam.getX()*(math.pi/180))))*180/math.pi)+90)
            
            self.zombie.setP(0)
            self.zombie.setR(0)

        else:
            if self.once:
                self.zombie.play('dieheadshot2')
                self.once = False
        
        # testing animations
        if base.mouseWatcherNode.isButtonDown(KeyboardButton.ascii_key('c')) and self.anim_over:
            self.zombie.loop(self.anim_list[self.anim%76])
            self.textNodePath.setText(self.anim_list[self.anim%76])
            self.anim += 1
            self.anim_over = False
        if base.mouseWatcherNode.isButtonDown(KeyboardButton.ascii_key('v')):
            self.anim_over = True
            
        return task.cont