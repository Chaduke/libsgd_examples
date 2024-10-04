# level_editor
# main.py
# by Chaduke
# 20241001

from libsgd import sgd
import os 
from actor import *
import json

def display_text_centered(text,font,yoffset): 
	sgd.set2DFont(font)	
	center = sgd.getWindowWidth() / 2	
	tw = sgd.getTextWidth(font,text) / 2;	
	sgd.draw2DText(text,center - tw,yoffset)

def mouse_in_rect(x1,y1,x2,y2):
    mx = sgd.getMouseX()
    my = sgd.getMouseY()
    return (mx > x1 and mx < x2 and my > y1 and my < y2)

def generate_unique_name(base_name, existing_names):
    name = base_name
    count = 1
    while name in existing_names:
        count += 1
        name = f"{base_name} ({count})"
    return name  
    
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)    

def save_all_actors(actor_list):
    data = []
    for actor in actor_list:    
        data.append(actor.to_dict())
    save_to_json(data,"level.json")     

def load_all_actors(model_path, collision_mesh):
    data = load_from_json("level.json")
    actors = [Actor.from_dict(actor_data, model_path, collision_mesh) for actor_data in data]
    return actors
    
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
collider_mesh = sgd.createSphereMesh(1,16,16,get_collider_material())
actors = []

load_on_start = True
colliders_visible = True

if load_on_start:
    actors = load_all_actors(models_folder, collider_mesh)
    if not colliders_visible:
        for actor in actors:
            sgd.setEntityVisible(actor.collider_model,False)
                
sgd.enableCollisions(0,1,1)
collisions_on = True
transform_mode = False
picked_entity = 0

selected_image = sgd.loadImage("../assets/textures/selected.png")
sgd.setImageViewMode(selected_image,2)
selected = sgd.createSprite(selected_image)
sgd.scaleEntity(selected,10,10,1)
sgd.turnEntity(selected,90,0,0)
sgd.moveEntity(selected,0,0,-0.1)

crosshairs = sgd.loadImage("../assets/textures/crosshairs.png")

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
    
    # load level.json 
    if sgd.isKeyHit(sgd.KEY_L):
        actors = load_all_actors(models_folder, collider_mesh)
        if not colliders_visible:
            for actor in actors:
                sgd.setEntityVisible(actor.collider_model,False)
                
    # toggle transform mode
    if sgd.isKeyHit(sgd.KEY_T):
        if transform_mode:
            transform_mode = False            
        else:
            transform_mode = True            
            collisions_on = True
            
    # mouse input   
    if not model_browser:
        sgd.turnEntity(pivot,0,-sgd.getMouseVX() * cam_turn,0)
        sgd.turnEntity(camera,-sgd.getMouseVY() * cam_turn,0,0)
        if transform_mode:
            if sgd.isMouseButtonHit(0):                
                picked_collider = sgd.cameraPick(camera,sgd.getWindowWidth()/2,sgd.getWindowHeight()/2,2)
                print(f"Picked Collider = {picked_collider}")
                if picked_collider:                    
                    picked_entity = sgd.getColliderEntity(picked_collider)
                    sgd.setEntityPosition(selected,sgd.getEntityX(picked_entity),0.1,sgd.getEntityZ(picked_entity))
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
                current_actor = Actor(unique_name,current_model_string,current_mesh,collider_mesh,sgd.getEntityX(pivot),sgd.getEntityZ(pivot))
                if not colliders_visible: sgd.setEntityVisible(current_actor.collider_model,False)
                actors.append(current_actor)
                sgd.setEntityRotation(current_actor.pivot,0,sgd.getEntityRY(pivot),0)
                sgd.moveEntity(current_actor.pivot,0,0,3)            
                sgd.setEntityRotation(pivot,0,sgd.getEntityRY(pivot),0)            
                model_browser = False            
            except Exception as e:
                print(f"Error: {e}")  # Debug print
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
        sgd.draw2DText("T - Toggle Transform Mode",5,65)
        
        display_text_centered("Chaduke's Level Editor",avenir_font,0)
        if transform_mode:
            display_text_centered("(TRANSFORM MODE)",avenir_font,25)
            sgd.draw2DImage(crosshairs,sgd.getWindowWidth()/2,sgd.getWindowHeight()/2,1)
        
        if collisions_on:
            display_text_centered("Collisions ON",avenir_font,sgd.getWindowHeight()-25)
        else:
            display_text_centered("Collisions OFF",avenir_font,sgd.getWindowHeight()-25)
    sgd.present()
save_all_actors(actors)    
sgd.terminate()



