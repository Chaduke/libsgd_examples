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

	sgd_EnableCollisions(1, 0, SGD_COLLISION_RESPONSE_SLIDEXZ);
	sgd_SetMouseZ(-10);

	bool loop = true;
	bool show_demo_window = false;	
	bool show_environment_window = true;

	while (loop) 
	{
		int e = sgd_PollEvents();
		if (e == SGD_EVENT_MASK_CLOSE_CLICKED) loop = false; 
		if (sgd_IsKeyHit(SGD_KEY_ESCAPE)) loop = false;

		// player input 		
		if (sgd_IsKeyHit(SGD_KEY_D))
		{
			player.Dance(); 			
		}	
		if (sgd_IsKeyHit(SGD_KEY_R))
		{
			player.Run();
		}

		if (player.idle)
		{
			Utils::UnrealMouseInput(pivot);
			sgd_SetEntityPosition(camera, 0, 0, 0);			
		}
		else
		{
			sgd_SetMouseCursorMode(SGD_MOUSE_CURSOR_MODE_DISABLED);
			// camera positioning
			sgd_SetEntityPosition(pivot,
				sgd_GetEntityX(player.view_model),
				sgd_GetEntityY(player.view_model),
				sgd_GetEntityZ(player.view_model)
			);
			sgd_SetEntityPosition(camera, 0, 0, sgd_GetMouseZ());

			// camera rotatation
			sgd_TurnEntity(pivot, -sgd_GetMouseVY() * 0.2, -sgd_GetMouseVX() * 0.2, 0);
			sgd_SetEntityRotation(pivot,sgd_GetEntityRX(pivot),	sgd_GetEntityRY(pivot),	0);
		}
				
		player.ProcessAnimation();	

		sgd_UpdateColliders();
		sgd_RenderScene();
		
		// imgui stuff
		ImGui_ImplSGD_NewFrame();
		ImGui::NewFrame();

		if (show_demo_window) ImGui::ShowDemoWindow(&show_demo_window);
		if (show_environment_window) environment.RenderGUI();

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