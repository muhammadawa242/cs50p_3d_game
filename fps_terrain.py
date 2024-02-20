"""This class is a modification of followCamera which also inherits from TerrainCamera"""

from Panda_3d_Procedural_Terrain_Engine.src.camera import *


class FpsCamera(TerrainCamera):
    
    def __init__(self, player, terrain):
        TerrainCamera.__init__(self)

        self.terrain = terrain
        self.player = player
        
        # make camera a child of player node
        self.camNode.reparentTo(player)
        
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
        
        self.camNode.setHpr(self.player, 180,0,0)
        
        # set the camera at player's head position level
        self.camNode.setZ(self.player, 3.5)
        
        self.fixHeight()


    def fixHeight(self):
        pos = self.camNode.getPos(render)
        minZ = self.terrain.getElevation(pos.x, pos.y) + 1.2
        
        if pos.z < minZ:
            pos.z = minZ
            
        self.camNode.setPos(render, pos)