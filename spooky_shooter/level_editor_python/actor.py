# actor.py
# by Chaduke
# 20241003

# this actor class / data structure is to be used with LibSGD for "wrangling"
# the pivot entity, the view model, the collider, the collider model
# vector3 objects for velocity and acceleration

from libsgd import sgd
from functions import Vec3
        
class Actor:
    def __init__(self,actor_name,filename,view_mesh,collider_mesh,x,y,z):        
        self.pivot = sgd.createModel(0)
        sgd.setEntityName(self.pivot,actor_name) 
        self.filename = filename  
        self.view_model = sgd.createModel(view_mesh)
        sgd.setEntityParent(self.view_model,self.pivot)
        sgd.moveEntity(self.view_model,0,-1,0)
        sgd.moveEntity(self.pivot,x,y,z)
        self.collider_model = sgd.createModel(collider_mesh)
        sgd.setEntityParent(self.collider_model,self.pivot)        
        self.collider = sgd.createSphereCollider(self.pivot,1,1)
        self.velocity = Vec3(0,0,0)
        self.acceleration = Vec3(0,0,0)
        
    def update_movement(self):
        self.velocity.add(self.acceleration)
        sgd.moveEntity(self.pivot,self.velocity.x,self.velocity.y,self.velocity.z)
    