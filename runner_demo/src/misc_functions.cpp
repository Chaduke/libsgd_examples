#include "misc_functions.h"
#include <sstream>
#include "sgd/sgd.h"

namespace Utils {

    SGD_Material GetCollisionMaterial() {
        SGD_Texture texture = sgd_Load2DTexture (
            "assets/textures/yellow_grid.png", 
            SGD_TEXTURE_FORMAT_SRGBA8, 
            SGD_TEXTURE_FLAGS_DEFAULT 
        );
        SGD_Material material = sgd_CreatePBRMaterial();
        sgd_SetMaterialTexture(material, "albedo", texture);
        sgd_SetMaterialBlendMode(material, SGD_BLEND_MODE_ALPHA_BLEND);
        sgd_SetMaterialCullMode(material, SGD_CULL_MODE_NONE);
        return material;
    }

    void UnrealMouseInput(SGD_Entity entity, float move_speed, float turn_speed) {
        if (sgd_IsMouseButtonDown(SGD_MOUSE_BUTTON_LEFT)) {
            sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_DISABLED);
            if (sgd_IsMouseButtonDown(SGD_MOUSE_BUTTON_RIGHT)) {
                sgd_MoveEntity(entity, sgd_GetMouseVX() * move_speed, -sgd_GetMouseVY() * move_speed, 0);
            } else {
                sgd_MoveEntity(entity, 0, 0, -sgd_GetMouseVY() * move_speed);
                sgd_TurnEntity(entity, 0, -sgd_GetMouseVX() * turn_speed, 0);
            }
        } else if (sgd_IsMouseButtonDown(SGD_MOUSE_BUTTON_RIGHT)) {
            sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_DISABLED);
            sgd_TurnEntity(entity, -sgd_GetMouseVY() * turn_speed, -sgd_GetMouseVX() * turn_speed, 0);
        } else {
            sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_NORMAL);
        }
        
        if (sgd_GetEntityRZ(entity) != 0) {
            sgd_SetEntityRotation(entity, sgd_GetEntityRX(entity), sgd_GetEntityRY(entity), 0);
        }
    }

    void DrawTextFloat(const char* prefix, float num, float x, float y) {
        std::ostringstream oss;
        oss << prefix << num;
        std::string text = oss.str();
        sgd_Draw2DText(text.c_str(), x, y);
    }

    void DisplayLoadingMessage(const char* msg) {
        sgd_Clear2D();
        sgd_Set2DTextColor(1, 1, 0, 1);
        sgd_Draw2DText(msg, 10, 10);
        sgd_PollEvents();
        sgd_RenderScene();
        sgd_Present();
    }
    void MoveEntityVec3(SGD_Entity entity, Vec3 velocity)
    {
        sgd_MoveEntity(entity, velocity.x, velocity.y, velocity.z);
    }
    // Implement additional utility functions as needed
}
