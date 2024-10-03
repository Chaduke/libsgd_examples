
############################################################################
#### LibSGD Examples
#### for the Python Programming Language
#### Get LibSGD here - https://patreon.com/libsgd
#### LibSGD Github Repository - https://github.com/blitz-research/libsgd/
#### LibSGD Forums - https://libsgd.org/forum/
#### API Docs - https://skirmish-dev.net/libsgd/help/html/index.html 
###########################################################################

# Example 004 - Mouse Navigation and Basic Collision
# ex004.py

# In this example we'll start from a skeleton of example 003
# We will add mouse input to enable us to steer and look around
# this enables what we call "Fly Mode"
# we'll demonstrate how to use basic collisions
# we'll replace two of the cubes with a sphere and a cylinder
# we'll place new materials on all three of our primitives
# we'll load a different skybox and align our sunlight to it

# Notes :
# As before, if you see anything that is overly confusing,
# consult the API docs, post on the forums or the Youtube 
# video comments that accompanies this lesson / example.

# Chad Dore' -Chaduke-
# 20241003
# https://www.youtube.com/chaddore
# https://www.github.com/chaduke/libsgd.examples

from libsgd import sgd

def display_text_centered(text,font,yoffset): 
	sgd.set2DFont(font)
	#get our X-axis window center in pixels	
	center = sgd.getWindowWidth() / 2
	# get the width of the text we are displaying and divide by two
	tw = sgd.getTextWidth(font,text) / 2
	# draw the text at the center of screen X-axis
	# and take into the yoffset value for Y-axis positioning
	sgd.draw2DText(text,center - tw,yoffset)	

def display_text_right(text,font,yoffset): 
	sgd.set2DFont(font)
	tw = sgd.getTextWidth(font,text) + 10
	right = sgd.getWindowWidth() - tw
	sgd.draw2DText(text,right,yoffset)
	
sgd.init() 	
sgd.createWindow(1920, 1080, "Example 004", sgd.WINDOW_FLAGS_FULLSCREEN)

# environment setup
# load a skybox texture from the assets folder in the libsgd.examples folder
environment = sgd.loadCubeTexture("assets/textures/skybox/skyboxsun5deg.png",4,18)
sgd.setEnvTexture(environment)
skybox = sgd.createSkybox(environment)
sgd.setSkyboxRoughness(skybox,0.2)	

camera = sgd.createPerspectiveCamera()	
# create an "empty" model called pivot to help out our camera "rig"
pivot = sgd.createModel(0)

# create a basic sphere collider attached to the pivot, type 0
pivot_collider = sgd.createSphereCollider(pivot,0,0.5)

# parent the camera to this pivot and now use the pivot to control the camera
# this gives us the flexibilty of being able to move and rotate the camera
# from the pivot but then do the same to the camera independently 
# on different axes, allowing us to make corrections for certain situations
# I'll demonstrate more later on and also in videos
sgd.setEntityParent(camera,pivot)	

# when we want to move or turn the camera globally 
# we use our pivot now
sgd.moveEntity(pivot,0,0.5,-5)
sgd.turnEntity(pivot,0,-60,0)

sun = sgd.createDirectionalLight()
sgd.setLightShadowsEnabled(sun,True)

# turn the sun to match the skybox
sgd.turnEntity(sun,-5,45,0)
sgd.setAmbientLightColor(1,1,1,0.1) 	

# cube setup
cube_material = sgd.loadPBRMaterial("assets/materials/Marble021_1K-JPG")    
cube_mesh = sgd.createBoxMesh(-0.5,-0.5,-0.5,0.5,0.5,0.5,cube_material)	
sgd.setMeshShadowsEnabled(cube_mesh,True)
cube = sgd.createModel(cube_mesh)	
sgd.moveEntity(cube,0,0.5,3)	

# create a basic sphere collider attached to the cube, type 1
cube_collider = sgd.createSphereCollider(cube,1,0.5)

# sphere setup
sphere_material = sgd.loadPBRMaterial("assets/materials/Metal061A_1K-JPG")    
sphere_mesh = sgd.createSphereMesh(0.5,32,32,sphere_material)	
sgd.setMeshShadowsEnabled(sphere_mesh,True)
sphere = sgd.createModel(sphere_mesh)	
sgd.moveEntity(sphere,-2,0.5,3)

# create a basic sphere collider attached to the sphere, type 1
sphere_collider = sgd.createSphereCollider(sphere,1,0.5)

# cylinder setup
cylinder_material = sgd.loadPBRMaterial("assets/materials/Wood067_1K-JPG")    
cylinder_mesh = sgd.createCylinderMesh(1,0.5,32,cylinder_material)	
sgd.setMeshShadowsEnabled(cylinder_mesh,True)
cylinder = sgd.createModel(cylinder_mesh)	
sgd.moveEntity(cylinder,2,0.5,3)

# create a basic sphere collider attached to the cylinder, type 1
cylinder_collider = sgd.createSphereCollider(cylinder,1,0.5)

# enable collisions between type 0 (the camera pivot) and type 1 (the shape primitives)
# we'll also set this as a sliding collision response (2)
sgd.enableCollisions(0,1,2) 

# ground setup 
ground_material = sgd.loadPBRMaterial("sgd://materials/PavingStones119_1K-JPG") 	
ground_mesh = sgd.createBoxMesh(-20,-0.1,-20,20,0,20,ground_material)	
sgd.transformTexCoords(ground_mesh,20,20,0,0)
ground = sgd.createModel(ground_mesh)
    
# load fonts
segoe_font = sgd.loadFont("c:/Windows/Fonts/seguihis.ttf",22)
segoe_script_font = sgd.loadFont("c:/Windows/Fonts/segoescb.ttf",30)

spin_speed = 1.1

# make some variables to adjust camera move and rotation speed
cam_move_speed = 0.1
cam_turn_speed = 0.2

# hide and lock the mouse cursor so we can have more freedom with out mouselook
# comment out the line below to see the difference
sgd.setMouseCursorMode(3)

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
    
    # move the camera with the keyboard by moving the pivot		
    if sgd.isKeyDown(sgd.KEY_A): sgd.moveEntity(pivot,-cam_move_speed,0,0)
    if sgd.isKeyDown(sgd.KEY_D): sgd.moveEntity(pivot,cam_move_speed,0,0)
    if sgd.isKeyDown(sgd.KEY_W): sgd.moveEntity(pivot,0,0,cam_move_speed)
    if sgd.isKeyDown(sgd.KEY_S): sgd.moveEntity(pivot,0,0,-cam_move_speed)	

    # we'll use mouse to control our camera now
    # turning the pivot like this will cause the camera to "roll"
    # basically it will twist on the Z-axis, but we'll correct it afterwards		
    sgd.turnEntity(pivot,-sgd.getMouseVY() * cam_turn_speed,-sgd.getMouseVX() * cam_turn_speed,0)	
    
    # correct Z-axis roll
    # comment out the line below to see what happens without it
    sgd.setEntityRotation(pivot,sgd.getEntityRX(pivot),sgd.getEntityRY(pivot),0)
    
    # let's limit our cameras X-axis rotation from -70 to 70 to prevent gimbal lock
    # comment out the following two lines to see what happens when you face "straight up" or "straight down"
    if sgd.getEntityRX(pivot) > 70: sgd.setEntityRotation(pivot,70,sgd.getEntityRY(pivot),0)
    if sgd.getEntityRX(pivot) < -70: sgd.setEntityRotation(pivot,-70,sgd.getEntityRY(pivot),0)
    
    # prevent our camera from going below the ground 
    if sgd.getEntityY(pivot) < 0.5: sgd.setEntityPosition( pivot,sgd.getEntityX(pivot),0.5,sgd.getEntityZ(pivot) )
    
    sgd.turnEntity(cube,0,spin_speed,0)		
    sgd.turnEntity(sphere,0,spin_speed / 2,0)
    sgd.turnEntity(cylinder,0,spin_speed * 2,0)
    
    # update the colliders 
    sgd.updateColliders()
    sgd.renderScene()
    
    # draw our 2D overlay
    sgd.clear2D()
    
    # get our font height in pixels + some padding
    # we can subtract 
    fh = sgd.getFontHeight(segoe_font) + 10    
    
    # green text 
    sgd.set2DTextColor(0.1,0.9,0.2,1)
    display_text_centered("Making a Flymode Camera",segoe_script_font,3)		
    
    sgd.set2DFont(segoe_font)    	
    sgd.draw2DText("Spin Speed : " + str(spin_speed),5,5)    		
    sgd.draw2DText("CameraRX : " + str(sgd.getEntityRX(camera)),5,25)    	
    sgd.draw2DText("PivotRX : " + str(sgd.getEntityRX(pivot)),5,45)
    
    # yellow text for the bottom of the screen
    sgd.set2DTextColor(1,1,0,1) 
    display_text_centered("- Press Escape to Exit -",segoe_font,sgd.getWindowHeight() - fh)	    
    # draw bottom center	
    sgd.draw2DText("FPS : " + str(sgd.getFPS()),5,sgd.getWindowHeight() - fh)
    # draw bottom right
    display_text_right("WASD - Move Camera",segoe_font,sgd.getWindowHeight() - fh)
    display_text_right("Mouse - Steer Camera",segoe_font,sgd.getWindowHeight() - fh * 2)
    # red text for the right side 
    sgd.set2DTextColor(1,0,0,1)
    display_text_right("Up and Down Arrows",segoe_font,3)
    display_text_right("Change Spin Speed",segoe_font,fh)		
    sgd.present()
    
sgd.terminate()

