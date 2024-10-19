cmake_minimum_required(VERSION 3.10)

# Project name
project(RunnerDemo)

# Specify C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include directories
include_directories(../include imgui)
link_directories(../lib)

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
target_link_libraries(RunnerDemo sgd_dynamic.lib)
