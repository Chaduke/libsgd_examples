from libsgd import sgd

class Environment:
    def __init__(self):
        self.env = sgd.loadCubeTexture("../../assets/textures/skybox/grimm_night.jpg",4,18)
        sgd.setEnvTexture(self.env)
        self.skybox = sgd.createSkybox(self.env)
        sgd.setEntityName(self.skybox,"Sky")
        self.light = sgd.createDirectionalLight()
        sgd.setEntityName(self.light,"Sun")
        sgd.turnEntity(self.light,-45,-45,0);
    @classmethod
    def create_environment(cls,skybox,light):
        instance = cls.__new__(cls)        
        instance.skybox = skybox
        sgd.setEntityName(instance.skybox,"Sky")
        instance.light = light
        sgd.setEntityName(instance.light,"Sun")
        return instance