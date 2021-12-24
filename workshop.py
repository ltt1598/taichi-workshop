import taichi as ti
ti.init(ti.cpu)

# gravitational constant 6.67408e-11, using 1 for simplicity
G = 1
PI = 3.141592653
TAU = 2*PI

N = 3000    # number of planets
m = 1       # unit mass
v0 = 100    # init vel

dt = 1e-4   # time-step size

# pos, vel and force of the particles
# Nx2 vectors
pos = ti.Vector.field(2, ti.f32, N)
vel = ti.Vector.field(2, ti.f32, N)
#TODO1 define the force for the particles.

@ti.kernel
def initialize():   # initialize the particles on a torus: r1=0.2, r2=0.4
    center=ti.Vector([0.5, 0.5])
    for i in range(N):
        theta = ti.random() * TAU
        r = ti.sqrt(ti.random()) * 0.2 + 0.2 
        # LOOKAT: offset is initialized using a random radian theta
        offset = r * ti.Vector([ti.cos(theta), ti.sin(theta)])
        pos[i] = center+offset
        # LOOKAT: velocity is initialized to the tangent direction
        vel[i] = ti.Vector([-offset.y, offset.x]) * v0

@ti.kernel          # compute the force for each particle
def compute_force():
    # clear force
    for i in range(N):
        ...
        #TODO2: set the force of particle i to zero

    # compute gravitational force
    for i in range(N):
        ...
        #TODO2: compute the gravitational force for all particles

@ti.kernel
def update():     #symplectic euler integration
    for i in range(N):     
        pos[i] += vel[i]*dt
        #TODO1: update velocity using acceleration
        #TODO1: update position using velocity

if __name__ == "__main__":

    paused = False
    initialize()

    gui = ti.GUI('N-body problem', (512, 512))

    while gui.running:
        for e in gui.get_events(ti.GUI.PRESS):
            if e.key == ti.GUI.ESCAPE:
                exit()
            elif e.key == ti.GUI.SPACE:
                paused = not paused
                print("paused =", paused)
            elif e.key == 'r':
                initialize()

        if (not paused):
            compute_force()
            update()

        gui.clear(0x112F41)
        gui.circles(pos.to_numpy(), color=0xfeffd4, radius=2)
        gui.show()