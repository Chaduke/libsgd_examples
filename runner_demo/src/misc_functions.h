#ifndef MISC_FUNCTIONS_H
#define MISC_FUNCTIONS_H

#include <string>
#include "sgd/sgd.h"

namespace Utils {

    SGD_Material GetCollisionMaterial();
    void UnrealMouseInput(SGD_Entity entity, float move_speed = 0.02f, float turn_speed = 0.2f);
    void DrawTextFloat(const char* prefix, float num, float x, float y);
    void DisplayLoadingMessage(const char* msg);
    
    struct Vec3 {
        float x, y, z;
        // Constructor
        Vec3(float x_val = 0, float y_val = 0, float z_val = 0) : x(x_val), y(y_val), z(z_val) {}

        Vec3& Add(const Vec3& other)
        {
            x += other.x;
            y += other.y;
            z += other.z;
            return *this;
        }
    };
    void MoveEntityVec3(SGD_Entity entity, Vec3 veolicty);
}

#endif // MISC_FUNCTIONS_H
