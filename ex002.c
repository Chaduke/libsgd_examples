
/**************************************************
*** LibSGD Examples 
*** for the C Programming Language
*** https://patreon.com/libsgd
*** https://github.com/blitz-research/libsgd/ 
*** https://libsgd.org/forum/
*** https://skirmish-dev.net/libsgd/help/html/index.html
**************************************************/

// Example 002 - A Spinning Cube
// ex002.c

// This example picks up where the previous one left off
// with a basic game "skeleton" but with no 3D objects added
// now we will create some essential pieces that complete a 
// working 3D scene and then add a "test cube", place a texture on it
// then during the game loop we will make it spin

// Notes :
// I will not add comments to anything I commented on previously
// unless the new code additions affect it in some way
// if anything uncommented doesn't make sense or requires an 
// explanation check with a previous example, or consult the API docs

// Chad Dore' -Chaduke-
// 20240923
// https://www.youtube.com/chaddore
// https://www.github.com/chaduke/libsgd_examples

#include <sgd/sgd.h>
#include <stdio.h>

int main() {
	
	sgd_Init(); 
    sgd_CreateWindow(1280, 720, "Example 002", SGD_WINDOW_FLAGS_CENTERED);
    sgd_SetClearColor(0.2, 0.5, 0.9, 1.0);
	
	// in order for 3D rendering to work we need to add a camera
	// "perspective" cameras are what you see most often in 3D games
	// there is also an option for an "orthographic" camera that is usually
	// more popular in 3D "applications" where you occasionally want to see 
	// the 3D scene in a "2D way" by looking at the objects straight down one axis
	// like from the "top" or the "side" or "front" view
	// it may also be useful for making 2D games but while using 3D models instead of sprites
    // this might be something interesting to explore later on			
	SGD_Camera camera = sgd_CreatePerspectiveCamera();
    
	// in order to see anything we need to add light
	// for now lets just add some "ambient" light so
	// we can see our cube spinning, in the next tutorial we'll 
	// experiment with different types of lights and shadows
	sgd_SetAmbientLightColor(1,1,1,1); 
	// this is a full bright light source coming from "all over"
	// later when we start adding point, directional, and spot lights 
	// we'll want to tone this ambient light way down or even remove it 
	// otherwise we wont see the shading those lights create

	// in order to create a cube we first need a material to place on its 6 sides 
    // so we can see it.  We can easily load a quick material from 
    // SGD library over the internet like this : 
    SGD_Material cube_material = sgd_LoadPBRMaterial("sgd://materials/Bricks076C_1K-JPG");
	
    // to browse other avaialable materials and assets look here:
	// https://skirmish-dev.net/assets/
	// also check this forum thread to find out where to get other mostly free game assets:
	// https://skirmish-dev.net/forum/topic/11/free-game-development-resources
	
	// now that we have a material loaded we need to create a "mesh" that defines
	// the points, edges, and faces that make up the cube, and tells LibSGD where to
	// apply this material into 3D space	
	SGD_Mesh cube_mesh = sgd_CreateBoxMesh(-0.5,-0.5,-0.5,0.5,0.5,0.5,cube_material);
	
	// one last step before we can see our cube rendered, we need to create a "model"
	// from this mesh with the material applied to it.  The model is the part that 
	// stores all the "transform" information like its position, rotation, and scale
	// all objects in LibSGD have this information applied and are referred to as "Entities" 
	// the camera we created earlier is also considered an entity and can be moved and rotated but not scaled
	// we'll just call our cube model "cube" because the model is the only part we really need to refer
	// to once the game loop starts.  If all this seems confusing don't worry, it will come together 
	// once you see it in action and start experimenting, and then you can come back and re-read all this crap
	// and it will start to sink in and eventually you'll be an expert, just be patient, it's totally worth it
	SGD_Model cube = sgd_CreateModel(cube_mesh);
	
	// when objects are first created they are at x,y,z location 0,0,0
	// since both our camera and our cube are located at 0,0,0
	// we would not be able to see the cube because the camera would be inside it
	// the camera faces forward by default so we need to move the cube forward 3 units 
	// in order to see it. Forward is a positive number on the z-axis
	sgd_MoveEntity(cube,0,0,3);
	// we could have also moved the camera backwards 3 units like this :
	// sgd_MoveEntity(camera,0,0,-3);
	// and got pretty much the same result as far as what we see on screen
	
	// for fun let's create a float variable called "spin_speed" and use the 
	// arrow keys to control it along with the amount our cube will turn each frame
	float spin_speed = 1.0;
	
    SGD_Bool loop = SGD_TRUE;	
    while(loop) 
	{	
		int e = sgd_PollEvents();
		if (e==SGD_EVENT_MASK_CLOSE_CLICKED) loop = SGD_FALSE;
		if (sgd_IsKeyHit(SGD_KEY_ESCAPE)) loop = SGD_FALSE;	
		
		// by holding down the left or right arrow keys 
		// we can change the cubes spin speed by a small amount
		if (sgd_IsKeyDown(SGD_KEY_LEFT)) spin_speed-=0.1;
		if (sgd_IsKeyDown(SGD_KEY_RIGHT)) spin_speed+=0.1;
		
		// we created our cube model before the game loop started
		// and as long as the camera, light, and objects are created and 
		// in place, nothing needs to happen here in order for them to render
		// however we'd just be looking at a still scene so let's make the cube spin
		sgd_TurnEntity(cube,0,spin_speed,0);
		// this turns the cube a number of degrees on its Y axis each frame 
		// based on the value of the variable spin_speeed
	    // the Y axis runs from the top of the screen through the middle of the cube 
	    // and to the bottom of the screen
		
        sgd_RenderScene();
		sgd_Clear2D();
		sgd_Draw2DText("A spinning textured cube, use left and right arrows to change speed, ESC to exit",5,5);		

		char buffer[30]; // increase the size to handle spin speed as well
		snprintf(buffer, sizeof buffer, "FPS : %f", sgd_GetFPS());
		sgd_Draw2DText(buffer,5,sgd_GetWindowHeight() - 20);
		
		// in the same way we converted the FPS float value to a char array 
		// we'll do the same with the spin_speed variable so we can see its current value
		snprintf(buffer, sizeof buffer, "Spin Speed : %f", spin_speed);
		sgd_Draw2DText(buffer,5,25);
		sgd_Present();
    }
	sgd_Terminate();
}