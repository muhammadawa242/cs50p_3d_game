from project import set_physics, get_delta, mouse_pos
from panda3d.bullet import BulletWorld
from direct.showbase.ShowBase import ShowBase

base = ShowBase()

def test_set_physics():
    assert set_physics(globalClock, BulletWorld()) == True
    
def test_get_delta():
    assert get_delta(globalClock) == globalClock.getDt()


def test_mouse_pos():    
    assert mouse_pos(base) == (base.win.getPointer(0).getX() - base.win.getXSize() // 2, 
                               base.win.getPointer(0).getY() - base.win.getYSize() // 2)