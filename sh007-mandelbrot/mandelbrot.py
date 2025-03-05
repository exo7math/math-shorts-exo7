
# A library to compute the Mandelbrot set and create video zooms


import numpy as np
from numba import jit

from scipy import interpolate    # for spline interpolation

from matplotlib import pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation


# import timeit

# Need to install numba
# conda activate mandel


### Part A: Constants ###

## Constants    

# Dimensions of the video
divfactor = 1  # 1 = full resolution
video_width_px = 1080 // divfactor
video_height_px = 1920 // divfactor



ratio = video_width_px/video_height_px  # = 9/16 ratio for short video
dpi = 128  # common DPI for video, adjust as needed
fps = 10  # frames per second, adjust as needed

# The whole M set
xmin, xmax, ymin, ymax = -2.0, 0.5, -1.25, 1.25
xc0, yc0 = (xmin + xmax) / 2, (ymin + ymax) / 2
r0 = (xmax - xmin) / 2
whole_mandelbrot_set = (xc0, yc0, r0)



### Part B: Mandelbrot set ###

# Fast Mandelbrot computation using numpy
# reference : https://gist.github.com/jfpuget/60e07a82dece69b011bb

@jit
def mandelbrot(c, maxiter):
    n=0
    z=0
    while (z.real * z.real + z.imag * z.imag < 4.0) and n<maxiter:
        z = z**2 + c
        n += 1
    return n


@jit
def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width,height))
    for i in range(width):
        for j in range(height):
            n3[i,j] = mandelbrot(r1[i] + 1j*r2[j], maxiter)
    return (r1, r2, n3)


### Part C: Mandelbrot images ###

def mandelbrot_image(xmin,xmax,ymin,ymax,width,height,maxiter,cmap='hot'):
    dpi = 72
    img_width = width
    img_height = height
    x,y,z = mandelbrot_set(xmin,xmax,ymin,ymax,img_width,img_height,maxiter)
    
    fig, ax = plt.subplots(figsize=(img_width/dpi, img_height/dpi), dpi=dpi)
    # ticks = np.arange(0,img_width,3*dpi)
    # x_ticks = xmin + (xmax-xmin)*ticks/img_width
    # plt.xticks(ticks, x_ticks)
    # y_ticks = ymin + (ymax-ymin)*ticks/img_width
    # plt.yticks(ticks, y_ticks)

    norm = colors.PowerNorm(0.3)
    ax.imshow(z.T, origin='lower', cmap=cmap, norm=norm)
    plt.show()

# Test image
# mandelbrot_image(-2.0,0.5,-1.25,1.25,1000,1000,10)
# mandelbrot_image(-2.0,0.5,-1.25,1.25,10,10,80)


# Time the execution
# res = timeit.repeat("mandelbrot_set(-2.0,0.5,-1.25,1.25,1000,1000,100)", globals=globals(), number=1, repeat=10)
# print(res)
# print("Mean time:", np.mean(res))
# print("Min time: ", np.min(res))
# print("Max time: ", np.max(res))


### Part D: colors ###  

# https://stackoverflow.com/questions/65018952/rotate-matplotlib-colourmap
def shift_cmap(cmap, frac):
    """Shifts a colormap by a certain fraction.

    Keyword arguments:
    cmap -- the colormap to be shifted. Can be a colormap name or a Colormap object
    frac -- the fraction of the colorbar by which to shift (must be between 0 and 1)
    """
    N = 256
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    n = cmap.name
    x = np.linspace(0,1,N)
    out = np.roll(x, int(N*frac))
    new_cmap = colors.LinearSegmentedColormap.from_list(f'{n}_s', cmap(out))

    # 0 si always black
    # new_cmap.set_under(0.0, color='black', alpha=None)
    return new_cmap


### Part E: Paths for zoom ###





def one_mandelbrot(xc, yc, r, maxiter):
    """ One Mandelbrot image centered at (xc, yc) with radius r """
    x, y, z = mandelbrot_set(xc-r, xc+r, yc-r/ratio, yc+r/ratio, video_width_px, video_height_px, maxiter)
    return z

def one_mandelbrot_image(xc, yc, r, maxiter=80, cmap='plt.cm.hot', powernorm=0.3, data=False):
    """ One Mandelbrot image centered at (xc, yc) with radius r """
    z = one_mandelbrot(xc, yc, r, maxiter)
    fig, ax = plt.subplots(figsize=(video_width_px/dpi, video_height_px/dpi), dpi=dpi)
    ax.axis('off')    
    # cmap = plt.cm.hsv
    cmap = cmap
    cmap.set_over('black', alpha = None)   # black for convergent zc (i.e. with maxiter)
    # norm = colors.Normalize(vmin=0, vmax=maxiter-1)      
    # norm = colors.LogNorm(vmin=0, vmax=maxiter-1)
    norm = colors.PowerNorm(powernorm, vmin=0, vmax=maxiter-1)
    ax.imshow(z.T, origin='lower', norm=norm, cmap=cmap)

    if data:  # Print xc, yc,r on the image
        ax.text(0.5, 0.1, f"{xc:.5f} + i {yc:.5f}, {r:.5f}", fontsize=12, color='white', ha='center', va='center', transform=ax.transAxes)

    plt.show()


# Test one image
# z = one_mandelbrot(-0.75, 1, 3, 10)
# fig, ax = plt.subplots(figsize=(video_width_px/dpi, video_height_px/dpi), dpi=dpi)
# ax.imshow(z.T, origin='lower', cmap='hot')
# plt.show()




def spline_path(points):
    """" A 3D path : 2D path for the centers, 1D path for the radius 
    Output a function from t in [0,1] to (Xc(t), Yc(t), R(t)) 
    The interpolation on the centers is independent of the interpolation on the radii """
    

    # Interpolation on the centers

    # degree of the spline
    X, Y, R = [p[0] for p in points], [p[1] for p in points], [p[2] for p in points]
    if len(X) == 2:
        deg = 1
    elif len(X) == 3:
        deg = 2
    else:
        deg = 3
    spl, _ = interpolate.splprep([X, Y], s=0, k=deg)

    # Interpolation of the radii
    T = np.linspace(0, 1, len(R))
    spl_r = interpolate.splrep(T, R, s=0, k=1)   # linear interpolation


    def path(t):
        xc, yc = interpolate.splev(t, spl)
        r = interpolate.splev(t, spl_r)
        return xc, yc, r
    
    return path

# Test spline path
# x0, y0, r0 = -0.75, 1, 3  # whole Mandelbrot set
# x1, y1, r1 = -0.64, -0.41, 1  # next, zoom to this point
# x2, y2, r2 = -0.6401, -0.405, 0.5  # next, zoom to this point
# points = [ [x0,x1,x2], [y0,y1,y2], [r0,r1,r2] ]
# func_path = spline_path(points)
# for t in np.linspace(0, 1, 10):
#     print(t, func_path(t))



def linear_path(points):
    """ A 3D path, union of linear segments between points """

    X, Y, R = [p[0] for p in points], [p[1] for p in points], [p[2] for p in points]
    n = len(X)-1  # number of legs

    # Interpolation on the centers
    # Interpolation of the radii

    def path(t):
        if t == 1:
            return X[-1], Y[-1], R[-1]
        
        i = int(t*n)
        s = t*n-i
        xc = (1-s)*X[i] + s*X[i+1] 
        yc = (1-s)*Y[i] + s*Y[i+1] 
        rc = (1-s)*R[i] + s*R[i+1] 

        return xc, yc, rc  
    
    vpath = np.vectorize(path)

    return vpath  


    
# Test linear path
# x0, y0, r0 = -0.75, 1, 3  # whole Mandelbrot set
# x1, y1, r1 = -0.64, -0.41, 1  # next, zoom to this point
# x2, y2, r2 = -0.64, -0.41, 0.5  # next, zoom to this point
# points = [ [x0,x1,x2], [y0,y1,y2], [r0,r1,r2] ]
# # for t in np.linspace(0, 1, 100):
# #     print(t, func_path(t))
# func_path = linear_path(points)
# # vfunc_path = np.vectorize(func_path)
# t = np.linspace(0,1,10)
# print(func_path(t))


def round_linear_path(points, r):
    """ A 3D path, union of linear segments between points 
    with a round interpolation at each point (r should be between 0 and 0.5)"""

    X, Y, R = [p[0] for p in points], [p[1] for p in points], [p[2] for p in points]
    n = len(X)-1  # number of legs

    # Interpolation on the centers
    # Interpolation of the radii

    def path(t):
        if t == 1:
            return X[-1], Y[-1], R[-1]
        
        i = int(t*n)
        s = t*n-i

        if r>0 and s > 1-r and i < n-1:
            u = (s - (1-r))/(2*r)
            xA, yA, rA = r*X[i] + (1-r)*X[i+1], r*Y[i] + (1-r)*Y[i+1], r*R[i] + (1-r)*R[i+1]
            xB, yB, rB = (1-r)*X[i+1] + r*X[i+2], (1-r)*Y[i+1] + r*Y[i+2], (1-r)*R[i+1] + r*R[i+2]
            xC, yC, rC = X[i+1], Y[i+1], R[i+1]
            xc = (1-u)**2*xA + 2*u*(1-u)*xC + u**2*xB
            yc = (1-u)**2*yA + 2*u*(1-u)*yC + u**2*yB
            rc = (1-u)**2*rA + 2*u*(1-u)*rC + u**2*rB
            

        elif r>0 and s < r and i > 0:
            u = 1/2 + s/(2*r)
            xA, yA, rA = r*X[i-1] + (1-r)*X[i], r*Y[i-1] + (1-r)*Y[i], r*R[i-1] + (1-r)*R[i]
            xB, yB, rB = (1-r)*X[i] + r*X[i+1], (1-r)*Y[i] + r*Y[i+1], (1-r)*R[i] + r*R[i+1]
            xC, yC, rC = X[i], Y[i], R[i]
            xc = (1-u)**2*xA + 2*u*(1-u)*xC + u**2*xB
            yc = (1-u)**2*yA + 2*u*(1-u)*yC + u**2*yB  
            rc = (1-u)**2*rA + 2*u*(1-u)*rC + u**2*rB

        else: 
            xc = (1-s)*X[i] + s*X[i+1] 
            yc = (1-s)*Y[i] + s*Y[i+1] 
            rc = (1-s)*R[i] + s*R[i+1] 
        
        return xc, yc, rc  
    
    vpath = np.vectorize(path)

    return vpath




def visualize_path(points, func_path):

    # Plot point in x, y only
    X, Y, R = [p[0] for p in points], [p[1] for p in points], [p[2] for p in points]
    plt.plot(X, Y, 'ro')
    # plt.plot(X, Y, 'r-')
    # ax.axis('equal')

    # Plot the linear path
    # path = linear_path(points)
    t = np.linspace(0, 1, 100)
    X, Y, R = func_path(t)
    plt.plot(X, Y, 'b-')
   

    plt.show()
    return



# visualize_path()



def prelim_view(points, maxiter=500):
    # Images at each point
    for xc, yc, rc in points:
        print(xc, yc, rc)
        # cmap = plt.cm.copper

        cmap = plt.cm.pink
        cmap.set_over('black', alpha = None)   # black for convergent zc (i.e. with maxiter)

        # Power of the norm : start at 0.2 for r=2, end at 0.5 for r=0.00001
        mypowernorm = 0.2 + 0.3*np.log(rc/2)/np.log(0.00001/2)

        one_mandelbrot_image(xc, yc, rc, maxiter=maxiter, cmap=cmap, powernorm=mypowernorm, data=True)

    # Path between points

    # func_path = mand.linear_path(points)
    # func_path = mand.spline_path(points)

    func_path = round_linear_path(points, r=0.5)
    t = np.linspace(0, 1, 100)
    path = func_path(t)

    # print(path)
    # visualize_path(points, func_path)




### Part F: Video zoom ###


def linear_zoom(xc1, yc1, r1, maxiter, steps):
    """ A zoom to the point (xc1, yc1) with radius r1 in steps (starting from the whole set) """

    # The whole M set
    xmin, xmax, ymin, ymax = -2.0, 0.5, -1.25, 1.25
    xc0, yc0 = (xmin + xmax) / 2, (ymin + ymax) / 2
    r0 = (xmax - xmin) / 2

    # A series of windows zooming to the point (xc, yc) with radius r
    Xc = np.linspace(xc0, xc1, steps)
    Yc = np.linspace(yc0, yc1, steps)
    R = np.linspace(r0, r1, steps)

    # Create a figure with specified size and a 2D axis
    fig_width_in = video_width_px / dpi    # Calculate figure size in inches
    fig_height_in = video_height_px / dpi
    fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in))

    # Colors
    cmap = 'plasma'
    norm = colors.PowerNorm(0.3)


    def animate(i):        
        t = i / fps 
        print(f"frame {i} time {t:.2f}")
        ax.clear()
        xc, yc, r = Xc[i], Yc[i], R[i]
        z = one_mandelbrot(xc, yc, r, maxiter)
        
        ax.imshow(z.T, origin='lower', cmap=cmap, norm=norm)
        return

    # Call the animator
    ani = animation.FuncAnimation(fig, animate, frames=steps, repeat=False)
    ani.save('video-mandelbrot-01.mp4', fps=fps, dpi=dpi)
    # animate(0)

    # plt.show()
    return

# Test zoom
# linear_zoom(-0.64, -0.41, 0.02, 50, 100)



def curved_zoom(path, maxiter=80, steps=100, pause_in=1, pause_out=2, name='video-mandelbrot.mp4'):
    """ A zoom along a path """

    # A series of windows zooming to the point (xc, yc) with radius r
    Xc, Yc, R = path

     # Create a figure with specified size and a 2D axis
    fig_width_in = video_width_px / dpi    # Calculate figure size in inches
    fig_height_in = video_height_px / dpi
    fig = plt.figure(figsize=(fig_width_in, fig_height_in))
    ax = fig.add_axes([0, 0, 1, 1])

    # Colors
    # cmap = 'hot_r'    
    # cmap = 'plasma'
    # cmap = plt.cm.hsv
    # norm = colors.PowerNorm(0.3)
    # norm = colors.Normalize(vmin=0, vmax=maxiter-1)
    # norm = colors.LogNorm(vmin=0, vmax=maxiter-1)
    
    def animate(i):        
        t = i / fps 
        print(f"frame {i} time {t:.2f}")
        ax.clear()
        xc, yc, r = Xc[i], Yc[i], R[i]
        z = one_mandelbrot(xc, yc, r, maxiter)
        
        # cmap = shift_cmap(plt.cm.hsv, 0.1*t)   # cycling on colors

        # cmap = plt.cm.hsv
        # cmap = plt.cm.hot        
        cmap = plt.cm.pink
        cmap.set_over('black', alpha = None)   # black for convergent zc (i.e. with maxiter)
        mypowernorm = 0.2 + 0.3*np.log(r/2)/np.log(0.00001/2)
        norm = colors.PowerNorm(mypowernorm, vmin=0, vmax=maxiter-1)

        ax.axis('off')
        ax.imshow(z.T, origin='lower', cmap=cmap, norm=norm)
        # no axis 

        return

    # Call the animator
    ani = animation.FuncAnimation(fig, animate, frames=steps, repeat=False)
    ani.save(name, fps=fps, dpi=dpi)

    # plt.show()
    return
       



