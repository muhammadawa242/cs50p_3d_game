import sys
from random import randint, choice

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, CardMaker, TextNode, Fog, Point2
from panda3d.core import (
    CollisionNode,
    CollisionRay,
    CollisionHandlerQueue,
    CollisionTraverser
)


base = ShowBase()
base.accept("escape", sys.exit)
props = WindowProperties()
props.set_mouse_mode(WindowProperties.M_relative)
props.cursor_hidden = True
base.win.request_properties(props)
base.cTrav = CollisionTraverser()

fog = Fog('fog')
fog.set_color((0.1,0.1,0.1,1))
base.win.set_clear_color((0.1,0.1,0.1,1))
render.set_fog(fog)

base.info = base.a2dTopLeft.attach_new_node(TextNode("info"))
base.info.set_scale(0.04)
base.info.node().text = """\nSimple FPS Arena Example.
\nAWSD to move \nShift to run \nClick to shoot.\nEscape to exit.
"""

base.text = base.a2dBottomRight.attach_new_node(TextNode("text"))
base.text.node().set_align(1)
base.text.set_pos(-0.1,0,0.1)
base.text.set_scale(0.1)

cardmaker = CardMaker('quad')
def quad(parent, frame, color=(1,1,1,1), hpr=(45,0,0)):
    cardmaker.set_frame(frame)
    cardmaker.set_color(color)
    quad = parent.attach_new_node(cardmaker.generate())
    quad.set_two_sided(True)
    #quad.set_transparency(True)
    quad.set_hpr(hpr)
    return quad

def floor(width=64, size=4):
    floor = render.attach_new_node("floor")
    for y in range(-width//2,width//2):
        for x in range(-width//2, width//2):
            color = ((0.1,0.1,0.1,1),(0.6,0.6,0.6,1))[(x+y)%2]
            frame = (x*size,x*size+size,y*size,y*size+size)
            segment = quad(floor, frame, color, (0,-90,0))
    floor.flatten_strong()
    return floor
floor()


class Enemy:
    def __init__(self, number, chasing):
        self.chasing = chasing
        self.path = render.attach_new_node("enemy_"+str(number))
        color = (1,0.4,0.4,1)
        head = quad(self.path, (-0.2,0.2,2.2,1.8), color)
        body = quad(self.path, (-0.5,0.5,1.7,0.8), color)
        legs = quad(self.path, (-0.3,0.3,0.8,0.0), color)
        self.path.flatten_strong()
        self.path.set_collide_mask(1)
        l = chasing.level
        while self.path.get_distance(chasing.path) < 40 + l:
            self.path.set_pos(chasing.path, randint(-16*l,16*l), randint(-16*l,16*l), 0)
        base.task_mgr.add(self.update)

    def update(self, task):
        self.path.look_at(self.chasing.path)
        self.path.set_y(self.path, (self.chasing.level+1)*1.1*base.clock.dt)
        if self.path.get_distance(self.chasing.path) < 1:
            self.chasing.die()
        if self in base.enemies:
            return task.cont
        self.path.detach_node()


class Player:
    def __init__(self):
        self.level = 8
        self.path = render.attach_new_node("player")
        self.crosshair = quad(aspect2d, (-0.001,0.001,0.001,-0.001))
        base.cam.reparent_to(self.path)
        base.cam.set_z(1.85)
        base.camLens.set_fov(100,100)

        # Ray for firing.
        ray = base.cam.attach_new_node(CollisionNode('gun'))
        ray.node().add_solid(CollisionRay((0,0,0),(0,1,0)))
        ray.node().set_collide_mask(1)
        self.queue = CollisionHandlerQueue()
        base.cTrav.add_collider(ray, self.queue)
        self.trail = quad(render, (-0.01,0.01,0,128))
        self.trail.set_transparency(1)
        self.flash = quad(render2d, (-1,1,1,-1))
        self.flash.set_transparency(1)

        self.prev_mouse = Point2(0)
        self.task = base.task_mgr.add(self.update)
        base.accept("mouse1", self.shoot)
        self.spawn()

    def spawn(self):
        base.text.node().text = "Level "+str(self.level)
        self.path.set_pos(0,0,0)
        base.enemies = [Enemy(i, self) for i in range(self.level*self.level)]

    def die(self):
        self.flash.set_color_scale((1,0.2,0.2,1))
        base.enemies = []
        self.level = 2
        self.spawn()

    def shoot(self):
        self.trail.set_pos_hpr(base.cam, (0.3,0,-0.3), (1,-90,0))
        self.trail.set_color_scale((1.0,1.0,0.2,1.0))
        self.flash.set_color_scale((1.0,0.2,0.2,0.1))
        # Remove any hit enemies
        self.queue.sort_entries()
        if len(self.queue.entries) > 0:
            name = self.queue.entries[0].get_into_node_path().parent.name
            number = int(name.split("_")[1])
            base.enemies[number] = None
        # If everyone is dead, go to the next level
        if len(set(base.enemies)) <= 1:
            self.flash.set_color_scale((0.2,1,1,1))
            self.level += 1
            self.spawn()

    def update(self, task):
        # BUG: trail doesn't alpha scale because of flash overlay
        self.trail.set_color_scale(self.trail.get_color_scale()*(0.2**base.clock.dt))
        self.flash.set_color_scale(self.flash.get_color_scale()*(0.2**base.clock.dt))
        if base.mouseWatcherNode.has_mouse():
            mouse = base.mouseWatcherNode.get_mouse()
            button = getattr(base.mouseWatcherNode, 'is_raw_button_down', base.mouseWatcherNode.is_button_down) # TODO
            delta = mouse - self.prev_mouse
            self.prev_mouse = Point2(mouse)
            self.path.set_h(self.path,-delta.x*50)
            base.cam.set_p(base.cam, delta.y*50)
            base.cam.set_p(max(-85, min(base.cam.get_p(), 85)))
            speed = (8+int(button("lshift")*4))*base.clock.dt
            self.path.set_pos(self.path,
                ((int(button("d")-int(button("a")))*speed)),
                ((int(button("w")-int(button("s")))*speed)), 0)
        return task.cont


Player()
base.run()