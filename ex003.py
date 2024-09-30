
#**************************************************
#*** LibSGD Examples 
#*** for the Python Programming Language
#*** https://patreon.com/libsgd
#*** https://github.com/blitz-research/libsgd/ 
#*** https://skirmish-dev.net/forum/
#*** https://skirmish-dev.net/libsgd/help/html/sgd_8h.html
#**************************************************/

# Example 003 - Environment
# ex003.py

# This example, like example 002, picks up where the previous 
# left off.  We have a spinning cube, we can control the spin rate.
# but it's just floating out in blue space, fully lit.  
# Let's add a more realistic sky, which will also serve as a 
# background for reflections, and then add a ground for our cube 
# to cast shadows upon.  We will also need a directional light 
# to serve as the sun.

# We will also add a few extra cubes to demonstrate mesh reuse
# and also the ability to move the camera with the keyboard
# We'll add a few "helper functions" that position text on different 
# parts of the screen and make our code cleaner

# Notes :
# As before, if you see anything that is overly confusing,
# consult the API docs, post on the forums or the Youtube 
# video comments that accompanies this lesson / example.

# Chad Dore' -Chaduke-
# 20240925
# https://www.youtube.com/chaddore
# https://www.github.com/chaduke/libsgd.examples

from libsgd import sgd

def display_text_centered(text,font,yoffset): 
	sgd.set2DFont(font)
	#get our X-axis window center in pixels	
	center = sgd.getWindowWidth() / 2
	# get the width of the text we are displaying and divide by two
	tw = sgd.getTextWidth(font,text) / 2;
	# draw the text at the center of screen X-axis
	# and take into the yoffset value for Y-axis positioning
	sgd.draw2DText(text,center - tw,yoffset)	

def display_text_right(text,font,yoffset): 
	sgd.set2DFont(font)
	tw = sgd.getTextWidth(font,text) + 10;
	right = sgd.getWindowWidth() - tw;
	sgd.draw2DText(text,right,yoffset)	

sgd.init() 
# let's do this in fullscreen HD mode now 
sgd.createWindow(1920, 1080, "Example 003", sgd.WINDOW_FLAGS_FULLSCREEN)

# we no longer need to set a clear color because our skybox will cover it
# sgd.SetClearColor(0.2, 0.5, 0.9, 1.0)
environment = sgd.loadCubeTexture("sgd://envmaps/sunnysky-cube.png",4,18)

# enable the line below to see the difference an "environment texture" makes on our scene
# for this scene I think it looks better with out it
# sgd.SetEnvTexture(environment)

# create a skybox from the environment cube texture
skybox = sgd.createSkybox(environment)

# blur the texture a little for better appearance
# test different values here to see what you like
sgd.setSkyboxRoughness(skybox,0.2)

camera = sgd.createPerspectiveCamera()

# move our camera back a little to see all 3 cubes
sgd.moveEntity(camera,0,0.5,-2)

# create our sun as a directional light
# the location of directional lights don't matter
# only the rotation, specifically on the X and Y axes
# will change how the light affects the scene
sun = sgd.createDirectionalLight()

# we need to do this to enable the light to cast shadows 
sgd.setLightShadowsEnabled(sun,True)
# we turn the light -20 degrees on X and -45 on Y
# this will cause shadows to appear in the back right of objects
# if we are looking at them straight-on from a non rotated camera	
sgd.turnEntity(sun,-20,-45,0)

# I'm going to change the ambient light alpha to 0.1 
# so we'll only have a very dim ambience and will be able to 
# better see the shading provided by our directional light	
sgd.setAmbientLightColor(1,1,1,0.1) 	

cube_material = sgd.loadPBRMaterial("sgd://materials/Bricks076C_1K-JPG")    
cube_mesh = sgd.createBoxMesh(-0.5,-0.5,-0.5,0.5,0.5,0.5,cube_material)	
# enable the cube mesh to cast shadows on other objects
sgd.setMeshShadowsEnabled(cube_mesh,True)
cube = sgd.createModel(cube_mesh)	
sgd.moveEntity(cube,0,0.5,3)

# we can now easily create other cubes using the same mesh
cube_left = sgd.createModel(cube_mesh)
sgd.moveEntity(cube_left,-2,0.5,3)
cube_right = sgd.createModel(cube_mesh)
sgd.moveEntity(cube_right,2,0.5,3)

# our next object, the ground, will consist of a cube mesh
# but scaled outwards 20 units in the X and Y directions
# on only 0.1 units on the Y axis 
# before we do this however, we need a ground material
# again we will consult the LibSGD asset libary and load one up
ground_material = sgd.loadPBRMaterial("sgd://materials/PavingStones119_1K-JPG") 	
ground_mesh = sgd.createBoxMesh(-20,-0.1,-20,20,0,20,ground_material)	

# this will reduce the scale of the ground material and make it look more realistic in our scene
# feel free to experiment with the values to see what happens
sgd.transformTexCoords(ground_mesh,20,20,0,0)
ground = sgd.createModel(ground_mesh)	

spin_speed = 1.0

# let's load some fonts from our Windows folder
# if for some reason this doesn't work for you check your 
# windows fonts folder and replace with something else 
# you have to right-click on the font and choose properties from 
# windows explorer in order to see the ".ttf" filename
# you can always fine a lot of .ttf font files on the net too
segoe_font = sgd.loadFont("c:/Windows/Fonts/seguihis.ttf",22)
segoe_script_font = sgd.loadFont("c:/Windows/Fonts/segoescb.ttf",30)

# start main loop
loop = True
while loop:
    # poll events and gather input 
    e = sgd.pollEvents()
    if e==sgd.EVENT_MASK_CLOSE_CLICKED: loop = False
    if sgd.isKeyHit(sgd.KEY_ESCAPE): loop = False
    
    # let's use up and down to change the spin speed now
    # since it makes more sense to use left / right for the camera
    if sgd.isKeyDown(sgd.KEY_DOWN): spin_speed-=0.1
    if sgd.isKeyDown(sgd.KEY_UP): spin_speed+=0.1		
    
    # move the camera around with WASD
    # or you can alter this to your preferred keyboard layout
    if sgd.isKeyDown(sgd.KEY_A): sgd.moveEntity(camera,-0.1,0,0)
    if sgd.isKeyDown(sgd.KEY_D): sgd.moveEntity(camera,0.1,0,0)
    if sgd.isKeyDown(sgd.KEY_W): sgd.moveEntity(camera,0,0,0.1)
    if sgd.isKeyDown(sgd.KEY_S): sgd.moveEntity(camera,0,0,-0.1)	

    # we'll use left and right arrows to steer our camera now
    if sgd.isKeyDown(sgd.KEY_LEFT): sgd.turnEntity(camera,0,2,0)
    if sgd.isKeyDown(sgd.KEY_RIGHT): sgd.turnEntity(camera,0,-2,0)
    
    sgd.turnEntity(cube,0,spin_speed,0)
    # turn the left and right cubes at different speeds
    sgd.turnEntity(cube_left,0,spin_speed / 2,0)
    sgd.turnEntity(cube_right,0,spin_speed * 2,0)
    
    sgd.renderScene()
    
    # draw our 2D overlay
    sgd.clear2D()
    
    # get our font height in pixels + some padding
    # we can subtract 
    fh = sgd.getFontHeight(segoe_font) + 10
       
    # black text 
    sgd.set2DTextColor(0,0,0,1)
    display_text_centered("Spinning Cubes on a Sunny Day",segoe_script_font,3)
    display_text_centered("by Chaduke",segoe_font,fh + 15)
    
    # grey text
    sgd.set2DTextColor(0.5,0.5,0.5,1)     		
    sgd.draw2DText("Spin Speed : " + str(spin_speed),5,5)
    
    # yellow text for the bottom of the screen
    sgd.set2DTextColor(1,1,0,1) 
    display_text_centered("- Press Escape to Exit -",segoe_font,sgd.getWindowHeight() - fh)	     
    
    # draw bottom center	
    sgd.draw2DText("FPS : " + str(sgd.getFPS()),5,sgd.getWindowHeight() - fh)
    # draw bottom right
    display_text_right("WASD - Move Camera",segoe_font,sgd.getWindowHeight() - fh)

    # red text for the right side 
    sgd.set2DTextColor(1,0,0,1)
    display_text_right("Up and Down Arrows",segoe_font,3)
    display_text_right("Change Spin Speed",segoe_font,fh)
    display_text_right("Left and Right Arrows",segoe_font,fh * 2)
    display_text_right("Steer the Camera",segoe_font,fh * 3)
    sgd.present()
    
sgd.terminate()
