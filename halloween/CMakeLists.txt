# TO BUILD  on your machine with Visual Studio 2022 installed do the follwing - 
# "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvarsall.bat" x64
# cd [path to this folder]
# cmake -G "Visual Studio 17 2022" -S . -B build
# cmake --build build --config Release
# ./build/Release/HalloweenShooter.exe

# make sure you have sgd_dynamic.dll version 0.16 in the build/Release folder

cmake_minimum_required(VERSION 3.10)

# Project name
project(HalloweenShooter)

# Specify C++ standard
set(CMAKE_CXX_STANDARD 11)
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
    src/halloween_shooter.cpp
    imgui/imgui.cpp
    imgui/imgui_demo.cpp
    imgui/imgui_draw.cpp
	imgui/imgui_tables.cpp
    imgui/imgui_widgets.cpp
)

# Add executable
add_executable(HalloweenShooter ${SOURCES})

# Link libraries
target_link_libraries(HalloweenShooter ${PROJECT_SOURCE_DIR}/lib/sgd_dynamic.lib)
