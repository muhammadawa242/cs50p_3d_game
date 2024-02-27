from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from panda3d.core import CardMaker, Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletPlaneShape


class Terrain(DirectObject.DirectObject):
    def __init__(self, tiles_quant, color_list):
        self.floor = render.attach_new_node("floor")
        self.color_list = color_list
        self.cardmaker = CardMaker('quad')
        self.floor_generate(tiles_quant)
        
        # add bullet plain so players can stand here
        self.env_shape = BulletPlaneShape(Vec3(0,0,1),0)
        self.node = BulletRigidBodyNode('env')
        self.node.addShape(self.env_shape)
        self.np = render.attach_new_node(self.node)
        self.np.setPos(0,0,0)
    
    def quad(self, floor, frame, color, hpr):
        self.cardmaker.set_frame(frame)
        self.cardmaker.set_color(color)
        
        quad = floor.attach_new_node(self.cardmaker.generate())
        quad.set_two_sided(True)
        quad.set_hpr(hpr)
        
        return quad

    def floor_generate(self, width=1, size=40):
        
        for y in range(width):
            
            for x in range(width):
                # alternate tile colors if more than one tiles color provided
                color = self.color_list[(x+y)%len(self.color_list)]
                
                frame = (x*size,x*size+size,y*size,y*size+size)
                self.quad(self.floor, frame, color, (0,-90,0))

    def get_bullet_node(self):
        return self.node