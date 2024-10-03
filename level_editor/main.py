# level_editor
# main.py
# by Chaduke
# 20241001

from libsgd import sgd
import os 
from actor import get_collider_material,Vec3,Actor

def display_text_centered(text,font,yoffset): 
	sgd.set2DFont(font)	
	center = sgd.getWindowWidth() / 2	
	tw = sgd.getTextWidth(font,text) / 2;	
	sgd.draw2DText(text,center - tw,yoffset)

def mouse_in_rect(x1,y1,x2,y2):
    mx = sgd.getMouseX()
    my = sgd.getMouseY()
    return (mx > x1 and mx < x2 and my > y1 and my < y2)
    
sgd.init()
sgd.createWindow(1920,1080,"Level Editor",sgd.WINDOW_FLAGS_FULLSCREEN)
env = sgd.loadCubeTexture("sgd://envmaps/nightsky-cube.png",4,18)
sgd.setEnvTexture(env)
skybox = sgd.createSkybox(env)

camera = sgd.createPerspectiveCamera()
pivot = sgd.createModel(0)
camera_collider = sgd.createSphereCollider(pivot,0,0.5)
sgd.setEntityParent(camera,pivot)
sgd.moveEntity(pivot,0,1,0)

light = sgd.createDirectionalLight()
sgd.setLightColor(light,0.6,0.8,1.0,0.4)
sgd.setAmbientLightColor(0.6,0.8,1.0,0.4)
sgd.setLightShadowsEnabled(light,True)
sgd.turnEntity(light,-20,-225,0)

# GROUND
ground_size = 50
ground_material = sgd.loadPBRMaterial("sgd://materials/PavingStones131_1K-JPG")
ground_mesh = sgd.createBoxMesh(-ground_size,-0.1,-ground_size,ground_size,0,ground_size,ground_material)
sgd.transformTexCoords(ground_mesh,ground_size,ground_size,0,0)
# sgd.setMeshShadowsEnabled(ground_mesh,True)
ground = sgd.createModel(ground_mesh)

avenir_font = sgd.loadFont("../assets/fonts/avenir.ttf",20)
sgd.set2DFont(avenir_font)

cam_speed = 0.15
cam_turn = 0.15
model_browser = False
models_folder = "../assets/gltf/"
model_entries = []
actors=[]
collider_mesh = sgd.createSphereMesh(1,16,16,get_collider_material())
sgd.enableCollisions(0,1,1)
collisions_on = True
colliders_visible = True

loop = True
while loop:
    e = sgd.pollEvents()
    if e == sgd.EVENT_MASK_CLOSE_CLICKED: loop = False
    if sgd.isKeyHit(sgd.KEY_ESCAPE): loop = False
    
    # show / hide the model browser
    if sgd.isKeyHit(sgd.KEY_TAB): 
        if model_browser:
            model_browser = False
        else:
            model_browser = True
            with os.scandir(models_folder) as entries:
                model_entries = [entry for entry in entries if entry.is_file() and entry.name.endswith('.gltf')]
                
    # run forwards / backwards
    if sgd.isKeyDown(sgd.KEY_W) or sgd.isKeyDown(sgd.KEY_UP): 
        sgd.moveEntity(pivot,0,0,cam_speed)        
    elif sgd.isKeyDown(sgd.KEY_S) or sgd.isKeyDown(sgd.KEY_DOWN): 
        sgd.moveEntity(pivot,0,0,-cam_speed)        
    
    # strafe left / right    
    if sgd.isKeyDown(sgd.KEY_A) or sgd.isKeyDown(sgd.KEY_LEFT): 
        sgd.moveEntity(pivot,-cam_speed,0,0)
    elif sgd.isKeyDown(sgd.KEY_D) or sgd.isKeyDown(sgd.KEY_RIGHT): 
        sgd.moveEntity(pivot,cam_speed,0,0)
    
    # toggle collider visiblity
    if sgd.isKeyHit(sgd.KEY_V):
        if colliders_visible:
            colliders_visible = False
            for actor in actors:
                sgd.setEntityVisible(actor.collider_model,False)
        else:
            colliders_visible = True
            for actor in actors:
                sgd.setEntityVisible(actor.collider_model,True)
                
    # toggle collisions_on
    if sgd.isKeyHit(sgd.KEY_C):
        if collisions_on:
            collisions_on = False
        else:
            collisions_on = True
            
    # mouse input   
    if not model_browser:
        sgd.turnEntity(pivot,0,-sgd.getMouseVX() * cam_turn,0)
        sgd.turnEntity(camera,-sgd.getMouseVY() * cam_turn,0,0)
    else:
        if sgd.isMouseButtonHit(0):
            current_mesh = sgd.loadMesh(models_folder + current_model_string)            
            sgd.setMeshShadowsEnabled(current_mesh,True)
            current_actor = Actor(current_model_string,current_mesh,collider_mesh,sgd.getEntityX(pivot),sgd.getEntityZ(pivot))
            if not colliders_visible: sgd.setEntityVisible(current_actor.collider_model,False)
            actors.append(current_actor)
            sgd.setEntityRotation(current_actor.pivot,0,sgd.getEntityRY(pivot),0)
            sgd.moveEntity(current_actor.pivot,0,0,3)            
            sgd.setEntityRotation(pivot,0,sgd.getEntityRY(pivot),0)            
            model_browser = False            
    
    if sgd.getEntityRX(camera) < -30 : sgd.setEntityRotation(camera,-30,0,0)
    if sgd.getEntityRX(camera) > 30 : sgd.setEntityRotation(camera,30,0,0)
    
    if sgd.getEntityX(pivot) > ground_size-1 : sgd.setEntityPosition(pivot,ground_size-1,sgd.getEntityY(pivot),sgd.getEntityZ(pivot))
    if sgd.getEntityX(pivot) < -ground_size + 1 : sgd.setEntityPosition(pivot,-ground_size+1,sgd.getEntityY(pivot),sgd.getEntityZ(pivot))
    if sgd.getEntityZ(pivot) > ground_size-1 : sgd.setEntityPosition(pivot,sgd.getEntityX(pivot),sgd.getEntityY(pivot),ground_size-1)
    if sgd.getEntityZ(pivot) < -ground_size + 1 : sgd.setEntityPosition(pivot,sgd.getEntityX(pivot),sgd.getEntityY(pivot),-ground_size + 1)
    if collisions_on: sgd.updateColliders()
    
    sgd.renderScene()    
    sgd.clear2D()
    if model_browser:      
        sgd.setMouseCursorMode(1)    
        y = 0
        x = 5
        max_rows = sgd.getWindowHeight() / 20 - 1
        col_width = 500
        for i,entry in enumerate(model_entries): 
            if y>=max_rows:
                y=0
                x+=col_width
            s = str(entry.name)    
            if mouse_in_rect(x,y*20,x + sgd.getTextWidth(avenir_font,s),y * 20 + sgd.getFontHeight(avenir_font)):
                sgd.set2DTextColor(1,1,0,1)
                current_model_string = s
            else:
                sgd.set2DTextColor(1,1,1,1)                
            sgd.draw2DText(s,x,y * 20)
            y+=1
        display_text_centered("MODEL BROWSER",avenir_font,sgd.getWindowHeight()-25)    
    else:
        sgd.setMouseCursorMode(3)
        sgd.draw2DText("TAB - Model Browser",5,5)
        sgd.draw2DText("V - Toggle Collider Visibility",5,25)
        sgd.draw2DText("C - Toggle Collisions",5,45)
        
        display_text_centered("Chaduke's Level Editor",avenir_font,0)
        if collisions_on:
            display_text_centered("Collisions ON",avenir_font,sgd.getWindowHeight()-25)
        else:
            display_text_centered("Collisions OFF",avenir_font,sgd.getWindowHeight()-25)
    sgd.present()
sgd.terminate()



