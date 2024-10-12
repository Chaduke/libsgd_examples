// misc_functions.h

// miscellaneous functions for halloween shooter
// until I find a better place for them 

#include <string>
#include <sstream>

SGD_Material LoadMaterialFromFolder(const char* folder_name) 
{
    SGD_Material material = sgd_CreatePBRMaterial();
	
	// albedo
    std::string full_path = std::string(folder_name) + "/albedo.png"; 
    SGD_Texture albedo_texture = sgd_Load2DTexture(full_path.c_str(),SGD_TEXTURE_FORMAT_SRGBA8,SGD_TEXTURE_FLAGS_DEFAULT); 
	sgd_SetMaterialTexture(material,"albedo",albedo_texture);
	
	// roughness
	full_path = std::string(folder_name) + "/roughness.png"; 
    SGD_Texture roughness_texture = sgd_Load2DTexture(full_path.c_str(),SGD_TEXTURE_FORMAT_SRGBA8,SGD_TEXTURE_FLAGS_DEFAULT); 
	sgd_SetMaterialTexture(material,"roughness",roughness_texture);
    return material;
}

void UnrealMouseInput(SGD_Entity entity, float move_speed=0.02, float turn_speed=0.2)
{
    if (sgd_IsMouseButtonDown(SGD_MOUSE_BUTTON_LEFT)) {		
        sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_DISABLED);  // hide and lock the cursor
        if (sgd_IsMouseButtonDown(SGD_MOUSE_BUTTON_RIGHT)) {
			// (both are held down now)
            sgd_MoveEntity(entity, sgd_GetMouseVX() * move_speed, -sgd_GetMouseVY() * move_speed, 0);
		}
        else {  
			// only left mouse button is down
            sgd_MoveEntity(entity, 0, 0, -sgd_GetMouseVY() * move_speed);
            sgd_TurnEntity(entity, 0, -sgd_GetMouseVX() * turn_speed, 0);
		}
	}
    else if (sgd_IsMouseButtonDown(SGD_MOUSE_BUTTON_RIGHT)) {  
	    // only right mouse button is down
        sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_DISABLED);
        sgd_TurnEntity(entity, -sgd_GetMouseVY() * turn_speed, -sgd_GetMouseVX() * turn_speed, 0);
	} else sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_NORMAL);  // set the mouse cursor to normal
	

    if (sgd_GetEntityRZ(entity) < 0 || sgd_GetEntityRZ(entity) > 0) 
        sgd_SetEntityRotation(entity, sgd_GetEntityRX(entity), sgd_GetEntityRY(entity), 0);	
}

void DrawTextFloat(const char* prefix, float num, float x, float y) 
{
    std::ostringstream oss;
    oss << prefix << num;
    std::string text = oss.str();
    sgd_Draw2DText(text.c_str(), x, y);
}

