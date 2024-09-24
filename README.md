# LibSGD Examples

This repository contains C and Python code examples demonstrating the functionality of the LibSGD game library which is currently in development.

![Example Screenshot](https://github.com/Chaduke/libsgd_examples/blob/master/images/example.png)

## Table of Contents

- Installation
- Usage
- Examples
- Contributing
- License

## Installation

1. Clone the repository:  
   ```sh
   git clone https://github.com/chaduke/libsgd_examples.git
   cd libsgd_examples
   ```

2. Install dependencies:  
	**For C:**    	
	Get the latest distribution of LibSGD here:        
	https://patreon.com/LibSGD  	
	- Copy the "include" folder and the "lib" folder from the zip file into the libsgd_examples folder.
	- Move "sgd_dynamic.dll" from the "lib" folder into the main folder so it can be found by your compiled executables.	
 	
	At this time the "distribution" of LibSGD only works with Windows.     	
	You can alternatively build LibSGD yourself for Windows, Mac and Linux, but that involves much more than I have space for here. 
	
	The repository is located here :     
	https://www.github.com/blitz-research/libsgd  
	
	**For Python:** 	
	Install Python 3.12 or higher, will probably work with older versions but I've only tested so far with 3.12.5, then do this:
	```sh
	pip install libsgd
	```
	then just type: 
	```sh
	python ex001.py 
	```
	or whatever example you want to run.  	
	
	The C examples are way more heavily commented so I suggest studying those regardless of whether you intend on using Python primarily or not.
	
	PyCharm Community Edition from JetBrains is free and works really well if you need a good Python IDE.    
	Setting up "virtual environments" takes a little getting used to if you are not familiar with Python.    
	I will probably create a video soon explaining that.  
	
3. Running the C examples:   	
	- **Install a C compiler.**     
	For Windows I suggest https://www.msys2.org/ to use gcc,      
	or Visual Studio 2022 will work with a little configuration.  
	
	(Note : If you are compiling LibSGD itself, use VS2022, you will run into issues with gcc, but for actually using the library gcc / msys works fine.)  
	
	Once msys2 is installed, use the UCRT64 configuration shortcut and do this:  
	```sh 
	pacman -S mingw-w64-ucrt-x86_64-gcc
	```
	You will now have gcc installed.  Make sure your PATH environment variable is set to find :   
	C:\msys64\ucrt64\bin, and modify if you installed it somewhere else.  
	
	Now you should be able to run the example files by using the included build.bat file in the libsgd_examples folder.  
	Make sure you edit this file first to reflect where you cloned the libsgd_examples folder, then you just need to change this part:  
	```code
	set file=exXXX
	```
	where XXX is the example number you want to compile and run, 001, 002, etc..   	
	I will soon make youtube videos at https://youtube.com/chaddore that will cover all of this in better detail. 

4. Contributing:  
	If you would like to contribute to this project find me at the forums here :
	- https://skirmish-dev.net/forum/ 
	- You can also email me at chaduke@gmail.com
	
	- I'd be more than happy to add examples or take suggestions, as long as they adhere to the format I'm using here.
	- I want to make the examples short and self-contained, and individually covering one primary feature/function of LibSGD.	
	- Other smaller features can also be covered but I'd like to avoid too much repetition. 
	- For more complete games / demos I plan on adding a seperate section for that later.	
		
5. License:     
	I'm using Creative Commons 0, so you can do anything you want with the code, but it would be nice if you referenced LibSGD and this repository to help grow the community and the success of LibSGD.  
	
6. Links:
	- Chaduke's Youtube - https://youtube.com/chaddore
	- Get LibSGD (Patreon) - https://patreon.com/libsgd
	- Blitz World forums - https://skirmish-dev.net/forum/
	- LibSGD Documentation - https://skirmish-dev.net/libsgd/help/html/sgd_8h.html