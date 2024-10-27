from libsgd import sgd

class Vec3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def add(self,other):
        self.x+=other.x
        self.y+=other.y
        self.z+=other.z 

# this returns a nice "wireframe" looking material for a collider mesh
def get_collider_material():
    texture = sgd.load2DTexture("../../assets/textures/yellow_grid.png",4,18)
    material = sgd.createPBRMaterial()
    sgd.setMaterialTexture(material,"albedo",texture)
    sgd.setMaterialBlendMode(material,3) # alpha blend for transparency
    sgd.setMaterialCullMode(material,1) # no culling
    return material

def generate_unique_name(base_name, existing_names):
    name = base_name
    count = 1
    while name in existing_names:
        count += 1
        name = f"{base_name} ({count})"
    return name
    
def display_text_centered(text,font,yoffset): 
	sgd.set2DFont(font)	
	center = sgd.getWindowWidth()/2	
	tw = sgd.getTextWidth(font,text)/2;	
	sgd.draw2DText(text,center - tw,yoffset)
    
def display_text_right(text,font,yoffset): 
	sgd.set2DFont(font)
	tw = sgd.getTextWidth(font,text) + 10
	right = sgd.getWindowWidth() - tw
	sgd.draw2DText(text,right,yoffset)
	
def mouse_in_rect(x1,y1,x2,y2):
    mx = sgd.getMouseX()
    my = sgd.getMouseY()
    return (mx > x1 and mx < x2 and my > y1 and my < y2)