// main.cpp
// for RUNNER DEMO
// by Chaduke
// 20241013

// an "endless runner" type demo to demonstrate LibSGD rendering

#define SGD_DYNAMIC 1
#include "sgd/sgd.h"
#define IMGUI_IMPL_SGD_IMPLEMENTATION 1
#include "sgd/imgui_impl_sgd.h"
#include <iostream>
#include "misc_functions.h"
#include "player.h"
#include "environment.h"

int main()
{	
	sgd_Init();
	sgd_CreateWindow(1920,1080,"Runner Demo",SGD_WINDOW_FLAGS_FULLSCREEN );	
	
	// imgui init 
	IMGUI_CHECKVERSION();
	ImGui::CreateContext();
	auto& io = ImGui::GetIO();
	io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard; // Enable Keyboard Controls
	io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;  // Enable Gamepad Controls

	ImGui::StyleColorsDark();

	ImGui_ImplSGD_Init();
		
	SGD_Camera camera = sgd_CreatePerspectiveCamera();	
	SGD_Model pivot = sgd_CreateModel(0);
	sgd_SetEntityParent(camera, pivot);		
	sgd_MoveEntity(pivot, 0, 1, -5);
	
	Utils::DisplayLoadingMessage("Creating Player...");
	Player player;	
	Utils::DisplayLoadingMessage("Creating Environment...");
	Environment environment;

	std::vector<SGD_Model> grounds(3);
	for (int i = 0; i < 3; i++)
	{
		grounds[i] = environment.CreateGround();
		Utils::DisplayLoadingMessage("Adding Trees...");
		environment.AddTrees(grounds[i]);
		Utils::DisplayLoadingMessage("Adding Rocks...");
		environment.AddRocks(grounds[i]);
		Utils::DisplayLoadingMessage("Adding Turtles...");
		environment.AddTurtles(grounds[i]);
		Utils::DisplayLoadingMessage("Adding Grass...");
		environment.AddGrass(grounds[i]);
		sgd_MoveEntity(grounds[i], 0, 0, 256 * (i-1));
	}	

	sgd_EnableCollisions(1, 0, SGD_COLLISION_RESPONSE_SLIDE);
	sgd_SetMouseZ(-5);

	bool loop = true;
	bool show_demo_window = false;	
	bool show_environment_window = false;
	bool show_player_window = true;
	bool show_camera_window = false;
	
	while (loop) 
	{
		int e = sgd_PollEvents();
		if (e == SGD_EVENT_MASK_CLOSE_CLICKED) loop = false; 
		if (sgd_IsKeyHit(SGD_KEY_ESCAPE)) loop = false;
		if (sgd_IsKeyHit(SGD_KEY_F1)) 
		{
			if (show_environment_window) show_environment_window = false; else show_environment_window = true;
		}
		if (sgd_IsKeyHit(SGD_KEY_F2)) 
		{
			if (show_player_window) show_player_window = false; else show_player_window = true;
		}
		if (sgd_IsKeyHit(SGD_KEY_F3)) 
		{
			if (show_camera_window) show_camera_window = false; else show_camera_window = true;
		}	
		
		if (!show_environment_window) 
		{
			player.Update();
			sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_DISABLED);
			sgd_SetEntityPosition(camera, 0, 0, sgd_GetMouseZ());
			
			// camera positioning
			sgd_SetEntityPosition(pivot,
			sgd_GetEntityX(player.pivot),
			sgd_GetEntityY(player.pivot) + 0.5,
			sgd_GetEntityZ(player.pivot)
			);
			
			if (sgd_GetMouseZ() > 0) sgd_SetMouseZ(0);	

			if (!player.gamepad)
			{				
				if (sgd_IsKeyHit(SGD_KEY_R)) player.Run();	
				// camera rotatation with mouse
				sgd_TurnEntity(pivot, -sgd_GetMouseVY() * 0.1, -sgd_GetMouseVX() * 0.1, 0);				
			}		
			else 
			{			
				float right_x = sgd_GetGamepadAxis(0, SGD_GAMEPAD_AXIS_RIGHT_X);
				float right_y = sgd_GetGamepadAxis(0, SGD_GAMEPAD_AXIS_RIGHT_Y);
				if (!player.running) 
				{
					sgd_TurnEntity(pivot, -right_y * 0.5, -right_x, 0);
				} 
				else 
				{					
					sgd_TurnEntity(player.pivot, -right_y * 0.1, -right_x * 0.1, 0);
					sgd_SetEntityRotation(pivot,sgd_GetEntityRX(pivot),	sgd_GetEntityRY(player.pivot) -180,0);
				}
			}
			// correct roll
			if (sgd_GetEntityRZ(pivot) > 0 || sgd_GetEntityRZ(pivot) < 0) 
				sgd_SetEntityRotation(pivot,sgd_GetEntityRX(pivot),	sgd_GetEntityRY(pivot),	0);
			
			if (sgd_GetEntityRX(pivot) > 5) sgd_SetEntityRotation(pivot,5,sgd_GetEntityRY(pivot),0);
			if (sgd_GetEntityRX(pivot) < -80) sgd_SetEntityRotation(pivot,-80,sgd_GetEntityRY(pivot),0);			
			
			sgd_UpdateColliders();
		}
		else sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_NORMAL);		
		
		// in order to create an endless ground to run on	
		// test the distance of player z location with ground 1,2 and 3
		// if > 384 or < -384 move the ground 768 units
		
		for (int i=0;i<3;i++)
		{
			float distance = float(sgd_GetEntityZ(player.pivot) - sgd_GetEntityZ(grounds[i]));
			if (distance < -384) sgd_MoveEntity(grounds[i],0,0,-768);
			if (distance > 384) sgd_MoveEntity(grounds[i],0,0,768);
		}
		
		sgd_RenderScene();
		
		// imgui stuff
		ImGui_ImplSGD_NewFrame();
		ImGui::NewFrame();

		if (show_demo_window) ImGui::ShowDemoWindow(&show_demo_window);
		if (show_environment_window) environment.RenderGUI();
		if (show_player_window) player.ReportStats();
		
		if (show_camera_window) 
		{
			if (ImGui::Begin("Camera Info"))
			{	
				ImGui::Text("Pivot X,Y,Z: %.1f,%.1f,%.1f", sgd_GetEntityX(pivot), sgd_GetEntityY(pivot), sgd_GetEntityZ(pivot));
				ImGui::Text("Pivot RX,RY,RZ: %.1f,%.1f,%.1f", sgd_GetEntityRX(pivot), 
															sgd_GetEntityRY(pivot), 
															sgd_GetEntityRZ(pivot));
				ImGui::Text("Camera X,Y,Z: %.1f,%.1f,%.1f", sgd_GetEntityX(camera), sgd_GetEntityY(camera), sgd_GetEntityZ(camera));
				ImGui::Text("Camera RX,RY,RZ: %.1f,%.1f,%.1f", sgd_GetEntityRX(camera), 
															sgd_GetEntityRY(camera), 
															sgd_GetEntityRZ(camera));
			}
			ImGui::End();
		}

		ImGui::Render();
		ImGui_ImplSGD_RenderDrawData(ImGui::GetDrawData());
		
		sgd_Clear2D();
		sgd_Present();	
	}
	// Cleanup
	ImGui_ImplSGD_Shutdown();
	ImGui::DestroyContext();
	
	sgd_Terminate();
}