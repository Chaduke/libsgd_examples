# LibSGD Examples

This repository contains C and Python code examples demonstrating the functionality of the LibSGD game library which is currently in development.

![Example Screenshot](https://github.com/Chaduke/libsgd_examples/blob/master/images/example.png)

## Table of Contents

- Installation
- Contributing
- License
- Links

## Installation

I created a basic tutorial here if you are unfamiliar with using git to clone a repository - https://youtu.be/71BPcdMyTrA   

1. Clone the repository:  
   ```sh
   git clone https://github.com/chaduke/libsgd_examples.git
   cd libsgd_examples
   ```

2. Install dependencies:  

	**For Python: (quickest route to get started)**  
   	
	Install Python 3.12 or higher. (will probably work with older versions but I've only tested so far with 3.12.5)  
	Make sure you check off the option during the install to add Python to your PATH environment variable.   
	
	then do this:  
	```sh
	pip install libsgd
	```
	then just type: 
	```sh
	python ex001.py 
	```
	or whatever example you want to run.  
	
	PyCharm Community Edition from JetBrains is free and works really well if you need a good Python IDE.  Setting up "virtual environments" takes a little getting used to if you are not familiar with Python. I will probably create a video soon explaining that.      
    
	**For C:**    	
	Get the latest distribution of LibSGD here:        
	https://patreon.com/LibSGD  	
	- Copy the "include" folder and the "lib" folder from the zip file into the libsgd_examples folder.
	- Move "sgd_dynamic.dll" from the "lib" folder into the main folder so it can be found by your compiled executables.  
	
 	Tutorial video here - https://youtu.be/BiGKGD3OtmE
	
	At this time the "distribution" of LibSGD only works with Windows.     	
	You can alternatively build LibSGD yourself for Windows, Mac and Linux, but that involves much more than I have space for here.    
	I will create a video series on how to do this at some point, but it will take some time as it involves a lot of pre-requisite knowledge.  
	If you are interested in the LibSGD source code see the Links section at the bottom of this README.   
	
3. Running the C examples:   	
	- **Install a C compiler.**     
	For Windows I suggest https://www.msys2.org/ to use gcc,      
	or Visual Studio 2022 will work with a little configuration.  
	
	(Note : If you are compiling LibSGD itself on Windows, use VS2022 because you will run into issues with gcc and dependencies at the present time, but for actually using the library gcc/msys2 works fine. For people that are new to C programming, I think its important to learn how to use the command line and see what complex IDEs like Visual Studio are doing behind the scenes.  Also by using gcc/msys2 you can gain some experience that will carry over into a Linux environment.)    
	
	Once msys2 is installed, use the "MSYS2 UCRT64" configuration shortcut (in your start menu) and do this:  
	```sh 
	pacman -S mingw-w64-ucrt-x86_64-gcc
	```
	You will now have gcc installed.  Make sure your PATH environment variable is set to find :   
	C:\msys64\ucrt64\bin, OR modify that path if you installed msys somewhere else.  
	
	Now you should be able to run the example files by using the included build.bat file in the libsgd_examples folder. Make sure you edit this file first to reflect where you cloned the libsgd_examples folder, then you just need to change this part:  
	```code
	set file=exXXX
	```
	where XXX is the example number you want to compile and run, 001, 002, etc..  
	If you prefer to use the Microsoft Compiler / Linker and have Visual Studio 2022 installed, look in build.bat for details.   
	I will soon make youtube videos at https://youtube.com/chaddore that will cover all of this in better detail.  	

## Contributing:  

If you would like to contribute to this project find me (Chaduke) at the forums here :  
- https://libsgd.org/forum  
- You can also email me at chaduke@gmail.com    

I'd be more than happy to add examples or take suggestions, as long as they adhere to the format I'm using here.  I want to make the examples short and self-contained, and individually covering one primary feature/function of LibSGD.    
   	
Other smaller features can also be covered but I'd like to avoid too much repetition.  
     
For more complete games / demos I plan on adding a seperate section for that later.    	
		
## License:     

I'm using Creative Commons 0, so you can do anything you want with the code, but it would be nice if you referenced LibSGD and this repository to help grow the community and the success of LibSGD.     
	
## Links: 
 
To get started with LibSGD, follow the instructions listed here step by step.   
Links to Youtube videos will be in each area to provide additional support.        
Everything here is constantly being worked on so make sure to star and watch the repository to get updates.  
Also please subscribe and like videos on the Youtube channel to get updates as well as help the algorithm.      

If you want get started quickly go the Python route as its a little easier to setup and free, but if you want a deeper learning experience go the C route or both.    

Supporting LibSGD through Patreon will allow you to get a closer look at its development as well as report bugs, ask questions, and make suggestions directly to the developer (Mark Sibly).  You'll be getting a product worth so much more than the amount required to get involved.  I'll also be spending most of my free time working on these tutorials and videos, as well and other members of the community.    

Links :   
- LibSGD Examples Github Repository - https://github.com/chaduke/libsgd_examples  
- LibSGD Tutorials Playlist - https://www.youtube.com/playlist?list=PLw0fDz0F4FPlvPNZYoop9puAC7sHdJl39  
- Chaduke's Youtube - https://youtube.com/chaddore    
- Chaduke's Creative Corner (Discord Invite) - https://discord.gg/Wenrjr8RcZ  
- Get LibSGD (Patreon) - https://patreon.com/libsgd    
- LibSGD Source Github Repository - https://github.com/blitz-research/libsgd  
- Blitz World forums - https://libsgd.org/forum 
- LibSGD Documentation - https://skirmish-dev.net/libsgd/help/html/index.html   