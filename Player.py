from direct.showbase import DirectObject
from panda3d.core import KeyboardButton, MouseButton, TransparencyAttrib, Vec3
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.bullet import BulletCapsuleShape, BulletRigidBodyNode, BulletCharacterControllerNode

class Player(DirectObject.DirectObject):
    def __init__(self, player, scale):
        self.player = player
        self.player.setScale(scale)
        base.taskMgr.add(self.move_player,'move_player')
        
        self.imageObject = OnscreenImage(image='assets/cross.png', pos=(0, 0, 0))
        self.imageObject.setTransparency(TransparencyAttrib.MAlpha)
        self.imageObject.setScale(.05)
        
        # bullet world settings
        shape = BulletCapsuleShape(radius=1, height=scale+1.5) # 2.25 + 1.59(cam height) + {cam own length} = total height
        self.node = BulletCharacterControllerNode(shape, 1, 'capsule_player')
        self.node.setGravity(100)
        self.np = render.attach_new_node(self.node)
        self.np.setPos(100,100,0)
        self.player.reparentTo(self.np)
        self.is_on_ground = False
        

    def move_player(self, task):
        speed_sens = 3
        sprint_factor = 20
        w = KeyboardButton.ascii_key('w')
        s = KeyboardButton.ascii_key('s')
        a = KeyboardButton.ascii_key('a')
        d = KeyboardButton.ascii_key('d')
        
        is_down = base.mouseWatcherNode.is_button_down
        
        speed = Vec3(0, 0, 0)
        
        # liner movement (opposite directions: cause camera is 180 to gun remember)
        if base.mouseWatcherNode.isButtonDown("shift"): speed_sens *= sprint_factor
        if is_down(w): speed.setY(-speed_sens)
        if is_down(s): speed.setY( speed_sens)
        if is_down(a): speed.setX( speed_sens)
        if is_down(d): speed.setX(-speed_sens)
        
        # jumping
        if base.mouseWatcherNode.isButtonDown("space"):
            self.node.setMaxJumpHeight(3.0)
            self.node.setJumpSpeed(20.0)
            self.node.doJump()
            

        self.node.setLinearMovement(speed, True)
        # angular movement
        # implemented in fps_terrain. coupling caution!
        
        return task.cont
    
    def get_bullet_node(self):
        return self.node