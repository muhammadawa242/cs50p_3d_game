from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, KeyboardButton, WindowProperties, loadPrcFile, MouseButton
from panda3d.core import CardMaker
from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain
from panda3d.core import Texture
from panda3d.core import Vec3


class Terrain(DirectObject.DirectObject):
    def __init__(self, game):
        self.game = game
        self.floor = self.game.render.attach_new_node("floor")
        
        # self.env = self.game.loader.loadModel('assets/grass.glb')
        # self.env.setPos(0,50,-10)
        # self.env.reparentTo(self.game.render)
        
        self.cardmaker = CardMaker('quad')
        self.game.taskMgr.add(self.generate_terrain,'generate_terrain')
        # self.floor_generate()
        self.floor_generate(5)
        self.bee = True
        """
        --> This here, my friend, is the code for one blue tile. Make procedural tile generation possible!
        
        color = ((0,0.3,0.5,1),(0.6,0,0.6,1))[(5+5)%2]
        size = 40
        xx = -4
        yy = 1
        frame = (xx*size,xx*size+size,yy*size,yy*size+size)
        print(frame)
        self.quad(self.floor, frame, color, (0,-90,0))
        """
        
    def generate_terrain(self, task):
        # print(self.game.cam.getX())
        # if there are already tiles at this X position
        if ...:
            for i in range(4):
                var = 5
                color = ((0,0.3,0.5,1),(0.6,0,0.6,1))[(i+5)%2]
                size = 40
                
                if self.game.cam.getX() > 0:
                    xx = var+self.game.cam.getX()/40
                else:
                    xx = -var+self.game.cam.getX()/40
                    
                yy = 1+i
                frame = (xx*size,xx*size+size,yy*size,yy*size+size)
                self.quad(self.floor, frame, color, (0,-90,0))
        
        # for i in range(4):
        #     var = 5
        #     color = ((0,0.3,0.5,1),(0.6,0,0.6,1))[(i+5)%2]
        #     size = 40
            
        #     if self.game.cam.getX() > 0:
        #         xx = var+self.game.cam.getX()/40
        #     else:
        #         xx = -var+self.game.cam.getX()/40
                
        #     yy = 1+i
        #     frame = (xx*size,xx*size+size,yy*size,yy*size+size)
        #     self.quad(self.floor, frame, color, (0,-90,0))
            
        
            
        return task.cont
    
    def quad(self, floor, frame, color=(1,1,1,1), hpr=(45,0,0)):
        self.cardmaker.set_frame(frame)
        self.cardmaker.set_color(color)
        
        quad = floor.attach_new_node(self.cardmaker.generate())
        quad.set_two_sided(True)
        
        quad.set_hpr(hpr)
        return quad

    def floor_generate(self, width=1, size=40):
        
        for y in range(width):
            for x in range(width):
                # x += 4
                # y += 4
                color = ((0.3,0.3,0.1,1),(0.5,0.5,0,1))[(x+y)%2]
                frame = (x*size,x*size+size,y*size,y*size+size)
                # print(x,y)
                # print(frame)
                self.quad(self.floor, frame, color, (0,-90,0))
            # print()
        # floor.flatten_strong()
        return self.floor