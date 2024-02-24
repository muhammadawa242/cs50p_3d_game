from direct.showbase import DirectObject
from panda3d.bullet import BulletRigidBodyNode, BulletPlaneShape
from panda3d.core import Point3, Vec3

class House(DirectObject.DirectObject):
    def __init__(self, house_file, house_scale):
        self.env = loader.loadModel(house_file)
        self.env.setScale(house_scale)
        self.env.reparentTo(render)
        
        self.env_shape = BulletPlaneShape(Vec3(0,0,1),0)
        self.node = BulletRigidBodyNode('env')
        self.node.addShape(self.env_shape)
        
        self.np = render.attachNewNode(self.node)
        self.np.setPos(0,0,0)
        
        
    def get_bullet_node(self):
        return self.node
    