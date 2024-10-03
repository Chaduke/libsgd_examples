# actor.py
# by Chaduke
# 20241003

# this actor class / data structure is to be used with LibSGD for "wrangling"
# the pivot entity, the view model, the collider, the collider model
# vector3 objects for velocity and acceleration

from libsgd import sgd

# this returns a nice "wireframe" looking material for a collider mesh
def get_collider_material():
    texture = sgd.load2DTexture("../assets/textures/yellow_grid.png",4,18)
    material = sgd.createPBRMaterial()
    sgd.setMaterialTexture(material,"albedo",texture)
    sgd.setMaterialBlendMode(material,3) # alpha blend for transparency
    sgd.setMaterialCullMode(material,1) # no culling
    return material

class Vec3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def add(self,other):
        self.x+=other.x
        self.y+=other.y
        self.z+=other.z 
        
class Actor:
    def __init__(self,actor_name,view_mesh,collider_mesh,x,z):        
        self.pivot = sgd.createModel(0)
        sgd.setEntityName(self.pivot,actor_name)    
        self.view_model = sgd.createModel(view_mesh)
        sgd.setEntityParent(self.view_model,self.pivot)
        sgd.moveEntity(self.view_model,0,-1,0)
        sgd.moveEntity(self.pivot,x,1,z)
        self.collider_model = sgd.createModel(collider_mesh)
        sgd.setEntityParent(self.collider_model,self.pivot)
        self.collider = sgd.createSphereCollider(self.pivot,1,1)
        self.velocity = Vec3(0,0,0)
        self.acceleration = Vec3(0,0,0)
    def update_movement():
        self.velocity.add(self.acceleration)
        sgd.moveEntity(self.pivot,self.velocity.x,self.velocity.y,self.velocity.z)
		
	

