from direct.gui.DirectGui import *
from direct.showbase import DirectObject

class Gui(DirectObject.DirectObject):
    def __init__(self, properties, movetask):
        self.box = DirectDialog(frameSize = (-0.7, 0.7, -0.7, 0.7),
                                    fadeScreen = 0.4)
        self.movetask = movetask
        self.properties = properties
        self.first_face = ''
        self.second_face = ''
        
    def show_cursor(self):
        """show cursor and cancel move task so that cursor can be moved"""
        self.movetask.remove()
        self.properties.setCursorHidden(False)
        base.win.requestProperties(self.properties)
        
    def hide_cursor_again(self):
        """hide cursor and stop cursor movement"""
        base.win.movePointer(0, (base.win.getXSize() // 2), (base.win.getYSize() // 2))
        taskMgr.add(self.movetask)
        self.properties.setCursorHidden(True)
        base.win.requestProperties(self.properties)
        

class FaceGui(Gui):
    def __init__(self, properties, movetask):
        super(FaceGui, Gui.__init__(self, properties, movetask))
        
        # for first
        first_column = [
            DirectButton(text = "Front",
                   pos = (-0.4, 0, 0.5),
                   parent = self.box,
                   scale = 0.07),
            DirectButton(text = "Back",
                    pos = (-0.4, 0, 0.3),
                    parent = self.box,
                    scale = 0.07),
            DirectButton(text = "Top",
                    pos = (-0.4, 0, 0.1),
                    parent = self.box,
                    scale = 0.07),
            DirectButton(text = "Bottom",
                    pos = (-0.4, 0, -0.1),
                    parent = self.box,
                    scale = 0.07),
            DirectButton(text = "Left",
                    pos = (-0.4, 0, -0.3),
                    parent = self.box,
                    scale = 0.07),
            DirectButton(text = "Right",
                    pos = (-0.4, 0, -0.5),
                    parent = self.box,
                    scale = 0.07)
            ]
        
        # for second
        second_column = [
            DirectButton(text = "Front",
                   pos = (0.4, 0, 0.5),
                   parent = self.box,
                   scale = 0.07),
            DirectButton(text = "Back",
                    pos = (0.4, 0, 0.3),
                    parent = self.box,
                    scale = 0.07),
            DirectButton(text = "Top",
                    pos = (0.4, 0, 0.1),
                    parent = self.box,
                    scale = 0.07),
            DirectButton(text = "Bottom",
                    pos = (0.4, 0, -0.1),
                    parent = self.box,
                    scale = 0.07),
            DirectButton(text = "Left",
                    pos = (0.4, 0, -0.3),
                    parent = self.box,
                    scale = 0.07),
            DirectButton(text = "Right",
                    pos = (0.4, 0, -0.5),
                    parent = self.box,
                    scale = 0.07)
            ]
        
        for first in first_column:
            first.bind(DGG.B1CLICK, self.buttonPressed0, extraArgs=[first['text']])
        
        for second in second_column:
            second.bind(DGG.B1CLICK, self.buttonPressed1, extraArgs=[second['text']])

    def buttonPressed0(self, text, mousePos):
        self.first_face = text.lower()
    
    def buttonPressed1(self, text, mousePos):
        self.second_face = text.lower()