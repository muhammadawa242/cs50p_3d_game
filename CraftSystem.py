from direct.showbase import DirectObject
from panda3d.core import LPoint2f, Vec3, KeyboardButton, CollisionRay, BitMask32, MouseButton
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionBox
from Item import Item
from common_functions import press_once

class CraftSystem(DirectObject.DirectObject):
    def __init__(self,text,gui,player):
        self.text = text
        self.gui = gui
        self.gui.box.hide()
        self.player = player
        # loads all the material from a pack and lines em up
        file = 'dungeon_stuff'
        # file = 'medieval_stuff'

        # ray casting
        self.ctrav = CollisionTraverser()
        self.ray_queue = CollisionHandlerQueue()
        self.ray = CollisionRay()
        p = CollisionHandlerPusher()
        
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
                
                self.env.np.setTag(str(i),str(o))
                self.env.set_obj_pos(3,3 + y,0)
                y += 30
                self.l.append(self.env)

        # tasks are meant to be added the following way to allow single press key functionality
        taskMgr.add(self.press_to_rotate, extraArgs=['z', self.yaw, 0], appendTask=True)
        taskMgr.add(self.press_to_rotate, extraArgs=['x', self.pitch, 1], appendTask=True)
        taskMgr.add(self.press_to_rotate, extraArgs=['c', self.roll, 2], appendTask=True)
        taskMgr.add(self.click_to_add, extraArgs=[MouseButton.button(0), self.list_fill, 3], appendTask=True)
        
        taskMgr.add(self.attach_faces, 'attach_faces')
        taskMgr.add(self.move_along_axis, 'move_along_axis')

    
    def move_along_axis(self, task):
        """It will let you select one item, move it and deselect it when done."""
        
        if len(self.items)==1:
            displacement = .1
            self.l[self.items[0]-1].np.show()
            # along x axis
            if base.mouseWatcherNode.isButtonDown('arrow_right'):
                self.l[self.items[0]-1].item.setX(self.l[self.items[0]-1].item.getX()+displacement)
            if base.mouseWatcherNode.isButtonDown('arrow_left'):
                self.l[self.items[0]-1].item.setX(self.l[self.items[0]-1].item.getX()-displacement)
            
            # along y axis
            if base.mouseWatcherNode.isButtonDown('arrow_up'):
                self.l[self.items[0]-1].item.setY(self.l[self.items[0]-1].item.getY()+displacement)
            if base.mouseWatcherNode.isButtonDown('arrow_down'):
                self.l[self.items[0]-1].item.setY(self.l[self.items[0]-1].item.getY()-displacement)
            
            # along z axis
            if base.mouseWatcherNode.isButtonDown('page_up'):
                self.l[self.items[0]-1].item.setZ(self.l[self.items[0]-1].item.getZ()+displacement)
            if base.mouseWatcherNode.isButtonDown('page_down'):
                self.l[self.items[0]-1].item.setZ(self.l[self.items[0]-1].item.getZ()-displacement)
            
            # bring item down to the player
            if base.mouseWatcherNode.isButtonDown('control') and base.mouseWatcherNode.isButtonDown(MouseButton.button(0)):
                self.l[self.items[0]-1].item.setPos(self.player, 0, -50, 0)
        
        # deselect the item when escape button pressed
        if base.mouseWatcherNode.isButtonDown('escape') and len(self.items)!=0:
            self.l[self.items[0]-1].np.hide()
            self.hide_shit()
            
        return task.cont
    
    def press_to_rotate(self, key, func, flag_indx, task):
        press_once(key, func, flag_indx, self.l, reset=False)
        return task.cont
    
    def click_to_add(self, key, func, flag_indx, task):
        press_once(key, func, flag_indx, self.l, reset=True)
        return task.cont

    def attach_faces(self, task):
        """provided the first and second face, join both of them """
        if self.gui.first_face != '' and self.gui.second_face != '':
            Item.attach(self.l[self.items[0]-1], self.l[self.items[1]-1], self.gui.first_face,self.gui.second_face)
            self.hide_shit()
            
        return task.cont

    def hide_shit(self):
        self.gui.show_cursor()  # have to call it otherwise calling hide on next line would mean hiding mouse that is already hidden
        self.gui.hide_cursor_again()
        self.gui.box.hide()
        self.items = []
        self.gui.first_face = ''
        self.gui.second_face = ''
        
    # Following functions get called only 'once' when respective key is pressed
    # by being called in the press_once function
    
    def list_fill(self,_):
        """when clicked, adds items to a list"""
        
        self.ray.setFromLens(base.camNode,0,0)
        self.ctrav.traverse(render)
        
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            try:
                rayHitnp = self.ray_queue.getEntry(0).getIntoNodePath()
                name = rayHitnp.getName()
                rayHit = rayHitnp.getTag(name)
            except:
                return
            
            self.items.append(int(rayHit))
            
            if len(self.items) == 2:
                if self.items[0] == self.items[1]:
                    del self.items[1]
                    return
                
                # show the dialogue box once 2 items are selected
                self.l[self.items[0]-1].np.hide()
                self.gui.box.show()
                self.gui.show_cursor()
        
        # self.text.setText(str(self.items))
    
    def yaw(self,_):
        if len(self.items)==1:
            self.l[self.items[0]-1].set_rotation(0)
    def pitch(self,_):
        if len(self.items)==1:
            self.l[self.items[0]-1].set_rotation(1)
    def roll(self,_):
        if len(self.items)==1:
            self.l[self.items[0]-1].set_rotation(2)
            
        
            
class Inventory(DirectObject.DirectObject):
    def __init__(self, gui, l, player):
        self.gui = gui
        self.l = l
        self.gui.box.hide()
        self.show_flag = 1
        self.player = player
        
        taskMgr.add(self.show_inventory_task, extraArgs=['i', self.show_inventory, 4], appendTask=True)
        taskMgr.add(self.add_item, 'add_item')
        
    
    def add_item(self, task):
        # if some button is selected in inventory
        if self.gui.item_selected != None:
            selected_indx = self.gui.item_selected
            self.hide_shit()
            # add item to render
            env = Item(self.l[selected_indx].name+str(len(self.l)), 'assets/KayKit_DungeonRemastered_1.0_FREE/KayKit_DungeonRemastered_1.0_FREE/Assets/gltf/'+self.l[selected_indx].name, 3)
            
            self.l.append(env)
            env.np.setTag(self.l[-1].name,str(len(self.l)))
            self.l[-1].item.reparentTo(render)
            self.l[-1].item.setPos(self.player, 0,-50,0)
            self.l[-1].item.setZ(0)
            # load item to self.l
            
        return task.cont
    
    def hide_shit(self):
        self.gui.box.hide()
        self.gui.show_cursor()
        self.gui.hide_cursor_again()
        self.gui.item_selected = None
        self.show_flag += 1
    
    def show_inventory_task(self, key, func, flag_indx, task):
        press_once(key, func, flag_indx, self.l, reset=True)
        return task.cont
    
    def show_inventory(self, _):
        if self.show_flag%2:
            self.gui.show_cursor()
            self.gui.box.show()
        else:
            self.hide_shit()
        
        self.show_flag += 1