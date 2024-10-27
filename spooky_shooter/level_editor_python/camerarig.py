from libsgd import sgd

class CameraRig:
    def __init__(self):
        self.camera = sgd.createPerspectiveCamera()
        sgd.setEntityName(self.camera,"Camera");
        self.pivot = sgd.createModel(0);   
        sgd.setEntityName(self.pivot,"CameraPivot");        
        self.collider = sgd.createSphereCollider(self.pivot,0,0.5)
        sgd.setEntityParent(self.camera,self.pivot)
        sgd.moveEntity(self.pivot,0,1,0)       
        self.speed = 0.15
        self.turn = 0.15
    @classmethod
    def create_camera_rig(cls,camera,pivot):
        instance = cls.__new__(cls)
        instance.camera = camera
        sgd.setEntityName(instance.camera,"Camera");
        instance.pivot = sgd.createModel(0);   
        sgd.setEntityName(instance.pivot,"CameraPivot");        
        instance.collider = sgd.createSphereCollider(instance.pivot,0,0.5)
        sgd.setEntityParent(instance.camera,instance.pivot)
        sgd.setEntityPosition(instance.pivot,0,1,0)
        instance.speed = 0.15
        instance.turn = 0.15
        return instance    