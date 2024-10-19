// halloween_shooter.cpp
// by Chaduke
// 20241012

// a Halloween themed shooter game demo
// mainly to test LibSGD scene serialization and my level editor 
// (check level_editor folder in this repo)

#define SGD_DYNAMIC 1
#include "sgd/sgd.h"
#include "misc_functions.h"
#define IMGUI_IMPL_SGD_IMPLEMENTATION 1
#include "sgd/imgui_impl_sgd.h"
#include <iostream>

int main()
{	
	sgd_Init();
	sgd_CreateWindow(1280,720,"Spooky Shooter",SGD_WINDOW_FLAGS_CENTERED);	
	
	// imgui init 
	IMGUI_CHECKVERSION();
	ImGui::CreateContext();
	auto& io = ImGui::GetIO();
	io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard; // Enable Keyboard Controls
	io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;  // Enable Gamepad Controls

	// Setup Dear ImGui style
	// ImGui::StyleColorsDark();
	ImGui::StyleColorsLight();

	ImGui_ImplSGD_Init();
	std::cout << "Loading Scene ..." << std::endl;
	sgd_LoadScene("level.json");
	std::cout << "Scene Loaded ..." << std::endl;
	
	SGD_Camera camera = sgd_CreatePerspectiveCamera();
	sgd_MoveEntity(camera,0,1,0);	
	
	// ground 
	SGD_Material ground_material = sgd_LoadPBRMaterial("sgd://misc/brownish-grass.jpg");
	SGD_Mesh ground_mesh = sgd_CreateBoxMesh(-40,-0.1f,-40,40,0,40,ground_material);	
	sgd_TransformTexCoords(ground_mesh,20,20,0,0);
	SGD_Model ground = sgd_CreateModel(ground_mesh);
	float roughness_factor = 0.5;	
	bool loop = true;
	bool show_demo_window = true;
	
	std::cout << "Init Finished..." << std::endl;
	while (loop) 
	{
		int e = sgd_PollEvents();
		if (e == SGD_EVENT_MASK_CLOSE_CLICKED) loop = false; 
		if (sgd_IsKeyHit(SGD_KEY_ESCAPE)) loop = false;
		
		Utils::UnrealMouseInput(camera);
		sgd_RenderScene();
		
		// imgui stuff
		ImGui_ImplSGD_NewFrame();
		ImGui::NewFrame();
		if (show_demo_window) ImGui::ShowDemoWindow(&show_demo_window);
		ImGui::Render();
		ImGui_ImplSGD_RenderDrawData(ImGui::GetDrawData());
		
		sgd_Present();	
	}
	// Cleanup
	ImGui_ImplSGD_Shutdown();
	ImGui::DestroyContext();
	
	sgd_Terminate();
}