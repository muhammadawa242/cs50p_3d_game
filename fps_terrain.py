class FpsCamera():
    def __init__(self, player):
        self.player = player
        
        # make camera a child of player node
        base.cam.reparentTo(player)
        
        # otherwise the camera and model are opposite to each other
        # Also this means pitch is now inverted. -x is now x
        base.cam.setHpr(self.player, 180,3,5)
        
        # set the camera at player's head position level
        base.cam.setPos(0.01,0.15,1.59)
        
        self.maxPitch = 50
        self.minPitch = -50
        
        
    def update(self, x, y):
        """
            Angularmovement is set along x while pitch along y. 
            Make sure that both are in accordance otherwise
            gun will have different sensitivities along x and y
        """
        
        angle_sens = 10
        relative_pitch = 40
        
        # find the new player pitch and clamp it to a reasonable range
        self.playerPitch = self.player.getP() + (angle_sens/relative_pitch) * y
        if (self.playerPitch < self.minPitch): 
            self.playerPitch = self.minPitch
        if (self.playerPitch > self.maxPitch): 
            self.playerPitch = self.maxPitch
        self.player.setP(self.playerPitch)
        
        # instead of setting yaw of the player, set angular movement for the controller 'np'
        self.player.parent.node().setAngularMovement(-angle_sens * x)