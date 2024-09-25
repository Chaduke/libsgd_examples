
/**************************************************
/*** LibSGD Examples 
/*** for the C Programming Language
/*** https://patreon.com/libsgd
/*** https://github.com/blitz-research/libsgd/ 
/*** https://skirmish-dev.net/forum/
/**************************************************/

// Example 003 - Environment
// ex003.c

// This example, like example 002, picks up where the previous 
// left off.  We have a spinning cube, we can control the spin rate.
// but it's just floating out in blue space, fully lit.  
// Let's add a more realistic sky, which will also serve as a 
// background for reflections, and then add a ground for our cube 
// to cast shadows upon.  We will also need a directional light 
// to serve as the sun.

// Notes :
// As before, if you see anything that is overly confusing,
// consult the API docs, post on the forums or the Youtube 
// video comments that accompanies this lesson / example.

// Chad Dore' -Chaduke-
// 20240924
// https://www.youtube.com/chaddore
// https://www.github.com/chaduke/libsgd_examples

#include <sgd/sgd.h>
#include <stdio.h>

int main() {
	
	sgd_Init(); 
    sgd_CreateWindow(1280, 720, "Example 003", SGD_WINDOW_FLAGS_CENTERED);
	// we no longer need to set a clear color because our skybox will cover it
    // sgd_SetClearColor(0.2, 0.5, 0.9, 1.0);
	SGD_Texture environment = sgd_LoadCubeTexture("sgd://envmaps/sunnysky-cube.png",4,18);
	// sgd_SetEnvTexture(environment);
	SGD_Skybox skybox = sgd_CreateSkybox(environment);
	sgd_SetSkyboxRoughness(skybox,0.2);
	SGD_Camera camera = sgd_CreatePerspectiveCamera();
	sgd_MoveEntity(camera,0,0.5,0);
	// create our sun as a directional light
	// the location of directional lights don't matter
	// only the rotation, specifically on the X and Y axes
	// will change how the light affects the scene
	SGD_Light sun = sgd_CreateDirectionalLight();
	
	// we need to do this to enable the light to cast shadows 
	sgd_SetLightShadowsEnabled(sun,SGD_TRUE);
	// we turn the light -45 degrees on both X and Y
	// this will cause shadows to appear in the back right of objects
	// if we are looking at them straight-on from a non rotated camera	
	sgd_TurnEntity(sun,-20,-45,0);
	
	// I'm going to change the ambient light alpha to 0.1 
	// so we'll only have a very dim ambience and will be able to 
	// better see the shading provided by our directional light	
	sgd_SetAmbientLightColor(1,1,1,0.1); 	
	
    SGD_Material cube_material = sgd_LoadPBRMaterial("sgd://materials/Bricks076C_1K-JPG");    
	SGD_Mesh cube_mesh = sgd_CreateBoxMesh(-0.5,-0.5,-0.5,0.5,0.5,0.5,cube_material);	
	// enable the cube mesh to cast shadows on other objects
	sgd_SetMeshShadowsEnabled(cube_mesh,SGD_TRUE);
	SGD_Model cube = sgd_CreateModel(cube_mesh);	
	sgd_MoveEntity(cube,0,0.5,3);
	
	// our next object, the ground, will consist of a cube mesh
	// but scaled outwards 20 units in the X and Y directions
	// on only 0.1 units on the Y axis 
	// before we do this however, we need a ground material
	// again we will consult the LibSGD asset libary and load one up
	SGD_Material ground_material = sgd_LoadPBRMaterial("sgd://materials/PavingStones119_1K-JPG"); 	
	SGD_Mesh ground_mesh = sgd_CreateBoxMesh(-20,-0.1,-20,20,0,20,ground_material);	
	
	// this will reduce the scale of the ground material and make it look more realistic in our scene
	// feel free to experiment with the values to see what happens
	sgd_TFormMeshTexCoords(ground_mesh,20,20,0,0);
	SGD_Model ground = sgd_CreateModel(ground_mesh);	
	
	float spin_speed = 1.0;	
    SGD_Bool loop = SGD_TRUE;	
    while(loop) 
	{	
		int e = sgd_PollEvents();
		if (e==SGD_EVENT_MASK_CLOSE_CLICKED) loop = SGD_FALSE;
		if (sgd_IsKeyHit(SGD_KEY_ESCAPE)) loop = SGD_FALSE;
		
		if (sgd_IsKeyDown(SGD_KEY_LEFT)) spin_speed-=0.1;
		if (sgd_IsKeyDown(SGD_KEY_RIGHT)) spin_speed+=0.1;
		
		sgd_TurnEntity(cube,0,spin_speed,0);	
		
        sgd_RenderScene();
		sgd_Clear2D();
		sgd_Set2DTextColor(0,0,0,1);
		sgd_Draw2DText("Spinning cube on Sunny Day, by Chaduke, ESC to exit",5,5);		

		char buffer[30]; 
		snprintf(buffer, sizeof buffer, "FPS : %f", sgd_GetFPS());
		sgd_Draw2DText(buffer,5,sgd_GetWindowHeight() - 20);		
		
		snprintf(buffer, sizeof buffer, "Spin Speed : %f", spin_speed);
		sgd_Draw2DText(buffer,5,25);
		sgd_Present();
    }
	sgd_Terminate();
}