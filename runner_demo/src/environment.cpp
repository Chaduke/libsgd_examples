// environment.cpp

#include "environment.h"
#include "sgd/sgd.h"
#include "imgui.h"
#include <fstream>
#include <filesystem>

namespace fs = std::filesystem;
using json = nlohmann::json;

Environment::Environment() 
    : sky_roughness(0.0f), dl_rotation_x(-20.0f), dl_rotation_y(25.0f),
      ambient_r(0.38f), ambient_g(0.33f), ambient_b(0.46f), ambient_a(0.20f),
      sky_texture_path("assets/textures/skybox/stormy.jpg") 
{
    SGD_Texture sky_texture = sgd_LoadCubeTexture(sky_texture_path.c_str(), SGD_TEXTURE_FORMAT_SRGBA8, SGD_TEXTURE_FLAGS_DEFAULT);
    sgd_SetEnvTexture(sky_texture);
    skybox = sgd_CreateSkybox(sky_texture);
    directional_light = sgd_CreateDirectionalLight();
    sgd_TurnEntity(directional_light, dl_rotation_x, dl_rotation_y, 0);
    sgd_SetAmbientLightColor(ambient_r, ambient_g, ambient_b, ambient_a);
    sgd_SetLightShadowsEnabled(directional_light, true); 
	
	// Create fog
	int fog = sgd_CreateFogEffect();
	sgd_SetFogEffectColor(fog,0.3f,0.6f,1,1);
	sgd_SetFogEffectPower(fog,10);
	
	sgd_SetConfigVar("csm.clipRange", "200");
	sgd_SetConfigVar("csm.depthBias", "0.0003");
	sgd_UpdateShadowMappingConfig();

    // Load foliage textures
    foliage_textures.push_back(sgd_LoadImage("assets/textures/foliage/grass1.png"));
    foliage_textures.push_back(sgd_LoadImage("assets/textures/foliage/grass2.png"));
    foliage_textures.push_back(sgd_LoadImage("assets/textures/foliage/weeds.png"));
    foliage_textures.push_back(sgd_LoadImage("assets/textures/foliage/daisies.png"));
    foliage_textures.push_back(sgd_LoadImage("assets/textures/foliage/wildflower_blue.png"));
    foliage_textures.push_back(sgd_LoadImage("assets/textures/foliage/wildflower_red.png"));
}

void Environment::AddTrees(SGD_Model ground) {

    SGD_Mesh tree_mesh = sgd_LoadMesh("assets/gltf/tree1.glb");
    sgd_SetMeshShadowsEnabled(tree_mesh, true);
    SGD_Mesh birch_mesh = sgd_LoadMesh("assets/gltf/birch_tree1.glb");
    sgd_SetMeshShadowsEnabled(birch_mesh, true);

    for (int i = 0; i < 80; ++i) {
        SGD_Model tree = (rand() % 2 == 0) ? sgd_CreateModel(tree_mesh) : sgd_CreateModel(birch_mesh);
        sgd_SetEntityParent(tree, ground);
        float scale = static_cast<float>(rand() % 10 + 1) / 2.0f + 0.5f;
        sgd_ScaleEntity(tree, scale, scale, scale);
        sgd_SetEntityPosition(tree, static_cast<float>(rand() % 111 - 120), 0.0f, static_cast<float>(rand() % 257 - 128));
        sgd_SetEntityRotation(tree, 0.0f, static_cast<float>(rand() % 360), 0.0f);
        AddGrassClump(ground, tree, foliage_textures);
    }

    for (int i = 0; i < 80; ++i) {
        SGD_Model tree = (rand() % 2 == 0) ? sgd_CreateModel(tree_mesh) : sgd_CreateModel(birch_mesh);
        sgd_SetEntityParent(tree, ground);
        float scale = static_cast<float>(rand() % 10 + 1) / 2.0f + 0.5f;
        sgd_ScaleEntity(tree, scale, scale, scale);
        sgd_SetEntityPosition(tree, static_cast<float>(rand() % 111 + 10), 0.0f, static_cast<float>(rand() % 257 - 128));
        sgd_SetEntityRotation(tree, 0.0f, static_cast<float>(rand() % 360), 0.0f);
        AddGrassClump(ground, tree, foliage_textures);
    }
}

void Environment::AddGrassClump(SGD_Model ground, SGD_Model tree, const std::vector<SGD_Texture>& images) {
    for (int j = 0; j < 18; ++j) {
        float rand_val = static_cast<float>(rand()) / static_cast<float>(RAND_MAX);
        int i;
        if (rand_val > 0.97) i = 5;
        else if (rand_val > 0.94) i = 4;
        else if (rand_val > 0.9) i = 3;
        else if (rand_val > 0.7) i = 1;
        else if (rand_val > 0.3) i = 2;
        else i = 0;

        SGD_Model sprite = sgd_CreateSprite(images[i]);
        sgd_SetEntityParent(sprite, ground);
        sgd_SetEntityPosition(sprite, sgd_GetEntityX(tree), 0.0f, sgd_GetEntityZ(tree));
        sgd_SetEntityRotation(sprite, 0.0f, static_cast<float>(rand() % 360), 0.0f);
        float scale = static_cast<float>(rand()) / static_cast<float>(RAND_MAX) + 1.0f;
        sgd_ScaleEntity(sprite, scale, scale, scale);
        sgd_MoveEntity(sprite, 0.0f, 0.4f, static_cast<float>(rand()) / static_cast<float>(RAND_MAX) * 1.5f);
    }
}

void Environment::AddRocks(SGD_Model ground) 
{
    SGD_Mesh rock_mesh = sgd_LoadMesh("assets/gltf/rock.glb");
    sgd_SetMeshShadowsEnabled(rock_mesh, true);

    for (int z = -128; z < 128; z+=4) {
        SGD_Model rock = sgd_CreateModel(rock_mesh);
        sgd_SetEntityParent(rock, ground);        
        sgd_SetEntityPosition(rock, static_cast<float>(rand() % 64 + 64), 0.0f, z);
        float scale = static_cast<float>(rand() % 3 + 0.5f);
        sgd_ScaleEntity(rock, scale, scale, scale);
        sgd_SetEntityRotation(rock, 0, static_cast<float>(rand() % 360), 0);
        rock = sgd_CreateModel(rock_mesh);
        sgd_SetEntityParent(rock, ground);
        sgd_SetEntityPosition(rock, -static_cast<float>(rand() % 64 + 64), 0.0f, z);
        scale = static_cast<float>(rand() % 3 + 0.5f);
        sgd_ScaleEntity(rock, scale, scale, scale);
        sgd_SetEntityRotation(rock, 0, static_cast<float>(rand() % 360), 0);
    }
}

void Environment::AddTurtles(SGD_Model ground)
{
    SGD_Mesh turtle_mesh = sgd_LoadMesh("assets/gltf/turtle.glb");
    sgd_SetMeshShadowsEnabled(turtle_mesh, true);

    for (int i = 0; i < 20; i++)  
    {
        SGD_Model turtle = sgd_CreateModel(turtle_mesh);
        sgd_SetEntityParent(turtle, ground);
        sgd_SetEntityPosition(turtle, static_cast<float>(rand() % 84 + 24), 0.0f, static_cast<float>(rand() % 256 - 128));
        float scale = static_cast<float>(rand() % 2 + 1);
        sgd_ScaleEntity(turtle, scale, scale, scale);
        sgd_SetEntityRotation(turtle, 0, static_cast<float>(rand() % 360), 0);
        turtle = sgd_CreateModel(turtle_mesh);
        sgd_SetEntityParent(turtle, ground);
        sgd_SetEntityPosition(turtle, -static_cast<float>(rand() % 84 + 24), 0.0f, static_cast<float>(rand() % 256 - 128));
        scale = static_cast<float>(rand() % 2 + 1);
        sgd_ScaleEntity(turtle, scale, scale, scale);
        sgd_SetEntityRotation(turtle, 0, static_cast<float>(rand() % 360), 0);
    }
}

void Environment::AddGrass(SGD_Model ground) {
    
    for (int i = 0; i < 1000; ++i) {
        int rand_index = rand() % 3;
        SGD_Model sprite = sgd_CreateSprite(foliage_textures[rand_index]);
        sgd_SetEntityParent(sprite, ground);
        float scale = static_cast<float>(rand() % 2 + 0.2) / 2;
        float x_pos = static_cast<float>(rand() % 148 - 128); // Rnd(-128, -20)
        float z_pos = static_cast<float>(rand() % 256 - 128); // Rnd(-128, 128)
        sgd_SetEntityPosition(sprite, x_pos, scale / 2, z_pos);
        sgd_SetEntityScale(sprite, scale, scale, scale);
    }
    for (int i = 0; i < 1000; ++i) {
        int rand_index = rand() % 3;
        SGD_Model sprite = sgd_CreateSprite(foliage_textures[rand_index]);
        sgd_SetEntityParent(sprite, ground);
        float scale = static_cast<float>(rand() % 2 + 0.2) / 2;
        float x_pos = static_cast<float>(rand() % 108 + 20); // Rnd(20, 128)
        float z_pos = static_cast<float>(rand() % 256 - 128); // Rnd(-128, 128)
        sgd_SetEntityPosition(sprite, x_pos, scale / 2, z_pos);
        sgd_SetEntityScale(sprite, scale, scale, scale);
    }
}


void Environment::Update() 
{
    sgd_SetSkyboxRoughness(skybox, sky_roughness);
    sgd_SetEntityRotation(directional_light, dl_rotation_x, dl_rotation_y, 0);
    sgd_SetAmbientLightColor(ambient_r, ambient_g, ambient_b, ambient_a);   
}

SGD_Model Environment::CreateGround() 
{    
    SGD_Material ground_material = sgd_LoadPBRMaterial("assets/materials/Ground048_1K-JPG");
    SGD_Mesh ground_mesh = sgd_CreateBoxMesh(-128, -0.1f, -128, 128, 0, 128, ground_material);
    sgd_TransformTexCoords(ground_mesh, 32, 32, 0, 0);
    SGD_Model ground_model = sgd_CreateModel(ground_mesh);
    SGD_Collider ground_collider = sgd_CreateMeshCollider(ground_model, 0, ground_mesh);
    return ground_model;
}

void Environment::RenderGUI() {
    if (ImGui::Begin("Environment Settings")) {      
        // Display the current sky texture path as read-only text
        ImGui::Text("Skybox Texture: %s", sky_texture_path.c_str());

        // Button to open a new window for selecting skybox textures
        if (ImGui::Button("Select Skybox Texture")) {
            ImGui::OpenPopup("Skybox Selector");
        }

        // Skybox Selector Popup
        if (ImGui::BeginPopup("Skybox Selector")) {
            for (const auto& entry : fs::directory_iterator("assets/textures/skybox/")) {
                if (entry.path().extension() == ".png" || entry.path().extension() == ".jpg") {
                    if (ImGui::Selectable(entry.path().filename().string().c_str())) {
                        sky_texture_path = entry.path().string();
                        SGD_Texture sky_texture = sgd_LoadCubeTexture(sky_texture_path.c_str(), SGD_TEXTURE_FORMAT_SRGBA8, SGD_TEXTURE_FLAGS_DEFAULT);
                        sgd_SetEnvTexture(sky_texture);
                        skybox = sgd_CreateSkybox(sky_texture);
                    }
                }
            }
            ImGui::EndPopup();
        }
         
        if (ImGui::SliderFloat("Sky Roughness", &sky_roughness, 0.0f, 1.0f)) Update();       
        if (ImGui::SliderFloat("Rotation X", &dl_rotation_x, -180.0f, 180.0f)) Update();
        if (ImGui::SliderFloat("Rotation Y", &dl_rotation_y, -180.0f, 180.0f)) Update(); 
        if (ImGui::ColorEdit4("Ambient Color", &ambient_r)) Update();
        
        if (ImGui::Button("Save Settings")) {
            SaveSettings("environment.json");
        }
        
        if (ImGui::Button("Load Settings")) {
            LoadSettings("environment.json");
        }

        // Add FPS counter at the bottom
        ImGui::SetCursorPosY(ImGui::GetCursorPosY() + 10); // Add some space
        ImGui::Separator();
        ImGui::Text("FPS: %.1f (ms/frame: %.3f)", ImGui::GetIO().Framerate, 1000.0f / ImGui::GetIO().Framerate);        
    }
    ImGui::End();
}

void Environment::SaveSettings(const std::string& file_path) {
    json j;
    j["sky_texture_path"] = sky_texture_path;
    j["sky_roughness"] = sky_roughness;
    j["dl_rotation_x"] = dl_rotation_x;
    j["dl_rotation_y"] = dl_rotation_y;
    j["ambient_r"] = ambient_r;
    j["ambient_g"] = ambient_g;
    j["ambient_b"] = ambient_b;
    j["ambient_a"] = ambient_a;

    std::ofstream file(file_path);
    file << j.dump(4);
}

void Environment::LoadSettings(const std::string& file_path) {
    std::ifstream file(file_path);
    if (file.is_open()) {
        json j;
        file >> j;

        sky_texture_path = j["sky_texture_path"].get<std::string>();
        sky_roughness = j["sky_roughness"].get<float>();
        dl_rotation_x = j["dl_rotation_x"].get<float>();
        dl_rotation_y = j["dl_rotation_y"].get<float>();
        ambient_r = j["ambient_r"].get<float>();
        ambient_g = j["ambient_g"].get<float>();
        ambient_b = j["ambient_b"].get<float>();
        ambient_a = j["ambient_a"].get<float>();

        // Apply loaded settings
        SGD_Texture sky_texture = sgd_LoadCubeTexture(sky_texture_path.c_str(), SGD_TEXTURE_FORMAT_SRGBA8, SGD_TEXTURE_FLAGS_DEFAULT);
        sgd_SetEnvTexture(sky_texture);
        skybox = sgd_CreateSkybox(sky_texture);
        Update();
    }
}

