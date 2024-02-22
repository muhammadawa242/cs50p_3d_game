"""This class is a modification of followCamera which also inherits from TerrainCamera"""

from Panda_3d_Procedural_Terrain_Engine.src.camera import *


class FpsCamera(TerrainCamera):
    
    def __init__(self, player, terrain):
        TerrainCamera.__init__(self)

        self.terrain = terrain
        self.player = player
        
        # make camera a child of player node
        self.camNode.reparentTo(player)
        
        # otherwise the camera and model are opposite to each other
        # Also this means pitch is now inverted. -x is now x
        self.camNode.setHpr(self.player, 180,3,5)
        
        # set the camera at player's head position level
        self.camNode.setPos(0.01,0.15,1.59)
        
        self.maxPitch = 50
        self.minPitch = -50
        
        
    def update(self, x, y):
        
        # alter player's yaw by an amount proportionate to deltaX
        self.player.setH(self.player.getH() - 0.3 * x)
        
        # find the new player pitch and clamp it to a reasonable range
        self.playerPitch = self.player.getP() + 0.3 * y
        if (self.playerPitch < self.minPitch): 
            self.playerPitch = self.minPitch
        if (self.playerPitch > self.maxPitch): 
            self.playerPitch = self.maxPitch
        self.player.setP(self.playerPitch)