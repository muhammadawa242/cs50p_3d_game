from direct.showbase import DirectObject
from panda3d.core import LPoint2f, Vec3, KeyboardButton, CollisionSegment, BitMask32, MouseButton
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionBox
from Item import Item
from common_functions import press_once

class CraftSystem(DirectObject.DirectObject):
    def __init__(self,text):
        self.text = text
        # loads all the material from a pack and lines em up
        file = 'dungeon_stuff'
        # file = 'medieval_stuff'

        # ray casting
        self.ctrav = CollisionTraverser()
        self.ray_queue = CollisionHandlerQueue()
        
        self.ray = CollisionSegment()
        p = CollisionHandlerPusher()
        # self.ray.setFromLens(base.camNode,10)
        ray_node = CollisionNode("ray")
        ray_node.add_solid(self.ray)
        self.ray_np = base.cam.attach_new_node(ray_node)
        ray_node.setFromCollideMask(0x10)
        self.ctrav.addCollider(self.ray_np, self.ray_queue)
        self.ray_np.show()
        
        with open(file + '.txt', 'r') as f:
            y = 0
            s = f.read()
            o = 0
            self.l = []
            
            self.items = []
            
            for i in reversed(s.split('\n')):
                if o == 5:
                    break
                o += 1
                
                if file == 'medieval_stuff':
                    self.env = Item(i, 'assets/kenney_retro-medieval-kit/Models/GLTF format/'+i, 3)
                else:
                    self.env = Item(i, 'assets/KayKit_DungeonRemastered_1.0_FREE/KayKit_DungeonRemastered_1.0_FREE/Assets/gltf/'+i, 3)
                
                self.env.item.setPythonTag('item',str(i))
                self.env.set_obj_pos(3,3 + y,0)
                y += 30
                self.l.append(self.env)
                
        # Item.attach(self.l[0],self.l[1],'bottom','top',0)
                
        # taskMgr.add(self.rotation_command, extraArgs=['arrow_left', CraftSystem.foo, 0], appendTask=True)
        taskMgr.add(self.rotate, extraArgs=['arrow_up', CraftSystem.yaw, 0], appendTask=True)
        taskMgr.add(self.rotate, extraArgs=['arrow_down', CraftSystem.pitch, 1], appendTask=True)
        taskMgr.add(self.rotate, extraArgs=['arrow_right', CraftSystem.roll, 2], appendTask=True)
        taskMgr.add(self.rotate, extraArgs=[MouseButton.button(0), self.list_fill, 3], appendTask=True)
    
    def list_fill(self,_):
        """when clicked, adds items to a list and attaches the list's 2 elements together
        on desired faces"""
        
        self.ctrav.traverse(render)
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            rayHit = self.ray_queue.getEntry(0).getIntoNodePath().getKey()
            self.text.setText(str(rayHit))
            
            self.items.append(int(rayHit))
            if len(self.items) == 2:
                if self.items[0] == self.items[1]:
                    del self.items[1]
                    return
                
                self.text.setText(str(self.items))
                Item.attach(self.l[self.items[0]-1], self.l[self.items[1]-1], 'right','left',0)
                self.items = []
                
    
    def rotate(self, key, func, flag_indx, task):
        self.ray.setFromLens(base.cam.node(),0,10) #does this work right?
        
        press_once(key, func, flag_indx, self.l, reset=False)
        return task.cont

    def yaw(l):
        l[1].set_rotation(0)
    def pitch(l):
        l[1].set_rotation(1)
    def roll(l):
        l[1].set_rotation(2)