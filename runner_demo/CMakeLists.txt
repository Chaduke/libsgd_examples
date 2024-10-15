# TO BUILD - on your machine with Visual Studio 2022 installed do the follwing - 
# "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvarsall.bat" x64
# cd [path to this folder]
# cmake -G "Visual Studio 17 2022" -S . -B build
# cmake --build build --config Release
# mv ./build/Release/RunnerDemo.exe .
# ./RunnerDemo.exe

# make sure you have sgd_dynamic.dll version 0.16 in this folder 

cmake_minimum_required(VERSION 3.10)

# Project name
project(RunnerDemo)

# Specify C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include directories
include_directories(include imgui)
link_directories(${PROJECT_SOURCE_DIR}/lib)

# Clone imgui repository if not already cloned
if(NOT EXISTS "${PROJECT_SOURCE_DIR}/imgui")
    message(STATUS "Cloning ImGui repository...")
    execute_process(
        COMMAND git clone https://github.com/blitz-research/imgui ${PROJECT_SOURCE_DIR}/imgui
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    )
endif()

# Source files
set(SOURCES
    src/main.cpp
	src/environment.cpp
    src/player.cpp
	src/misc_functions.cpp
    imgui/imgui.cpp
    imgui/imgui_demo.cpp
    imgui/imgui_draw.cpp
	imgui/imgui_tables.cpp
    imgui/imgui_widgets.cpp
)

# Add executable
add_executable(RunnerDemo ${SOURCES})

# Link libraries
target_link_libraries(RunnerDemo ${PROJECT_SOURCE_DIR}/lib/sgd_dynamic.lib)
