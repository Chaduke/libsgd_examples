# level_editor
# main.py
# by Chaduke
# 20241001

from libsgd import sgd
import os 

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
skybox = sgd.loadSkybox("sgd://envmaps/nightsky-cube.png",0.1)
camera = sgd.createPerspectiveCamera()
pivot = sgd.createModel(0)
sgd.setEntityParent(camera,pivot)
sgd.moveEntity(pivot,0,0.5,0)

light = sgd.createDirectionalLight()
sgd.setLightColor(light,0.6,0.8,1.0,0.4)
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

loop = True
while loop:
    e = sgd.pollEvents()
    if e == sgd.EVENT_MASK_CLOSE_CLICKED: loop = False
    if sgd.isKeyHit(sgd.KEY_ESCAPE): loop = False
    
    # show / hide the model browser
    if sgd.isKeyHit(sgd.KEY_F2): 
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
    
    # mouse input   
    if not model_browser:
        sgd.turnEntity(pivot,0,-sgd.getMouseVX() * cam_turn,0)
        sgd.turnEntity(camera,-sgd.getMouseVY() * cam_turn,0,0)
    else:
        if sgd.isMouseButtonHit(0):
            current_model = sgd.loadModel(models_folder + current_model_string)
            sgd.setMeshShadowsEnabled(sgd.getModelMesh(current_model),True)
            sgd.setEntityPosition(current_model,sgd.getEntityX(pivot),0,sgd.getEntityZ(pivot))
            sgd.setEntityRotation(current_model,0,sgd.getEntityRY(pivot),0)
            sgd.setEntityRotation(pivot,0,sgd.getEntityRY(pivot),0)
            sgd.moveEntity(current_model,0,0,3)
            model_browser = False            
    
    if sgd.getEntityRX(camera) < -30 : sgd.setEntityRotation(camera,-30,0,0)
    if sgd.getEntityRX(camera) > 30 : sgd.setEntityRotation(camera,30,0,0)
    
    if sgd.getEntityX(pivot) > ground_size-1 : sgd.setEntityPosition(pivot,ground_size-1,sgd.getEntityY(pivot),sgd.getEntityZ(pivot))
    if sgd.getEntityX(pivot) < -ground_size + 1 : sgd.setEntityPosition(pivot,-ground_size+1,sgd.getEntityY(pivot),sgd.getEntityZ(pivot))
    if sgd.getEntityZ(pivot) > ground_size-1 : sgd.setEntityPosition(pivot,sgd.getEntityX(pivot),sgd.getEntityY(pivot),ground_size-1)
    if sgd.getEntityZ(pivot) < -ground_size + 1 : sgd.setEntityPosition(pivot,sgd.getEntityX(pivot),sgd.getEntityY(pivot),-ground_size + 1)
        
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
    else:
        sgd.setMouseCursorMode(3)
        sgd.draw2DText("F2 - Model Browser",5,5)
        display_text_centered("Chaduke's Level Editor",avenir_font,0)
    
    sgd.renderScene()
    sgd.present()
sgd.terminate()



