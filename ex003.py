
#**************************************************
#*** LibSGD Examples 
#*** for the Python Programming Language
#*** https:#patreon.com/libsgd
#*** https:#github.com/blitz-research/libsgd/ 
#*** https:#skirmish-dev.net/forum/
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
	sgd.Set2DFont(font)
	#get our X-axis window center in pixels	
	center = sgd.GetWindowWidth() / 2
	# get the width of the text we are displaying and divide by two
	tw = sgd.GetTextWidth(font,text) / 2;
	# draw the text at the center of screen X-axis
	# and take into the yoffset value for Y-axis positioning
	sgd.Draw2DText(text,center - tw,yoffset)	

def display_text_right(text,font,yoffset): 
	sgd.Set2DFont(font)
	tw = sgd.GetTextWidth(font,text) + 10;
	right = sgd.GetWindowWidth() - tw;
	sgd.Draw2DText(text,right,yoffset)	

sgd.Init() 
# let's do this in fullscreen HD mode now 
sgd.CreateWindow(1920, 1080, "Example 003", sgd.WINDOW_FLAGS_FULLSCREEN)

# we no longer need to set a clear color because our skybox will cover it
# sgd.SetClearColor(0.2, 0.5, 0.9, 1.0)
environment = sgd.LoadCubeTexture("sgd://envmaps/sunnysky-cube.png",4,18)

# enable the line below to see the difference an "environment texture" makes on our scene
# for this scene I think it looks better with out it
# sgd.SetEnvTexture(environment)

# create a skybox from the environment cube texture
skybox = sgd.CreateSkybox(environment)

# blur the texture a little for better appearance
# test different values here to see what you like
sgd.SetSkyboxRoughness(skybox,0.2)

camera = sgd.CreatePerspectiveCamera()

# move our camera back a little to see all 3 cubes
sgd.MoveEntity(camera,0,0.5,-2)

# create our sun as a directional light
# the location of directional lights don't matter
# only the rotation, specifically on the X and Y axes
# will change how the light affects the scene
sun = sgd.CreateDirectionalLight()

# we need to do this to enable the light to cast shadows 
sgd.SetLightShadowsEnabled(sun,sgd.TRUE)
# we turn the light -20 degrees on X and -45 on Y
# this will cause shadows to appear in the back right of objects
# if we are looking at them straight-on from a non rotated camera	
sgd.TurnEntity(sun,-20,-45,0)

# I'm going to change the ambient light alpha to 0.1 
# so we'll only have a very dim ambience and will be able to 
# better see the shading provided by our directional light	
sgd.SetAmbientLightColor(1,1,1,0.1) 	

cube_material = sgd.LoadPBRMaterial("sgd://materials/Bricks076C_1K-JPG")    
cube_mesh = sgd.CreateBoxMesh(-0.5,-0.5,-0.5,0.5,0.5,0.5,cube_material)	
# enable the cube mesh to cast shadows on other objects
sgd.SetMeshShadowsEnabled(cube_mesh,True)
cube = sgd.CreateModel(cube_mesh)	
sgd.MoveEntity(cube,0,0.5,3)

# we can now easily create other cubes using the same mesh
cube_left = sgd.CreateModel(cube_mesh)
sgd.MoveEntity(cube_left,-2,0.5,3)
cube_right = sgd.CreateModel(cube_mesh)
sgd.MoveEntity(cube_right,2,0.5,3)

# our next object, the ground, will consist of a cube mesh
# but scaled outwards 20 units in the X and Y directions
# on only 0.1 units on the Y axis 
# before we do this however, we need a ground material
# again we will consult the LibSGD asset libary and load one up
ground_material = sgd.LoadPBRMaterial("sgd://materials/PavingStones119_1K-JPG") 	
ground_mesh = sgd.CreateBoxMesh(-20,-0.1,-20,20,0,20,ground_material)	

# this will reduce the scale of the ground material and make it look more realistic in our scene
# feel free to experiment with the values to see what happens
sgd.TFormMeshTexCoords(ground_mesh,20,20,0,0)
ground = sgd.CreateModel(ground_mesh)	

spin_speed = 1.0

# let's load some fonts from our Windows folder
# if for some reason this doesn't work for you check your 
# windows fonts folder and replace with something else 
# you have to right-click on the font and choose properties from 
# windows explorer in order to see the ".ttf" filename
# you can always fine a lot of .ttf font files on the net too
segoe_font = sgd.LoadFont("c:/Windows/Fonts/seguihis.ttf",22)
segoe_script_font = sgd.LoadFont("c:/Windows/Fonts/segoescb.ttf",30)

# start main loop
loop = True
while loop:
    # poll events and gather input 
    e = sgd.PollEvents()
    if e==sgd.EVENT_MASK_CLOSE_CLICKED: loop = False
    if sgd.IsKeyHit(sgd.KEY_ESCAPE): loop = False
    
    # let's use up and down to change the spin speed now
    # since it makes more sense to use left / right for the camera
    if sgd.IsKeyDown(sgd.KEY_DOWN): spin_speed-=0.1
    if sgd.IsKeyDown(sgd.KEY_UP): spin_speed+=0.1		
    
    # move the camera around with WASD
    # or you can alter this to your preferred keyboard layout
    if sgd.IsKeyDown(sgd.KEY_A): sgd.MoveEntity(camera,-0.1,0,0)
    if sgd.IsKeyDown(sgd.KEY_D): sgd.MoveEntity(camera,0.1,0,0)
    if sgd.IsKeyDown(sgd.KEY_W): sgd.MoveEntity(camera,0,0,0.1)
    if sgd.IsKeyDown(sgd.KEY_S): sgd.MoveEntity(camera,0,0,-0.1)	

    # we'll use left and right arrows to steer our camera now
    if sgd.IsKeyDown(sgd.KEY_LEFT): sgd.TurnEntity(camera,0,2,0)
    if sgd.IsKeyDown(sgd.KEY_RIGHT): sgd.TurnEntity(camera,0,-2,0)
    
    sgd.TurnEntity(cube,0,spin_speed,0)
    # turn the left and right cubes at different speeds
    sgd.TurnEntity(cube_left,0,spin_speed / 2,0)
    sgd.TurnEntity(cube_right,0,spin_speed * 2,0)
    
    sgd.RenderScene()
    
    # draw our 2D overlay
    sgd.Clear2D()
    
    # get our font height in pixels + some padding
    # we can subtract 
    fh = sgd.GetFontHeight(segoe_font) + 10
       
    # black text 
    sgd.Set2DTextColor(0,0,0,1)
    display_text_centered("Spinning Cubes on a Sunny Day",segoe_script_font,3)
    display_text_centered("by Chaduke",segoe_font,fh + 15)
    
    # grey text
    sgd.Set2DTextColor(0.5,0.5,0.5,1)     		
    sgd.Draw2DText("Spin Speed : " + str(spin_speed),5,5)
    
    # yellow text for the bottom of the screen
    sgd.Set2DTextColor(1,1,0,1) 
    display_text_centered("- Press Escape to Exit -",segoe_font,sgd.GetWindowHeight() - fh)	     
    
    # draw bottom center	
    sgd.Draw2DText("FPS : " + str(sgd.GetFPS()),5,sgd.GetWindowHeight() - fh)
    # draw bottom right
    display_text_right("WASD - Move Camera",segoe_font,sgd.GetWindowHeight() - fh)

    # red text for the right side 
    sgd.Set2DTextColor(1,0,0,1)
    display_text_right("Up and Down Arrows",segoe_font,3)
    display_text_right("Change Spin Speed",segoe_font,fh)
    display_text_right("Left and Right Arrows",segoe_font,fh * 2)
    display_text_right("Steer the Camera",segoe_font,fh * 3)
    sgd.Present()
    
sgd.Terminate()
