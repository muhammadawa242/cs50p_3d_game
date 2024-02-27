from direct.showbase import DirectObject
from panda3d.core import Point3, Vec3, KeyboardButton
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionBox
from Item import Item

class CraftSystem(DirectObject.DirectObject):
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