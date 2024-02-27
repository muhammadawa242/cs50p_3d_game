from direct.showbase import DirectObject
from panda3d.core import Point3, Vec3, KeyboardButton
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionBox


class Item(DirectObject.DirectObject):
    def __init__(self, name, item_path, item_scale):
        self.item = loader.loadModel(item_path)
        self.item.setScale(item_scale)
        self.item.reparentTo(render)
        
        # put collider round the item
        self.item_shape = CollisionBox(self.item.getTightBounds()[0], self.item.getTightBounds()[1])
        self.item_node = CollisionNode(name)
        self.item_node.addSolid(self.item_shape)
        self.np = render.attach_new_node(self.item_node)
        self.np.show()
        
    def set_obj_pos(self, x, y, z):
        """set the item's position along with collider cause collider not a child of item"""
        self.item.setPos(x, y, z)
        self.np.setPos(x, y, z)
        
    def __add__(self,other):
        ...