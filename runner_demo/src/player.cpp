#include "player.h"
#include "imgui.h"
#include <cmath>

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
    velocity = Utils::Vec3(0, 0, -0.095f); // Z value is run speed
    nseq = 2; // idle
    time0 = 0.0;
    time1 = 0.0;
    time0Step = 0.0;
    time1Step = 0.02f;
    blendStep = 0.05f;
    blend = 0.0;
    seq0 = 2;
    seq1 = 2;
	animation_speed = 1.0f;
    falling = false;
    running = false;
    sliding = false;
    dancing = false;
    jumping = false;
    idle = true;
	if (sgd_IsGamepadConnected(0)) gamepad = true; else gamepad = false;	
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
		animation_speed = 1.0f;		
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

void Player::Update()
{
	if (running || gamepad) GenshinInput();
	Move();
	HandleCollision();	
	ProcessAnimation();
}

void Player::Move()
{
    if (running || jumping)
    {
        velocity.Add(acceleration);        
        Utils::MoveEntityVec3(pivot, velocity); 
    }
}

void Player::HandleCollision()
{
	int c = sgd_GetCollisionCount(collider);
	
	if (c > 0) 
	{
		jumping = false;
		velocity.y = 0;		
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
    time0 += time0Step * animation_speed;
    sgd_AnimateModel(view_model, seq0, time0, SGD_ANIMATION_MODE_LOOP, 1);

    // Apply blend
    time1 += time1Step * animation_speed;
    sgd_AnimateModel(view_model, seq1, time1, SGD_ANIMATION_MODE_LOOP, blend);   
}

void Player::ReportStats()
{
    if (ImGui::Begin("Player Info"))
    {
        ImGui::Text("Position X,Y,Z: %.1f,%.1f,%.1f", sgd_GetEntityX(pivot), sgd_GetEntityY(pivot), sgd_GetEntityZ(pivot));
        ImGui::Text("Rotation X,Y,Z: %.1f,%.1f,%.1f", sgd_GetEntityRX(pivot), sgd_GetEntityRY(pivot), sgd_GetEntityRZ(pivot));
        ImGui::Text("Velocity: %.3f,%.3f,%.3f",velocity.x, velocity.y, velocity.z);
        ImGui::Text("Acceleration: %.3f,%.3f,%.3f", acceleration.x, acceleration.y, acceleration.z);
		ImGui::Text("Animation Speed: %f",animation_speed);
		ImGui::Text("Gamepad Connected : %d",gamepad);
    }
	ImGui::End();
}

void Player::GenshinInput() 
{	
	if (sgd_IsKeyHit(SGD_KEY_G))
	{
		if (gamepad) 
		{
			gamepad = false;
		}
		else 
		{				
			if (sgd_IsGamepadConnected(0)) gamepad = true;
		}
	}
	
	if (!gamepad) 
	{		
		if (sgd_IsKeyDown(SGD_KEY_W) || sgd_IsKeyDown(SGD_KEY_UP))
		{
			velocity.z = 0.095f;
			if(!running) Run();					
		}
		else 
		{
			// toggle running off
			if(running)
			{
				velocity.z = 0;
				Run();
			}
		}
	} 
	else // process gamepad input instead of keyboard input
	{
		float move_x = sgd_GetGamepadAxis(0,SGD_GAMEPAD_AXIS_LEFT_X);
		float move_z = sgd_GetGamepadAxis(0,SGD_GAMEPAD_AXIS_LEFT_Y);
		
		sgd_SetEntityRotation(pivot,0,Utils::GetRotationAngle(move_x,move_z),0);		
		
		float move_speed = std::max(std::abs(move_x), std::abs(move_z));
		if (move_speed > 0) 
		{			
			velocity.z = -0.095f * move_speed; // this is for movement 
			animation_speed = std::abs(move_speed); // this is for animation speed
		}
		else 
		{
			velocity.z = 0.0f;
			animation_speed = 1.0f;
		}	
		
		// nothing on the gamepad
		if (move_speed < 0.2f) 
		{
			// toggle running off
			if(running) Run();			
		}
		else 
		{
			// toggle running on
			if(!running) Run();			
		}
		
		// Right stick assists with turning
        float right_x = sgd_GetGamepadAxis(0, SGD_GAMEPAD_AXIS_RIGHT_X);
        float right_y = sgd_GetGamepadAxis(0, SGD_GAMEPAD_AXIS_RIGHT_Y);
        if (running) {
            float right_angle = Utils::GetRotationAngle(right_x, right_y);
			float rotation_angle = float(sgd_GetEntityRY(pivot));
            float blended_angle = (rotation_angle + right_angle) / 2.0f; // Blend rotation angles
            sgd_SetEntityRotation(pivot, 0, blended_angle, 0);
        }
	}	
}