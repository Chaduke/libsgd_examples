/*
                                bbbbbbbb                                                                         
LLLLLLLLLLL               iiii  b::::::b               SSSSSSSSSSSSSSS         GGGGGGGGGGGGGDDDDDDDDDDDDD        
L:::::::::L              i::::i b::::::b             SS:::::::::::::::S     GGG::::::::::::GD::::::::::::DDD     
L:::::::::L               iiii  b::::::b            S:::::SSSSSS::::::S   GG:::::::::::::::GD:::::::::::::::DD   
LL:::::::LL                      b:::::b            S:::::S     SSSSSSS  G:::::GGGGGGGG::::GDDD:::::DDDDD:::::D  
  L:::::L               iiiiiii  b:::::bbbbbbbbb    S:::::S             G:::::G       GGGGGG  D:::::D    D:::::D 
  L:::::L               i:::::i  b::::::::::::::bb  S:::::S            G:::::G                D:::::D     D:::::D
  L:::::L                i::::i  b::::::::::::::::b  S::::SSSS         G:::::G                D:::::D     D:::::D
  L:::::L                i::::i  b:::::bbbbb:::::::b  SS::::::SSSSS    G:::::G    GGGGGGGGGG  D:::::D     D:::::D
  L:::::L                i::::i  b:::::b    b::::::b    SSS::::::::SS  G:::::G    G::::::::G  D:::::D     D:::::D
  L:::::L                i::::i  b:::::b     b:::::b       SSSSSS::::S G:::::G    GGGGG::::G  D:::::D     D:::::D
  L:::::L                i::::i  b:::::b     b:::::b            S:::::SG:::::G        G::::G  D:::::D     D:::::D
  L:::::L         LLLLLL i::::i  b:::::b     b:::::b            S:::::S G:::::G       G::::G  D:::::D    D:::::D 
LL:::::::LLLLLLLLL:::::Li::::::i b:::::bbbbbb::::::bSSSSSSS     S:::::S  G:::::GGGGGGGG::::GDDD:::::DDDDD:::::D  
L::::::::::::::::::::::Li::::::i b::::::::::::::::b S::::::SSSSSS:::::S   GG:::::::::::::::GD:::::::::::::::DD   
L::::::::::::::::::::::Li::::::i b:::::::::::::::b  S:::::::::::::::SS      GGG::::::GGG:::GD::::::::::::DDD     
LLLLLLLLLLLLLLLLLLLLLLLLiiiiiiii bbbbbbbbbbbbbbbb    SSSSSSSSSSSSSSS           GGGGGG   GGGGDDDDDDDDDDDDD  

 __ _                 _          ___                          ___               _                                  _   
/ _(_)_ __ ___  _ __ | | ___    / _ \__ _ _ __ ___   ___     /   \_____   _____| | ___  _ __  _ __ ___   ___ _ __ | |_ 
\ \| | '_ ` _ \| '_ \| |/ _ \  / /_\/ _` | '_ ` _ \ / _ \   / /\ / _ \ \ / / _ \ |/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __|
_\ \ | | | | | | |_) | |  __/ / /_\\ (_| | | | | | |  __/  / /_//  __/\ V /  __/ | (_) | |_) | | | | | |  __/ | | | |_ 
\__/_|_| |_| |_| .__/|_|\___| \____/\__,_|_| |_| |_|\___| /___,' \___| \_/ \___|_|\___/| .__/|_| |_| |_|\___|_| |_|\__|
               |_|                                                                     |_|                             
*/

/**************************************************
/*** LibSGD Examples 
/*** for the C Programming Language
/*** https://patreon.com/libsgd
/*** https://github.com/blitz-research/libsgd/ 
/*** https://skirmish-dev.net/forum/
/**************************************************/

// Example 001 - Hello World!
// ex001.c

// This example gets a LibSGD window up and running 
// clears the background to blue, starts a game loop,
// polls input events, prints some 2D text, then exits
// when the window is closed or Escape key is pressed

// Notes :
// This file is compatitible with LibSGD version 0.14.4
// The latest distribution is available from Patreon link above
// You only need to pay 2 bucks a month (minimum) to support this awesome project 
// and I think it's well worth it! 
// if you have any questions, comments or bug reports see the forum link above

// If you are saavy with C++ and CMake you can compile LibSGD yourself
// fairly easily from the Github repo noted above, just be prepared to give up 
// around 10 Gigs of HD space (maybe more) and possibly a few hours of your time 
// depending on your skill level and speed of your machine

// the current distribution zip file has the folders "include" and "lib"
// make sure to copy these folders to your project folder 
// also make sure a copy of "sgd_dynamic.dll" (found in the "lib" folder)
// resides in your project folder next to your executable 
// or wherever your executable resides after compilation 

// Chad Dore' -Chaduke-
// 20240923

// include the main LibSGD header file
#include <sgd/sgd.h>

// for snprintf
#include <stdio.h>

int main() {
	// initialize LibSGD
	sgd_Init();
	
    // create a window, this also creates an empty "scene"
	// API documentation on different window flags (among everything else) can be found at:
	// https://skirmish-dev.net/libsgd/help/html/sgd_8h.html
	// (look towards the end of the page)	
    sgd_CreateWindow(1280, 720, "Example 001", SGD_WINDOW_FLAGS_CENTERED);
	
	// set the scene clear color
	// it defaults to solid black but let's change it to a sky blue color
	// the parameters are red, green, blue, and alpha
	// floating point numbers ranging from 0.0 to 1.0
	// I'll create some examples of using alpha values other than 1.0 
	// later down the road, I'm not even really sure at this point
	// how it might apply to the background clear color
    sgd_SetClearColor(0.2, 0.5, 0.9, 1.0);
	
	// create a boolean (True or False) called "loop"
	// as long as it remains true the game loop will continue on
	// you can probably use 0 and 1 here to represent true and false
	// but I think seeing the words written out makes the code 
	// more understandable 		
    SGD_Bool loop = SGD_TRUE;
	
	// start the main game loop
    while(loop) 
	{	
		// create an integer variable "e" to store the result of the "PollEvents" function
		// you can find the event mask values in the API documentation listed above
		// or by looking at sgd.h
		// you can also do a search on the github repository
		// all are useful tools to help in learning LibSGD
		
		// the most popular is SGD_EVENT_MASK_CLOSE_CLICKED
		// which has a value of 1 and occurs when the user 
		// clicks the X in the upper right of the window to close it
		// there are also less exciting events for suspending and minimizing 
		// that I'll make examples for later 
		int e = sgd_PollEvents();
		
		// check if the user closed the window 
		// if so set loop to false which will cause the loop to end		
		if (e==SGD_EVENT_MASK_CLOSE_CLICKED) loop = SGD_FALSE;
		
		// check if the user pressed the Escape key
		// and if so set loop false and exit as well	
		// you can also exit most windows programs with ALT-F4
		// unless something is really wrong or nothing is 
		// polling the keyboard.  If you leave out the PollEvents
		// function or just don't properly handle it you'll get 
		// this condition and may be forced to CTRL-ALT-DELETE or even
		// have to power off your machine in some cases 
		if (sgd_IsKeyHit(SGD_KEY_ESCAPE)) loop = SGD_FALSE;
		
		///////////////////////////////////////////////////////////////////
		// this is the area where we normally gather other types of input
		// for instance other keys, pressed once or held down
		// also mouse input and/or gamepad input 
		
		// once we've gathered all our user input, we make changes 
		// to any 3D objects we have in our scene if necessary
		///////////////////////////////////////////////////////////////////
		
		// finally we process and render these 3D objects to an offscreen buffer		
        sgd_RenderScene();
		
		// before we transfer our buffer to the actual screen
		// we want to process all of our 2D drawing like text, 2D shapes, images, GUIs, HUDs,etc.
		// calling Clear2D only clears the 2D stuff we drew on the last pass, it doesn't affect our 3D render		
		sgd_Clear2D();
		
		// draw some 2D text at the upper left corner of the screen
		// "overlayed" on top of our 3D scene
		sgd_Draw2DText("Hello LibSGD! - Press Escape to Exit",5,5);
		
		// let's also draw our frames per second at the bottom left
		// Draw2DText expects a char array (a string in C)
		// but sgd_GetFPS() returns a float value
		// we can create an array called buffer to hold our string
		// a length of 16 is enough space to hold our FPS string
		char buffer[16];
		
		// use the snprintf function to basically "print"
		// the float value into the buffer we created
		// you have to #include <stdio.h> above to do this 
		// if you're not familiar with printf and escape sequences in C
		// https://en.wikipedia.org/wiki/Escape_sequences_in_C
		snprintf(buffer, sizeof buffer, "FPS : %f", sgd_GetFPS());
		
		// we also the use the GetWindowHeight function here 
		// to move to the bottom of the screen, then back up 20 pixels
		// to cover the height of the default font
		// we'll cover loading and changing fonts later
		sgd_Draw2DText(buffer,5,sgd_GetWindowHeight() - 20);
			
		// this final call in the loop takes the combined result 
		// of what we have on our offscreen buffers
		// and transfers it to our display
		// by default this will occur 60 times per second
		// unless our CPU or GPU is struggling to keep up
		sgd_Present();
    }
	// exit the loop and call terminate on LibSGD
	// if you create other data structures in memory
	// it may be required to clean them up here as well
	// not doing so can cause all kinds of instability / problems
	// calling Terminate here should clean anything up related to LibSGD
	sgd_Terminate();
}