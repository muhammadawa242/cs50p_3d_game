from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from panda3d.core import CardMaker


class Terrain(DirectObject.DirectObject):
    def __init__(self, tiles_quant, color_list):
        self.floor = render.attach_new_node("floor")
        self.color_list = color_list
        self.cardmaker = CardMaker('quad')
        self.floor_generate(tiles_quant)
    
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

