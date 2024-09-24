from libsgd import sgd

sgd.Init()
sgd.CreateWindow(1280,720,"Example 001",sgd.WINDOW_FLAGS_CENTERED)
sgd.SetClearColor(0.1,0.2,0.9,1.0)
loop = True
while loop:
    e = sgd.PollEvents()
    if e == sgd.EVENT_MASK_CLOSE_CLICKED or sgd.IsKeyHit(sgd.KEY_ESCAPE) : loop = False
    sgd.RenderScene()  # render 3D stuff
    # render 2D stuff
    sgd.Clear2D()
    sgd.Draw2DText("Hello World",5,5)
    sgd.Present() # swap buffers
sgd.Terminate()
