#                                 bbbbbbbb
# LLLLLLLLLLL               iiii  b::::::b               SSSSSSSSSSSSSSS         GGGGGGGGGGGGGDDDDDDDDDDDDD
# L:::::::::L              i::::i b::::::b             SS:::::::::::::::S     GGG::::::::::::GD::::::::::::DDD
# L:::::::::L               iiii  b::::::b            S:::::SSSSSS::::::S   GG:::::::::::::::GD:::::::::::::::DD
# LL:::::::LL                      b:::::b            S:::::S     SSSSSSS  G:::::GGGGGGGG::::GDDD:::::DDDDD:::::D
#   L:::::L               iiiiiii  b:::::bbbbbbbbb    S:::::S             G:::::G       GGGGGG  D:::::D    D:::::D
#   L:::::L               i:::::i  b::::::::::::::bb  S:::::S            G:::::G                D:::::D     D:::::D
#   L:::::L                i::::i  b::::::::::::::::b  S::::SSSS         G:::::G                D:::::D     D:::::D
#   L:::::L                i::::i  b:::::bbbbb:::::::b  SS::::::SSSSS    G:::::G    GGGGGGGGGG  D:::::D     D:::::D
#   L:::::L                i::::i  b:::::b    b::::::b    SSS::::::::SS  G:::::G    G::::::::G  D:::::D     D:::::D
#   L:::::L                i::::i  b:::::b     b:::::b       SSSSSS::::S G:::::G    GGGGG::::G  D:::::D     D:::::D
#   L:::::L                i::::i  b:::::b     b:::::b            S:::::SG:::::G        G::::G  D:::::D     D:::::D
#   L:::::L         LLLLLL i::::i  b:::::b     b:::::b            S:::::S G:::::G       G::::G  D:::::D    D:::::D
# LL:::::::LLLLLLLLL:::::Li::::::i b:::::bbbbbb::::::bSSSSSSS     S:::::S  G:::::GGGGGGGG::::GDDD:::::DDDDD:::::D
# L::::::::::::::::::::::Li::::::i b::::::::::::::::b S::::::SSSSSS:::::S   GG:::::::::::::::GD:::::::::::::::DD
# L::::::::::::::::::::::Li::::::i b:::::::::::::::b  S:::::::::::::::SS      GGG::::::GGG:::GD::::::::::::DDD
# LLLLLLLLLLLLLLLLLLLLLLLLiiiiiiii bbbbbbbbbbbbbbbb    SSSSSSSSSSSSSSS           GGGGGG   GGGGDDDDDDDDDDDDD
#
#  __ _                 _          ___                          ___               _                                  _
# / _(_)_ __ ___  _ __ | | ___    / _ \__ _ _ __ ___   ___     /   \_____   _____| | ___  _ __  _ __ ___   ___ _ __ | |_
# \ \| | '_ ` _ \| '_ \| |/ _ \  / /_\/ _` | '_ ` _ \ / _ \   / /\ / _ \ \ / / _ \ |/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __|
# _\ \ | | | | | | |_) | |  __/ / /_\\ (_| | | | | | |  __/  / /_//  __/\ V /  __/ | (_) | |_) | | | | | |  __/ | | | |_
# \__/_|_| |_| |_| .__/|_|\___| \____/\__,_|_| |_| |_|\___| /___,' \___| \_/ \___|_|\___/| .__/|_| |_| |_|\___|_| |_|\__|
#                |_|                                                                     |_|
#

############################################################################
#### LibSGD Examples
#### for the Python Programming Language
#### Get LibSGD here - https://patreon.com/libsgd
#### LibSGD Github Repository - https://github.com/blitz-research/libsgd/
#### LibSGD Forums - https://libsgd.org/forum/
#### API Docs - https://skirmish-dev.net/libsgd/help/html/index.html 
###########################################################################

# Example 001 - Hello World
# ex001.py

# This example gets a LibSGD window up and running
# clears the background to blue, starts a game loop,
# polls input events, prints some 2D text, then exits
# when the window is closed or Escape key is pressed

# Notes :
# This file is compatible with LibSGD version 0.15
# The latest distribution is available from Patreon link above
# You only need to pay 2 bucks a month (minimum) to support this awesome project
# and I think it's well worth it!
# if you have any questions, comments or bug reports see the forum link above

# If you want examples with a lot more descriptive text, take a look at the
# C language examples in this same folder.  Since C is the "mother" language of
# most of the software used in the world, it would not hurt at all to familiarize
# yourself with C, as well as learn about what's going on under the hood when you
# use Python and see how it's saving you all time and effort!
# the C examples will be WAY more verbose comments wise, at least in the beginning.

# Chad Dore' -Chaduke-
# 20240924
# https://www.youtube.com/chaddore
# https://www.github.com/chaduke

from libsgd import sgd

sgd.init()
sgd.createWindow(1280,720,"Example 001",sgd.WINDOW_FLAGS_CENTERED)
sgd.setClearColor(0.1,0.2,0.9,1.0)
loop = True
while loop:
    e = sgd.pollEvents()
    if e == sgd.EVENT_MASK_CLOSE_CLICKED or sgd.isKeyHit(sgd.KEY_ESCAPE) : loop = False
    # render 3D stuff
    sgd.renderScene()
    # render 2D stuff
    sgd.clear2D()
    sgd.draw2DText("Hello LibSGD! Press Escape to exit",5,5)
    sgd.draw2DText("FPS : " + str(sgd.getFPS()), 5, sgd.getWindowHeight() - 20)
    sgd.present() # swap buffers
sgd.terminate()
