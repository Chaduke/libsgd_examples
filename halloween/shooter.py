from libsgd import sgd
import random
from math import sin

def display_text_centered(text,font,yoffset): 
	sgd.set2DFont(font)	
	center = sgd.getWindowWidth() / 2	
	tw = sgd.getTextWidth(font,text) / 2;	
	sgd.draw2DText(text,center - tw,yoffset)
    
sgd.init()
sgd.createWindow(1920,1080,"Halloween Shooter",sgd.WINDOW_FLAGS_FULLSCREEN)
camera = sgd.createPerspectiveCamera()
pivot = sgd.createModel(0)
sgd.setEntityParent(camera,pivot)
light = sgd.createDirectionalLight()
sgd.setLightColor(light,1,1,1,0.8)
sgd.setLightShadowsEnabled(light,True)
sgd.turnEntity(light,-20,-225,0)
sgd.moveEntity(pivot,0,1,-10)
sgd.setAmbientLightColor(0.5,0.5,0.5,0.2)
skybox = sgd.loadSkybox("sgd://envmaps/stormy-cube.jpg",0)

# GROUND
ground_size = 50
ground_material = sgd.loadPBRMaterial("sgd://materials/PavingStones131_1K-JPG")
ground_mesh = sgd.createBoxMesh(-ground_size,-0.1,-ground_size,ground_size,0,ground_size,ground_material)
sgd.transformTexCoords(ground_mesh,ground_size,ground_size,0,0)
sgd.setMeshShadowsEnabled(ground_mesh,True)
ground = sgd.createModel(ground_mesh)

# GRASS / WEEDS
weeds_image = sgd.loadImage("assets/textures/weeds.png")

for i in range(ground_size * 60):   
    w = sgd.createSprite(weeds_image) 
    sc = random.random() + 0.5    
    sgd.moveEntity(w, random.random() * ground_size * 2 - ground_size, sc / 2, random.random() * ground_size * 2 - ground_size)    
    sgd.setEntityScale(w,sc,sc,1)

# HALLOWEEN 3D PACK MODELS 
arch_gate = sgd.loadModel("assets/gltf/arch_gate.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(arch_gate),True)

tree_dead_large = sgd.loadModel("assets/gltf/tree_dead_large.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(tree_dead_large),True)
sgd.moveEntity(tree_dead_large,-10,0,0)

tree_dead_medium = sgd.loadModel("assets/gltf/tree_dead_medium.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(tree_dead_medium),True)
sgd.moveEntity(tree_dead_medium,-8,0,5)

tree_dead_small = sgd.loadModel("assets/gltf/tree_dead_small.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(tree_dead_small),True)
sgd.moveEntity(tree_dead_small,8,0,5)

tree_dead_large_decorated = sgd.loadModel("assets/gltf/tree_dead_large_decorated.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(tree_dead_large_decorated),True)
sgd.moveEntity(tree_dead_large_decorated,10,0,0)

bench = sgd.loadModel("assets/gltf/bench.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(bench),True)
sgd.moveEntity(bench,2,0,-3)

bench_decorated = sgd.loadModel("assets/gltf/bench_decorated.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(bench_decorated),True)
sgd.moveEntity(bench_decorated,-2,0,-3)

# BONES
bones = [sgd.loadMesh("assets/gltf/bone_A.gltf"),
sgd.loadMesh("assets/gltf/bone_B.gltf"),
sgd.loadMesh("assets/gltf/bone_C.gltf")]

for bone in bones:
    sgd.setMeshShadowsEnabled(bone,True)   

for i in range(ground_size):
    r = random.random()  
    if r > 0.66: 
        bone = sgd.createModel(bones[0])
    elif r > 0.33: 
        bone = sgd.createModel(bones[1])
    else: 
        bone = sgd.createModel(bones[2])
    sgd.moveEntity(bone, random.random() * ground_size * 2 - ground_size, 0, random.random() * ground_size * 2 - ground_size)
    sc = random.random() * 0.5 + 0.5
    sgd.scaleEntity(bone, sc,sc,sc)
    sgd.turnEntity(bone,0,random.random() * 360,0)

candle = sgd.loadModel("assets/gltf/candle.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(candle),True)
sgd.moveEntity(candle,-3,0,-5)

candle_melted = sgd.loadModel("assets/gltf/candle_melted.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(candle_melted),True)
sgd.moveEntity(candle_melted,-1,0,-5)

candle_thin = sgd.loadModel("assets/gltf/candle_thin.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(candle_thin),True)
sgd.moveEntity(candle_thin,1,0,-5)

candle_triple = sgd.loadModel("assets/gltf/candle_triple.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(candle_triple),True)
sgd.moveEntity(candle_triple,3,0,-5)

coffin = sgd.loadModel("assets/gltf/coffin.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(coffin),True)
sgd.moveEntity(coffin,-5,0,10)

coffin_decorated = sgd.loadModel("assets/gltf/coffin_decorated.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(coffin_decorated),True)
sgd.moveEntity(coffin_decorated,5,0,10)

crypt = sgd.loadModel("assets/gltf/crypt.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(crypt),True)
sgd.moveEntity(crypt,0,0,10)

# FENCE
fence_mesh = sgd.loadMesh("assets/gltf/fence.gltf")
sgd.setMeshShadowsEnabled(fence_mesh,True)

fence_broken_mesh = sgd.loadMesh("assets/gltf/fence_broken.gltf")
sgd.setMeshShadowsEnabled(fence_broken_mesh,True)

for i in range(-ground_size+2,ground_size,4):
    if random.random() > 0.9:
        fence = sgd.createModel(fence_broken_mesh)
    else:
        fence = sgd.createModel(fence_mesh)   
    sgd.setEntityPosition(fence,i,0,ground_size)
    
    if random.random() > 0.9:
        fence = sgd.createModel(fence_broken_mesh)
    else:
        fence = sgd.createModel(fence_mesh)   
    sgd.setEntityPosition(fence,i,0,-ground_size)
    
    if random.random() > 0.9:
        fence = sgd.createModel(fence_broken_mesh)
    else:
        fence = sgd.createModel(fence_mesh)   
    sgd.setEntityPosition(fence,-ground_size,0,i)
    sgd.setEntityRotation(fence,0,90,0)
    
    if random.random() > 0.9:
        fence = sgd.createModel(fence_broken_mesh)
    else:
        fence = sgd.createModel(fence_mesh)   
    sgd.setEntityPosition(fence,ground_size,0,i)
    sgd.setEntityRotation(fence,0,90,0)   

fence_pillar = sgd.loadModel("assets/gltf/fence_pillar.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(fence_pillar),True)
sgd.moveEntity(fence_pillar,-10,0,15)  

fence_pillar_broken = sgd.loadModel("assets/gltf/fence_pillar_broken.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(fence_pillar_broken),True)
sgd.moveEntity(fence_pillar_broken,-12,0,15)   

fence_gate = sgd.loadModel("assets/gltf/fence_gate.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(fence_gate),True)
sgd.moveEntity(fence_gate,10,0,15) 

fence_seperate = sgd.loadModel("assets/gltf/fence_seperate.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(fence_seperate),True)
sgd.moveEntity(fence_seperate,-10,0,17)  

fence_seperate_broken = sgd.loadModel("assets/gltf/fence_seperate_broken.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(fence_seperate_broken),True)
sgd.moveEntity(fence_seperate_broken,-12,0,17)

floor_dirt = sgd.loadModel("assets/gltf/floor_dirt.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(floor_dirt),True)
sgd.moveEntity(floor_dirt,12,0.02,18)  

floor_dirt_grave = sgd.loadModel("assets/gltf/floor_dirt_grave.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(floor_dirt_grave),True)
sgd.moveEntity(floor_dirt_grave,14,0.02,20)

floor_dirt_small = sgd.loadModel("assets/gltf/floor_dirt_small.gltf")
sgd.setMeshShadowsEnabled(sgd.getModelMesh(floor_dirt_small),True)
sgd.moveEntity(floor_dirt_small,16,0.02,22)

rock_font = sgd.loadFont("assets/fonts/rock.ttf",80)
rock_font_small = sgd.loadFont("assets/fonts/rock.ttf",26)

loop = True
cam_speed = 0.15
cam_turn = 0.15
cam_bob_angle = 0.0
jumping = False
jump_strength = 0.3
gravity = 0.01
y_vel = 0
sgd.setMouseCursorMode(3)

while loop:
    e = sgd.pollEvents()
    if e == sgd.EVENT_MASK_CLOSE_CLICKED or sgd.isKeyHit(sgd.KEY_ESCAPE) : loop = False
    
    # run forwards / backwards
    if sgd.isKeyDown(sgd.KEY_W) or sgd.isKeyDown(sgd.KEY_UP): 
        sgd.moveEntity(pivot,0,0,cam_speed)
        if not jumping : cam_bob_angle+=0.18
    elif sgd.isKeyDown(sgd.KEY_S) or sgd.isKeyDown(sgd.KEY_DOWN): 
        sgd.moveEntity(pivot,0,0,-cam_speed)
        if not jumping : cam_bob_angle-=0.18
    
    # strafe left / right    
    if sgd.isKeyDown(sgd.KEY_A) or sgd.isKeyDown(sgd.KEY_LEFT): 
        sgd.moveEntity(pivot,-cam_speed,0,0)
    elif sgd.isKeyDown(sgd.KEY_D) or sgd.isKeyDown(sgd.KEY_RIGHT): 
        sgd.moveEntity(pivot,cam_speed,0,0)
    
    # JUMP
    if sgd.isKeyHit(sgd.KEY_SPACE) or sgd.isKeyHit(sgd.KEY_RIGHT_CONTROL):
        if not jumping:
            jumping = True
            y_vel+=jump_strength
            
    # apply y-velocity and subtract gravity
    if jumping:
        sgd.moveEntity(pivot,0,y_vel,0)
        y_vel -= gravity
        
    # hitting the ground    
    if sgd.getEntityY(pivot) < 1 : 
        sgd.setEntityPosition(pivot,sgd.getEntityX(pivot),1,sgd.getEntityZ(pivot))
        jumping = False
        y_vel = 0
    
    # head bobbing
    sgd.setEntityPosition(camera,0,0.5 + sin(cam_bob_angle) * 0.1,0)
    
    sgd.turnEntity(pivot,0,-sgd.getMouseVX() * cam_turn,0)
    sgd.turnEntity(camera,-sgd.getMouseVY() * cam_turn,0,0)
    
    if sgd.getEntityRX(camera) < -10 : sgd.setEntityRotation(camera,-10,0,0)
    if sgd.getEntityRX(camera) > 20 : sgd.setEntityRotation(camera,20,0,0)
    
    if sgd.getEntityX(pivot) > ground_size-1 : sgd.setEntityPosition(pivot,ground_size-1,sgd.getEntityY(pivot),sgd.getEntityZ(pivot))
    if sgd.getEntityX(pivot) < -ground_size + 1 : sgd.setEntityPosition(pivot,-ground_size+1,sgd.getEntityY(pivot),sgd.getEntityZ(pivot))
    if sgd.getEntityZ(pivot) > ground_size-1 : sgd.setEntityPosition(pivot,sgd.getEntityX(pivot),sgd.getEntityY(pivot),ground_size-1)
    if sgd.getEntityZ(pivot) < -ground_size + 1 : sgd.setEntityPosition(pivot,sgd.getEntityX(pivot),sgd.getEntityY(pivot),-ground_size + 1)
    
    sgd.renderScene()
    # render 2D stuff
    sgd.clear2D()
    sgd.set2DTextColor(1,0.5,0,1)
    display_text_centered("Happy Halloween!!",rock_font,0)
    sgd.set2DFont(rock_font_small)
    sgd.draw2DText("FPS : " + str(int(sgd.getFPS())), 5, sgd.getWindowHeight() - 30)
    sgd.present() # swap buffers
sgd.terminate()
