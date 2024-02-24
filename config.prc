
#http://www.panda3d.org/manual/index.php/Configuring_Panda3D

window-title awais cool game

show-frame-rate-meter #t
show-occlusion
show-tex-mem

#constrained to a harmonic of 60fps (that is, 60, 30, 20, 15, 12, and so on)
sync-video 0

# windowed

4:3


# field of view of screen Y in degrees (panda default is 30)
default-fov 60

# Camera clipping distance
default-far 10000
default-near 0.01


#http://www.panda3d.org/manual/index.php/Multithreaded_Render_Pipeline
threading-model Cull/Draw

# Sound off as there are issues right now...
audio-library-name null