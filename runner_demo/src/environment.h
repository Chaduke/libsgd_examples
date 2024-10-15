// environment.h
#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

#include "sgd/sgd.h"
#include <string>
#include <vector>
#include <nlohmann/json.hpp>

class Environment 
{
public:
    Environment();

    void Update();
    void RenderGUI();
    void SaveSettings(const std::string& file_path);
    void LoadSettings(const std::string& file_path);
    SGD_Model CreateGround();
    void AddTrees(SGD_Model ground);
    void AddGrassClump(SGD_Model ground, SGD_Model tree, const std::vector<SGD_Texture>& images);
	void AddRocks(SGD_Model ground);
    void AddTurtles(SGD_Model ground);
    void AddGrass(SGD_Model ground);
private:
    SGD_Skybox skybox;
    SGD_Light directional_light;
    float sky_roughness;
    float dl_rotation_x;
    float dl_rotation_y;
    float ambient_r;
    float ambient_g;
    float ambient_b;
    float ambient_a;
    std::string sky_texture_path;
    std::vector<SGD_Texture> foliage_textures;
};

#endif

