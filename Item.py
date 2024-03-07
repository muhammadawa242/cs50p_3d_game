from direct.showbase import DirectObject
from panda3d.core import Point3, Vec3, KeyboardButton, LVecBase3f, BitMask32, LPoint3
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionBox
import copy
from rotation_rules import _rotation_rules

class Item(DirectObject.DirectObject):
    def __init__(self, name, item_path, item_scale):
        # model
        self.item = loader.loadModel(item_path)
        self.item.setScale(item_scale)
        self.item.reparentTo(render)
        
        bound0, bound1 = self.item.getTightBounds()[0], self.item.getTightBounds()[1]
        dimensions = bound1 - bound0
        x, y, z = dimensions[0], dimensions[1], dimensions[2]
        
        # (x,y,z) point of each face positions from mid to respective face for all 6
        self.faces_positions = {
            'front' : [y/2, LVecBase3f(0, -1, 0)],
            'top' : [z, LVecBase3f(0, 0, 1)],
            'left' : [x/2, LVecBase3f(1, 0, 0)],
            'right' : [x/2, LVecBase3f(-1, 0, 0)],
            'bottom' : [0, LVecBase3f(0, 0, -1)],
            'back' : [y/2, LVecBase3f(0, 1, 0)]
        }
        
        # will later be used to reset original faces
        self.faces_copy = copy.deepcopy(self.faces_positions)
        
        # put collider round the item
        self.item_shape = CollisionBox(bound0/3, bound1/3)
        self.item_node = CollisionNode(name)
        self.item_node.addSolid(self.item_shape)
        self.np = self.item.attach_new_node(self.item_node)
        # self.np.show()
        
        # set into colision mask
        self.np.setCollideMask(0x10)
        
        
    def set_obj_pos(self, x, y, z):
        self.item.setPos(x, y, z)
        
    
    def set_rotation(self, hpr):
        """This function sets +90 deg rotation along one axis at a time.
        if multiple rotations along different axes are required call it accordingly."""
        
        if hpr != 0 and hpr != 1 and hpr != 2:
            print('Wrong input!')
            return
        
        four_seq = [
            ['left', 'back', 'right', 'front'],
            ['top', 'front', 'bottom', 'back'],
            ['top', 'right', 'bottom', 'left']
        ]
        
        # (h,p,r) represented by (0,1,2)
        self.replace_faces(four_seq[hpr])
        
        if hpr == 0: self.item.setH(self.item.getH()+90)
        if hpr == 1: self.item.setP(self.item.getP()+90)
        if hpr == 2: self.item.setR(self.item.getR()+90)
    
    def reset_rotations(self):
        self.faces_positions = copy.deepcopy(self.faces_copy)
        self.item.setHpr(0,0,0)
        
        
    def replace_faces(self, keys_list):
        """This function changes the placement of the dictinoary's values
        based on order of provided keys_list elements in circular manner"""
        
        if len(keys_list) != 4:
            print('Error replacing faces!')
            return
        
        tmp = self.faces_positions[keys_list[0]][1]
        last_indx = len(keys_list)-1
        
        for i in range(last_indx):
            self.faces_positions[keys_list[i]][1] = self.faces_positions[keys_list[i+1]][1]
            
        self.faces_positions[keys_list[last_indx]][1] = tmp
        
    
    def get_face_pos(self, face):
        # panda has no float*vector operator so order is vector*float
        return self.faces_positions[face][1]*self.faces_positions[face][0]
    
    def attach(first_item, second_item, first_face, second_face):
        """Attaches 2 Item objects together. The second one will be
        placed after the first one joining the desired faces for both objects"""
        
        for i in _rotation_rules[first_face][second_face]:
            second_item.set_rotation(i)
        
        first_pos = first_item.item.getPos() + first_item.get_face_pos(first_face)
        second_spacing = second_item.get_face_pos(second_face) # second item needs to start at the face not its middle point
        second_item.item.set_pos(first_pos-second_spacing)