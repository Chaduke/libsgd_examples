#include "player.h"

Player::Player() {
    pivot = sgd_CreateModel(0);
    view_model = sgd_LoadBonedModel("assets/gltf/aj_animated.glb", true);
    sgd_SetMeshShadowsEnabled(sgd_GetModelMesh(view_model), true);
    sgd_SetEntityParent(view_model, pivot);
    SGD_Mesh collision_mesh = sgd_CreateSphereMesh(0.5, 16, 16, Utils::GetCollisionMaterial());
    collision_model = sgd_CreateModel(collision_mesh);
    sgd_SetEntityParent(collision_model, pivot);
    sgd_SetEntityVisible(collision_model, false);
    sgd_MoveEntity(pivot, 0, 0.5, 0); // prevent player from falling through the ground on game start
    sgd_MoveEntity(view_model, 0, -0.5, 0);
    collider = sgd_CreateSphereCollider(pivot, 1, 0.5);
    acceleration = Utils::Vec3(0, -0.006f, 0); // Y value is gravity
    velocity = Utils::Vec3(0, 0, -0.0095f); // Z value is run speed
    nseq = 2; // idle
    time0 = 0.0;
    time1 = 0.0;
    time0Step = 0.0;
    time1Step = 0.02f;
    blendStep = 0.05f;
    blend = 0.0;
    seq0 = 2;
    seq1 = 2;
    falling = false;
    running = false;
    sliding = false;
    dancing = false;
    jumping = false;
    idle = true;
}


void Player::Dance()
{
    if (dancing) {        
        dancing = false;
        idle = true;
        nseq = ANIM_IDLE;
    }
    else
    {
        if (idle) {
            idle = false;
            dancing = true;
            nseq = ANIM_DANCING;
        }       
    }    
}

void Player::Run()
{
    if (running)
    {
        running = false;
        idle = true;
        nseq = ANIM_IDLE;
    }
    else
    {
        if (idle || dancing)
        {
            idle = false;
            dancing = false;
            running = true;
            nseq = ANIM_RUNNING;
        }
    }
}

void Player::Move()
{
    if (running || jumping)
    {
        velocity.Add(acceleration);        
        Utils::MoveEntityVec3(pivot, velocity); 
    }
}

void Player::ProcessAnimation() {
    // Change to new anim
    if (blendStep == 0 && seq0 != nseq) {
        time0Step = 0;
        seq1 = nseq;
        time1 = 0;
        time1Step = 0.02f;
        blendStep = 0.05f;
    }

    // Update blend state
    blend = blend + blendStep;
    if (blend >= 1) {
        seq0 = seq1;
        time0 = time1;
        time0Step = time1Step;
        time1 = 0;
        time1Step = 0;
        blend = 0;
        blendStep = 0;
    }

    // Set base animation
    time0 += time0Step;
    sgd_AnimateModel(view_model, seq0, time0, SGD_ANIMATION_MODE_LOOP, 1);

    // Apply blend
    time1 += time1Step;
    sgd_AnimateModel(view_model, seq1, time1, SGD_ANIMATION_MODE_LOOP, blend);

    Move();
}

void Player::ReportStats()
{
	ImGUI::Begin();
	ImGui::End();
}