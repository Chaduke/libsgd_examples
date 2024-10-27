# level_editor
# main.py
# by Chaduke
# 20241001

from libsgd import sgd
import os, random
from math import floor
from actor import *
from functions import *
from environment import *
from camerarig import *

# delete an actor from the actors list 
def delete_actor(selected_actor_name):
    global actors  # Ensure we're modifying the global actors list
    
    for actor in actors:
        if sgd.getEntityName(actor.pivot) == selected_actor_name:
            # Release LibSGD resources       
            sgd.releaseHandle(actor.collider)
            sgd.destroyEntity(actor.collider_model)
            sgd.destroyEntity(actor.view_model)
            sgd.destroyEntity(actor.pivot)
            
            # Remove from actors list
            actors.remove(actor)
            del actor  # Ensure the actor is removed from memory
            print(f"Deleted : {selected_actor_name}")
            break
   
sgd.init()
sgd.createWindow(1366,768,"LibSGD Level Editor",sgd.WINDOW_FLAGS_CENTERED)

load_on_start = False
save_on_close = False

if load_on_start:
    sgd.loadScene("../../assets/levels/spooky_shooter_1.json")
    sun = sgd.findEntityChild(0,"Sun")
    sky = sgd.findEntityChild(0,"Sky")
    env = Environment.create_environment(sky,sun)    
    p = sgd.findEntityChild(0,"CameraPivot")
    c = sgd.getEntityChild(p,0)
    cam = CameraRig.create_camera_rig(c,p)    
else:
    env = Environment()
    cam = CameraRig()
    ground = sgd.loadModel("../../assets/gltf/ground50m.glb")

avenir_font = sgd.loadFont("../../assets/fonts/avenir.ttf",20)
year_font = sgd.loadFont("../../assets/fonts/year.ttf",26)
sgd.set2DFont(avenir_font)

model_browser = False
models_folder = "../../assets/gltf/"
model_entries = []
actors = []
collider_mesh = sgd.createSphereMesh(1,16,16,get_collider_material())
                
collisions_on = False
colliders_visible = False
picked_entity = 0
topdown_mode = False

transform_move = True
transform_edit = False
transform_rotate = False
transform_scale = False

selected_image = sgd.loadImage("../../assets/textures/selected.png")
sgd.setImageViewMode(selected_image,2)
selected = sgd.createSprite(selected_image)
sgd.scaleEntity(selected,5,5,1)
sgd.turnEntity(selected,90,0,0)
sgd.moveEntity(selected,0,0,-0.1)

crosshairs = sgd.loadImage("../../assets/textures/crosshairs.png")
ground_size = 50

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
                model_entries = [entry for entry in entries if entry.is_file() and (entry.name.endswith('.gltf') or entry.name.endswith('.glb'))]
                
    # move the selected object    
    if transform_move and picked_entity and sgd.isKeyDown(sgd.KEY_LEFT_SHIFT):
        if sgd.isKeyHit(sgd.KEY_A):
            sgd.setEntityRotation(picked_entity,0,0,0)            
            if sgd.isKeyDown(sgd.KEY_LEFT_CONTROL):
                sgd.moveEntity(picked_entity,-0.1,0,0)
            else:
                # make sure we're to a 1 unit grid
                current_x = sgd.getEntityX(picked_entity)
                if current_x != floor(current_x):
                    sgd.setEntityPosition(picked_entity,floor(current_x),sgd.getEntityY(picked_entity),sgd.getEntityZ(picked_entity))                
                sgd.moveEntity(picked_entity,-1,0,0)                
            sgd.setEntityPosition(selected,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity)-0.9,sgd.getEntityZ(picked_entity)) 
        if sgd.isKeyHit(sgd.KEY_D):
            sgd.setEntityRotation(picked_entity,0,0,0)
            if sgd.isKeyDown(sgd.KEY_LEFT_CONTROL):
                sgd.moveEntity(picked_entity,0.1,0,0)
            else:
                # make sure we're to a 1 unit grid
                current_x = sgd.getEntityX(picked_entity)
                if current_x != floor(current_x):
                    sgd.setEntityPosition(picked_entity,floor(current_x),sgd.getEntityY(picked_entity),sgd.getEntityZ(picked_entity))                
                sgd.moveEntity(picked_entity,1,0,0)                
            sgd.setEntityPosition(selected,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity)-0.9,sgd.getEntityZ(picked_entity)) 
        if sgd.isKeyHit(sgd.KEY_W):
            sgd.setEntityRotation(picked_entity,0,0,0)
            if sgd.isKeyDown(sgd.KEY_LEFT_CONTROL):
                sgd.moveEntity(picked_entity,0,0,0.1)
            else:    
                current_z = sgd.getEntityZ(picked_entity)
                # make sure we're to a 1 unit grid
                if current_z != floor(current_z):
                    sgd.setEntityPosition(picked_entity,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity),floor(current_z))
                sgd.moveEntity(picked_entity,0,0,1)
            sgd.setEntityPosition(selected,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity)-0.9,sgd.getEntityZ(picked_entity)) 
        if sgd.isKeyHit(sgd.KEY_S):            
            sgd.setEntityRotation(picked_entity,0,0,0)
            if sgd.isKeyDown(sgd.KEY_LEFT_CONTROL):
                    sgd.moveEntity(picked_entity,0,0,-0.1)
            else:        
                current_z = sgd.getEntityZ(picked_entity)
                # make sure we're to a 1 unit grid
                if current_z != floor(current_z):
                    sgd.setEntityPosition(picked_entity,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity),floor(current_z))
                sgd.moveEntity(picked_entity,0,0,-1)
            sgd.setEntityPosition(selected,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity)-0.9,sgd.getEntityZ(picked_entity))            
        if sgd.isKeyHit(sgd.KEY_Q):                  
            sgd.moveEntity(picked_entity,0,0.1,0)
            sgd.setEntityPosition(selected,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity)-0.9,sgd.getEntityZ(picked_entity))             
        if sgd.isKeyHit(sgd.KEY_E):
            sgd.moveEntity(picked_entity,0,-0.1,0)
            sgd.setEntityPosition(selected,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity)-0.9,sgd.getEntityZ(picked_entity)) 
    else:        
        # run forwards / backwards           
        if sgd.isKeyDown(sgd.KEY_W) or sgd.isKeyDown(sgd.KEY_UP): 
            if topdown_mode:
                sgd.moveEntity(cam.pivot,0,cam.speed*2,0)
            else:
                sgd.moveEntity(cam.pivot,0,0,cam.speed)
                
        elif sgd.isKeyDown(sgd.KEY_S) or sgd.isKeyDown(sgd.KEY_DOWN): 
            if topdown_mode:
                sgd.moveEntity(cam.pivot,0,-cam.speed*2,0)
            else:
                sgd.moveEntity(cam.pivot,0,0,-cam.speed)
        
        # strafe left / right    
        if sgd.isKeyDown(sgd.KEY_A) or sgd.isKeyDown(sgd.KEY_LEFT): 
            if topdown_mode:
                sgd.moveEntity(cam.pivot,-cam.speed*2,0,0)
            else:
                sgd.moveEntity(cam.pivot,-cam.speed,0,0)
        elif sgd.isKeyDown(sgd.KEY_D) or sgd.isKeyDown(sgd.KEY_RIGHT):
            if topdown_mode:
                sgd.moveEntity(cam.pivot,cam.speed*2,0,0)
            else:
                sgd.moveEntity(cam.pivot,cam.speed,0,0)
        
        # move up / down   
        if sgd.isKeyDown(sgd.KEY_Q):           
            sgd.moveEntity(cam.pivot,0,cam.speed,0)
        elif sgd.isKeyDown(sgd.KEY_E):            
            sgd.moveEntity(cam.pivot,0,-cam.speed,0)
    
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
            
    # toggle transform mode or topdown mode
    if sgd.isKeyHit(sgd.KEY_T):
        if sgd.isKeyDown(sgd.KEY_LEFT_SHIFT):
            if topdown_mode:
                topdown_mode = False
                sgd.setEntityPosition(cam.pivot,saved_x,saved_y,saved_z)
                sgd.setEntityRotation(cam.pivot,saved_rx,saved_ry,saved_rz)                
            else:
                topdown_mode = True
                saved_x = sgd.getEntityX(cam.pivot)
                saved_y = sgd.getEntityY(cam.pivot)
                saved_z = sgd.getEntityZ(cam.pivot)
                saved_rx = sgd.getEntityRX(cam.pivot)
                saved_ry = sgd.getEntityRY(cam.pivot)
                saved_rz = sgd.getEntityRZ(cam.pivot)
                sgd.setEntityRotation(cam.pivot,-90,0,0)
                sgd.setEntityPosition(cam.pivot,saved_x,120,saved_z)
        else:        
            if transform_move:
                transform_move = False            
            else:
                transform_move = True            
                collisions_on = True
                
    if sgd.isKeyHit(sgd.KEY_U):
        if transform_edit:
            transform_edit = False            
        else:
            transform_edit = True
            
    # save scene to the monster shooter folder         
    if sgd.isKeyHit(sgd.KEY_I):
        sgd.destroyEntity(cam.camera)    
        sgd.destroyEntity(selected)
        sgd.saveScene("../../assets/levels/spooky_shooter_1.json")
        loop = False
        
    # mouse input   
    if not model_browser:
        if not topdown_mode and not transform_edit:
            sgd.turnEntity(cam.pivot,0,-sgd.getMouseVX() * cam.turn,0)
            sgd.turnEntity(cam.camera,-sgd.getMouseVY() * cam.turn,0,0)
        if transform_move:
            if sgd.isMouseButtonHit(0):                
                picked_collider = sgd.cameraPick(cam.camera,sgd.getWindowWidth()/2,sgd.getWindowHeight()/2,2)
                print(f"Picked Collider = {picked_collider}")
                if picked_collider:                    
                    picked_entity = sgd.getColliderEntity(picked_collider)
                    for actor in actors:
                        if sgd.getEntityName(actor.pivot) == sgd.getEntityName(picked_entity):
                            picked_actor = actor
                            break
                    sgd.setEntityPosition(selected,sgd.getEntityX(picked_entity),sgd.getEntityY(picked_entity)-0.9,sgd.getEntityZ(picked_entity))
                else:
                    sgd.setEntityPosition(selected,sgd.getEntityX(selected),-0.1,sgd.getEntityZ(selected))    
            if picked_entity:
                # Check for Delete key press
                if sgd.isKeyHit(sgd.KEY_DELETE):
                    selected_actor_name = sgd.getEntityName(picked_entity) 
                    print(f"Deleting Actor : {selected_actor_name}") 
                    delete_actor(selected_actor_name)    
                    picked_entity = 0
                    picked_collider = 0                    
                    sgd.setEntityPosition(selected,sgd.getEntityX(selected),-0.1,sgd.getEntityZ(selected)) 
    else:
        # load model from disk
        if sgd.isMouseButtonHit(0):            
            try:                
                current_mesh = sgd.loadMesh(models_folder + current_model_string)
                if not current_mesh:
                    raise Exception("Failed to load mesh")                
                sgd.setMeshShadowsEnabled(current_mesh,True)
                # check actors list for existing name
                existing_strings = []                
                for actor in actors:
                    existing_strings.append(sgd.getEntityName(actor.pivot))                    
                unique_name = generate_unique_name(current_model_string,existing_strings)
                print (f"Unique Name : {unique_name}")
                current_actor = Actor(unique_name,current_model_string,current_mesh,collider_mesh,sgd.getEntityX(cam.pivot),1,sgd.getEntityZ(cam.pivot))
                if not colliders_visible: sgd.setEntityVisible(current_actor.collider_model,False)
                actors.append(current_actor)
                sgd.setEntityRotation(current_actor.pivot,0,sgd.getEntityRY(cam.pivot),0)
                sgd.moveEntity(current_actor.pivot,0,0,3)            
                sgd.setEntityRotation(cam.pivot,0,sgd.getEntityRY(cam.pivot),0)            
                model_browser = False            
            except Exception as e:
                print(f"Error: {e}")  # Debug print   
    
    if not topdown_mode:
        if sgd.getEntityRX(cam.camera) < -30 : sgd.setEntityRotation(cam.camera,-30,0,0)
        if sgd.getEntityRX(cam.camera) > 30 : sgd.setEntityRotation(cam.camera,30,0,0)
        if sgd.getEntityX(cam.pivot) > ground_size-1 : sgd.setEntityPosition(cam.pivot,ground_size-1,sgd.getEntityY(cam.pivot),sgd.getEntityZ(cam.pivot))
        if sgd.getEntityX(cam.pivot) < -ground_size + 1 : sgd.setEntityPosition(cam.pivot,-ground_size+1,sgd.getEntityY(cam.pivot),sgd.getEntityZ(cam.pivot))
        if sgd.getEntityZ(cam.pivot) > ground_size-1 : sgd.setEntityPosition(cam.pivot,sgd.getEntityX(cam.pivot),sgd.getEntityY(cam.pivot),ground_size-1)
        if sgd.getEntityZ(cam.pivot) < -ground_size + 1 : sgd.setEntityPosition(cam.pivot,sgd.getEntityX(cam.pivot),sgd.getEntityY(cam.pivot),-ground_size + 1)
        
    if collisions_on: sgd.updateColliders()
    
    sgd.renderScene()    
    sgd.clear2D()
    sgd.set2DTextColor(1,1,1,1)  
    if model_browser:      
        sgd.setMouseCursorMode(1)    
        y = 0
        x = 5
        max_rows = sgd.getWindowHeight() / 20 - 2
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
        sgd.set2DTextColor(1.0,0,0,1.0)
        display_text_centered("- MODEL BROWSER -",avenir_font,sgd.getWindowHeight()-25)    
    else:
        if not transform_edit : sgd.setMouseCursorMode(3)
        sgd.draw2DText("TAB - Model Browser",5,5)
        sgd.draw2DText("V - Toggle Collider Visibility",5,25)
        sgd.draw2DText("C - Toggle Collisions",5,45)
        sgd.draw2DText("T - Toggle Transform Mode",5,65)
        sgd.draw2DText("SHIFT+T - Toggle Topdown Mode",5,85)
        
        display_text_centered("LibSGD Level Editor",year_font,0)
        if transform_move:
            if transform_edit:
                display_text_centered("(TRANSFORM - EDIT)",avenir_font,25)
                sgd.setMouseCursorMode(1)
            else:
                sgd.setMouseCursorMode(3)
                display_text_centered("(TRANSFORM - MOVE)",avenir_font,25)
                sgd.draw2DImage(crosshairs,sgd.getWindowWidth()/2,sgd.getWindowHeight()/2,1)
        
        if collisions_on:
            display_text_centered("Collisions ON",avenir_font,sgd.getWindowHeight()-25)
        else:
            display_text_centered("Collisions OFF",avenir_font,sgd.getWindowHeight()-25)
            
        if picked_entity:
            display_text_right(sgd.getEntityName(picked_actor.pivot),avenir_font,5)
            display_text_right(f"Position : {sgd.getEntityX(picked_actor.pivot):.1f},{sgd.getEntityY(picked_actor.pivot):.1f},{sgd.getEntityZ(picked_actor.pivot):.1f}",avenir_font,25)
            display_text_right(f"Rotation : {sgd.getEntityRX(picked_actor.pivot):.1f},{sgd.getEntityRY(picked_actor.pivot):.1f},{sgd.getEntityRZ(picked_actor.pivot):.1f}",avenir_font,45)
            display_text_right(f"Scale : {sgd.getEntitySX(picked_actor.pivot):.1f},{sgd.getEntitySY(picked_actor.pivot):.1f},{sgd.getEntitySZ(picked_actor.pivot):.1f}",avenir_font,65) 
            
            if mouse_in_rect(sgd.getWindowWidth() - 100,85,sgd.getWindowWidth(),105):
                sgd.set2DTextColor(1,1,0,1)                
                if sgd.isMouseButtonHit(0):
                    if sgd.isEntityVisible(picked_actor.view_model):
                        sgd.setEntityVisible(picked_actor.view_model,False)
                    else:
                        sgd.setEntityVisible(picked_actor.view_model,True)
            else:
                sgd.set2DTextColor(1,1,1,1)               
            display_text_right(f"Visible : {sgd.isEntityVisible(picked_actor.view_model)}",avenir_font,85) 
            
            if mouse_in_rect(sgd.getWindowWidth() - 100,105,sgd.getWindowWidth(),125):
                sgd.set2DTextColor(1,1,0,1)                
                if sgd.isMouseButtonHit(0):
                    if sgd.isEntityEnabled(picked_actor.pivot):
                        sgd.setEntityEnabled(picked_actor.pivot,False)
                    else:
                        sgd.setEntityEnabled(picked_actor.pivot,True)
            else:
                sgd.set2DTextColor(1,1,1,1)  
            display_text_right(f"Enabled : {sgd.isEntityEnabled(picked_actor.pivot)}",avenir_font,105)
    sgd.present()
sgd.destroyEntity(selected);
if save_on_close: sgd.saveScene("../../assets/levels/spooky_shooter_1.json")
sgd.terminate()



