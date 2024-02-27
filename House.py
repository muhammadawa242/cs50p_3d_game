from direct.showbase import DirectObject
from panda3d.bullet import BulletRigidBodyNode, BulletPlaneShape
from panda3d.core import Point3, Vec3, KeyboardButton
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionBox
from Item import Item

class House(DirectObject.DirectObject):
    def __init__(self):
        # loads all the material from a pack and lines em up
        file = 'dungeon_stuff'
        # file = 'medieval_stuff'
        with open(file + '.txt', 'r') as f:
            y = 0
            s = f.read()
            for i in s.split('\n'):
                self.env = Item(i, 'assets/KayKit_DungeonRemastered_1.0_FREE/KayKit_DungeonRemastered_1.0_FREE/Assets/gltf/'+i, 3)
                # if file == 'medieval_stuff':
                #     self.env = loader.loadModel('assets/kenney_retro-medieval-kit/Models/GLTF format/'+i)
                # else:
                #     self.env = loader.loadModel('assets/KayKit_DungeonRemastered_1.0_FREE/KayKit_DungeonRemastered_1.0_FREE/Assets/gltf/'+i)
                # self.env.setScale(30)
                # self.env.setY(3 + y)
                # self.env.reparentTo(render)
                self.env.set_obj_pos(3,3 + y,0)
                y += 30
        
        self.env_shape = BulletPlaneShape(Vec3(0,0,1),0)
        self.node = BulletRigidBodyNode('env')
        self.node.addShape(self.env_shape)
        
        self.np = render.attach_new_node(self.node)
        self.np.setPos(0,0,0)
        # with open('asd.csv') as f:
        #     x = f.read().split('\n')
        # self.box_positions = {
        #     'bed0' : (Point3(8.50779, -9.93618, 2.76),Point3(5.71946, -17, 3)),
        #     'table0' : (Point3(float(x[0]),float(x[1]),float(x[2])),Point3(float(x[4]),float(x[5]),float(x[6])))
        # }
        
        # self.set_colliders()
        # taskMgr.add(self.set_colliders, 'oh')
        
        
    def get_bullet_node(self):
        return self.node
    
    # def set_colliders(self, task):
    #     if base.mouseWatcherNode.is_button_down(KeyboardButton.ascii_key('z')):
    #         with open('asd.csv') as f:
    #             x = f.read().split('\n')
                
    #         self.box_positions = {
    #             'test0' : [(float(x[0]),float(x[1]),float(x[2])),float(x[4]),float(x[5]),float(x[6])]
    #         }
            
    #         for box_name in self.box_positions:
    #             box_shape = CollisionBox(self.box_positions[box_name][0],self.box_positions[box_name][1],self.box_positions[box_name][2],self.box_positions[box_name][3])
    #             box_node = CollisionNode(box_name)
    #             box_node.addSolid(box_shape)
    #             box_np = render.attach_new_node(box_node)
    #             box_np.show()
        
    #     return task.cont