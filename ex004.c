
/**************************************************
/*** LibSGD Examples 
/*** for the C Programming Language
/*** https://patreon.com/libsgd
/*** https://github.com/blitz-research/libsgd/ 
/*** https://libsgd.org/forum/
/*** https://skirmish-dev.net/libsgd/help/html/index.html

/**************************************************/

// Example 004 - Mouse Navigation and Basic Collision
// ex004.c

// In this example we'll start from a skeleton of example 003
// We will add mouse input to enable us to steer and look around
// while we go into "Fly Mode"
// we'll demonstrate how to use basic collisions
// we'll replace two of the cubes with a sphere and a cylinder
// we'll place the materials on all three of our primitives
// we'll load a different skybox and align our sunlight to it

// Notes :
// As before, if you see anything that is overly confusing,
// consult the API docs, post on the forums or the Youtube 
// video comments that accompanies this lesson / example.

// Chad Dore' -Chaduke-
// 20240930
// https://www.youtube.com/chaddore
// https://www.github.com/chaduke/libsgd_examples

#include <sgd/sgd.h>
#include <stdio.h>

void DisplayTextCentered(const char* text,SGD_Font font,float yoffset)
{	
	sgd_Set2DFont(font);	
	float center = sgd_GetWindowWidth() / 2;	
	float tw = sgd_GetTextWidth(font,text) / 2;	
	sgd_Draw2DText(text,center - tw,yoffset);	
}

void DisplayTextRight(const char* text,SGD_Font font,float yoffset)
{	
	sgd_Set2DFont(font);
	float tw = sgd_GetTextWidth(font,text) + 10;
	float right = sgd_GetWindowWidth() - tw;
	sgd_Draw2DText(text,right,yoffset);	
}

int main() {
	
	sgd_Init(); 	
    sgd_CreateWindow(1920, 1080, "Example 004", SGD_WINDOW_FLAGS_FULLSCREEN);
	
	// environment setup
	// load a skybox texture from the assets folder in the libsgd_examples folder
	SGD_Texture environment = sgd_LoadCubeTexture("assets/textures/skybox/skyboxsun5deg.png",4,18);
	sgd_SetEnvTexture(environment);
	SGD_Skybox skybox = sgd_CreateSkybox(environment);
	sgd_SetSkyboxRoughness(skybox,0.2);	
	
	SGD_Camera camera = sgd_CreatePerspectiveCamera();	
	// create an "empty" model called pivot to help out our camera "rig"
	SGD_Model pivot = sgd_CreateModel(0);
	
	// parent the camera to this pivot and now use the pivot to control the camera
	// this gives us the flexibilty of being able to move and rotate the camera
	// from the pivot but then do the same to the camera independently 
	// on different axes, allowing us to make corrections for certain situations
	// I'll demonstrate more later on and also in videos
	sgd_SetEntityParent(camera,pivot);	
	// when we want to move the camera globally we move the pivot now
	sgd_MoveEntity(pivot,0,0.5,10);
	sgd_SetEntityRotation(pivot,0,-60,0);
	
	SGD_Light sun = sgd_CreateDirectionalLight();
	sgd_SetLightShadowsEnabled(sun,SGD_TRUE);
	
	// turn the sun to match the skybox
	sgd_TurnEntity(sun,-5,45,0);
	sgd_SetAmbientLightColor(1,1,1,0.1); 	

	// cube setup
    SGD_Material cube_material = sgd_LoadPBRMaterial("assets/materials/Marble021_1K-JPG");    
	SGD_Mesh cube_mesh = sgd_CreateBoxMesh(-0.5,-0.5,-0.5,0.5,0.5,0.5,cube_material);	
	sgd_SetMeshShadowsEnabled(cube_mesh,SGD_TRUE);
	SGD_Model cube = sgd_CreateModel(cube_mesh);	
	sgd_MoveEntity(cube,0,0.5,3);	
	
	// sphere setup
    SGD_Material sphere_material = sgd_LoadPBRMaterial("assets/materials/Metal061A_1K-JPG");    
	SGD_Mesh sphere_mesh = sgd_CreateSphereMesh(0.5,32,32,sphere_material);	
	sgd_SetMeshShadowsEnabled(sphere_mesh,SGD_TRUE);
	SGD_Model sphere = sgd_CreateModel(sphere_mesh);	
	sgd_MoveEntity(sphere,-2,0.5,3);
	
	// cylinder setup
    SGD_Material cylinder_material = sgd_LoadPBRMaterial("assets/materials/Wood067_1K-JPG");    
	SGD_Mesh cylinder_mesh = sgd_CreateCylinderMesh(1,0.5,32,cylinder_material);	
	sgd_SetMeshShadowsEnabled(cylinder_mesh,SGD_TRUE);
	SGD_Model cylinder = sgd_CreateModel(cylinder_mesh);	
	sgd_MoveEntity(cylinder,2,0.5,3);
	
	// ground setup 
	SGD_Material ground_material = sgd_LoadPBRMaterial("sgd://materials/PavingStones119_1K-JPG"); 	
	SGD_Mesh ground_mesh = sgd_CreateBoxMesh(-20,-0.1,-20,20,0,20,ground_material);	
	sgd_TransformTexCoords(ground_mesh,20,20,0,0);
	SGD_Model ground = sgd_CreateModel(ground_mesh);
		
	// load fonts
	SGD_Font segoe_font = sgd_LoadFont("c:/Windows/Fonts/seguihis.ttf",22);
	SGD_Font segoe_script_font = sgd_LoadFont("c:/Windows/Fonts/segoescb.ttf",30);
	
	float spin_speed = 1.1;
	
	// make some variables to adjust camera move and rotation speed
	float cam_move_speed = 0.1;
	float cam_turn_speed = 0.2;
	
	// hide and lock the mouse cursor so we can have more freedom with out mouselook
	// comment out the line below to see the difference
	sgd_SetMouseCursorMode(3);
	
	// start main loop
    SGD_Bool loop = SGD_TRUE;	
    while(loop) 
	{	
		// poll events and gather input 
		int e = sgd_PollEvents();
		if (e==SGD_EVENT_MASK_CLOSE_CLICKED) loop = SGD_FALSE;
		if (sgd_IsKeyHit(SGD_KEY_ESCAPE)) loop = SGD_FALSE;
		
		// let's use up and down to change the spin speed now
		// since it makes more sense to use left / right for the camera
		if (sgd_IsKeyDown(SGD_KEY_DOWN)) spin_speed-=0.1;
		if (sgd_IsKeyDown(SGD_KEY_UP)) spin_speed+=0.1;		
		
		// move the camera with the keyboard by moving the pivot		
		if (sgd_IsKeyDown(SGD_KEY_A)) sgd_MoveEntity(pivot,-cam_move_speed,0,0);
		if (sgd_IsKeyDown(SGD_KEY_D)) sgd_MoveEntity(pivot,cam_move_speed,0,0);
		if (sgd_IsKeyDown(SGD_KEY_W)) sgd_MoveEntity(pivot,0,0,cam_move_speed);
		if (sgd_IsKeyDown(SGD_KEY_S)) sgd_MoveEntity(pivot,0,0,-cam_move_speed);	

		// we'll use mouse to control our camera now
		// turning the pivot like this will cause the camera to "roll"
		// basically it will twist on the Z-axis, but we'll correct it afterwards		
		sgd_TurnEntity(pivot,-sgd_GetMouseVY() * cam_turn_speed,-sgd_GetMouseVX() * cam_turn_speed,0);	
		
		// correct Z-axis roll
		// comment out the line below to see what happens without it
		sgd_SetEntityRotation(pivot,sgd_GetEntityRX(pivot),sgd_GetEntityRY(pivot),0);
		
		// let's limit our cameras X-axis rotation to prevent gimbal lock
		// comment out the following two lines to see what happens when you face "straight up" or "straight down"
		if (sgd_GetEntityRX(pivot) > 70) sgd_SetEntityRotation(pivot,70,sgd_GetEntityRY(pivot),0);
		if (sgd_GetEntityRX(pivot) < -70) sgd_SetEntityRotation(pivot,-70,sgd_GetEntityRY(pivot),0);
		
		// prevent our camera from going below the ground 
		if (sgd_GetEntityY(pivot) < 0.5) sgd_SetEntityPosition( pivot,sgd_GetEntityX(pivot),0.5,sgd_GetEntityZ(pivot) );
		
		sgd_TurnEntity(cube,0,spin_speed,0);		
		sgd_TurnEntity(sphere,0,spin_speed / 2,0);
		sgd_TurnEntity(cylinder,0,spin_speed * 2,0);
		
		sgd_RenderScene();
		
		// draw our 2D overlay
		sgd_Clear2D();
		
		// get our font height in pixels + some padding
		// we can subtract 
		float fh = sgd_GetFontHeight(segoe_font) + 10;
		// setup our buffer for snprintf
		char buffer[30];	
		
		// black text 
		sgd_Set2DTextColor(0,0,0,1);
		DisplayTextCentered("Making a Flymode Camera",segoe_script_font,3);
		
		// grey text
		sgd_Set2DTextColor(0.5,0.5,0.5,1); 
		sgd_Set2DFont(segoe_font);
		snprintf(buffer, sizeof buffer, "Spin Speed : %f", spin_speed);		
		sgd_Draw2DText(buffer,5,5);
		
		// yellow text for the bottom of the screen
		sgd_Set2DTextColor(1,1,0,1); 
		DisplayTextCentered("- Press Escape to Exit -",segoe_font,sgd_GetWindowHeight() - fh);		
		 
		snprintf(buffer, sizeof buffer, "FPS : %f", sgd_GetFPS());	
		// draw bottom center	
		sgd_Draw2DText(buffer,5,sgd_GetWindowHeight() - fh);
		// draw bottom right
		DisplayTextRight("WASD - Move Camera",segoe_font,sgd_GetWindowHeight() - fh);

		// red text for the right side 
		sgd_Set2DTextColor(1,0,0,1);
		DisplayTextRight("Up and Down Arrows",segoe_font,3);
		DisplayTextRight("Change Spin Speed",segoe_font,fh);		
		sgd_Present();
    }
	sgd_Terminate();
}
