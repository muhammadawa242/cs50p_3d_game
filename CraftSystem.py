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
            o = 0
            l = []
            for i in reversed(s.split('\n')):
                if o == 5:
                    break
                o += 1
                
                if file == 'medieval_stuff':
                    self.env = Item(i, 'assets/kenney_retro-medieval-kit/Models/GLTF format/'+i, 3)
                else:
                    self.env = Item(i, 'assets/KayKit_DungeonRemastered_1.0_FREE/KayKit_DungeonRemastered_1.0_FREE/Assets/gltf/'+i, 3)
                
                self.env.set_obj_pos(3,3 + y,0)
                y += 30
                l.append(self.env)
                
        Item.attach(l[0],l[1],'front','top',0)