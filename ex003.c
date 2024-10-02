
/**************************************************
/*** LibSGD Examples 
/*** for the C Programming Language
/*** https://patreon.com/libsgd
/*** https://github.com/blitz-research/libsgd/ 
/*** https://libsgd.org/forum/
/*** https://skirmish-dev.net/libsgd/help/html/index.html

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

// We will also add a few extra cubes to demonstrate mesh reuse
// and also the ability to move the camera with the keyboard
// We'll add a few "helper functions" that position text on different 
// parts of the screen and make our code cleaner

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

void DisplayTextCentered(const char* text,SGD_Font font,float yoffset)
{	
	sgd_Set2DFont(font);
	// get our X-axis window center in pixels	
	float center = sgd_GetWindowWidth() / 2;
	// get the width of the text we are displaying and divide by two
	float tw = sgd_GetTextWidth(font,text) / 2;
	// draw the text at the center of screen X-axis
	// and take into the yoffset value for Y-axis positioning
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
	// let's do this in fullscreen HD mode now 
    sgd_CreateWindow(1920, 1080, "Example 003", SGD_WINDOW_FLAGS_FULLSCREEN);
	
	// we no longer need to set a clear color because our skybox will cover it
    // sgd_SetClearColor(0.2, 0.5, 0.9, 1.0);
	SGD_Texture environment = sgd_LoadCubeTexture("sgd://envmaps/sunnysky-cube.png",4,18);
	
	// enable the line below to see the difference an "environment texture" makes on our scene
	// for this scene I think it looks better with out it
	// sgd_SetEnvTexture(environment);
	
	// create a skybox from the environment cube texture
	SGD_Skybox skybox = sgd_CreateSkybox(environment);
	
	// blur the texture a little for better appearance
	// test different values here to see what you like
	sgd_SetSkyboxRoughness(skybox,0.2);
	
	SGD_Camera camera = sgd_CreatePerspectiveCamera();
	
	// move our camera back a little to see all 3 cubes
	sgd_MoveEntity(camera,0,0.5,-2);
	
	// create our sun as a directional light
	// the location of directional lights don't matter
	// only the rotation, specifically on the X and Y axes
	// will change how the light affects the scene
	SGD_Light sun = sgd_CreateDirectionalLight();
	
	// we need to do this to enable the light to cast shadows 
	sgd_SetLightShadowsEnabled(sun,SGD_TRUE);
	// we turn the light -20 degrees on X and -45 on Y
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
	
	// we can now easily create other cubes using the same mesh
	SGD_Model cube_left = sgd_CreateModel(cube_mesh);
	sgd_MoveEntity(cube_left,-2,0.5,3);
	SGD_Model cube_right = sgd_CreateModel(cube_mesh);
	sgd_MoveEntity(cube_right,2,0.5,3);
	
	// our next object, the ground, will consist of a cube mesh
	// but scaled outwards 20 units in the X and Y directions
	// on only 0.1 units on the Y axis 
	// before we do this however, we need a ground material
	// again we will consult the LibSGD asset libary and load one up
	SGD_Material ground_material = sgd_LoadPBRMaterial("sgd://materials/PavingStones119_1K-JPG"); 	
	SGD_Mesh ground_mesh = sgd_CreateBoxMesh(-20,-0.1,-20,20,0,20,ground_material);	
	
	// this will reduce the scale of the ground material and make it look more realistic in our scene
	// feel free to experiment with the values to see what happens
	sgd_TransformTexCoords(ground_mesh,20,20,0,0);
	SGD_Model ground = sgd_CreateModel(ground_mesh);	
	
	float spin_speed = 1.1;	
	
	// let's load some fonts from our Windows folder
	// if for some reason this doesn't work for you check your 
	// windows fonts folder and replace with something else 
	// you have to right-click on the font and choose properties from 
	// windows explorer in order to see the ".ttf" filename
	// you can always fine a lot of .ttf font files on the net too
	SGD_Font segoe_font = sgd_LoadFont("c:/Windows/Fonts/seguihis.ttf",22);
	SGD_Font segoe_script_font = sgd_LoadFont("c:/Windows/Fonts/segoescb.ttf",30);
	
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
		
		// move the camera around with WASD
		// or you can alter this to your preferred keyboard layout
		if (sgd_IsKeyDown(SGD_KEY_A)) sgd_MoveEntity(camera,-0.1,0,0);
		if (sgd_IsKeyDown(SGD_KEY_D)) sgd_MoveEntity(camera,0.1,0,0);
		if (sgd_IsKeyDown(SGD_KEY_W)) sgd_MoveEntity(camera,0,0,0.1);
		if (sgd_IsKeyDown(SGD_KEY_S)) sgd_MoveEntity(camera,0,0,-0.1);	

		// we'll use left and right arrows to steer our camera now
		if (sgd_IsKeyDown(SGD_KEY_LEFT)) sgd_TurnEntity(camera,0,2,0);
		if (sgd_IsKeyDown(SGD_KEY_RIGHT)) sgd_TurnEntity(camera,0,-2,0);
		
		sgd_TurnEntity(cube,0,spin_speed,0);
		// turn the left and right cubes at different speeds
		sgd_TurnEntity(cube_left,0,spin_speed / 2,0);
		sgd_TurnEntity(cube_right,0,spin_speed * 2,0);
		
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
		DisplayTextCentered("Spinning Cubes on a Sunny Day",segoe_script_font,3);
		DisplayTextCentered("by Chaduke",segoe_font,fh + 15);
		
		// grey text
		sgd_Set2DTextColor(0.5,0.5,0.5,1); 
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
		DisplayTextRight("Left and Right Arrows",segoe_font,fh * 2);
		DisplayTextRight("Steer the Camera",segoe_font,fh * 3);
		sgd_Present();
    }
	sgd_Terminate();
}